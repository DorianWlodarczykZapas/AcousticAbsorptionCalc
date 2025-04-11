from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from RoomAcousticCalculator import RoomAcousticCalculator

from .models import Norm


class AcousticCalculationView(View):
    def post(self, request, *args, **kwargs):
        import json

        try:
            data = json.loads(request.body)

            height = data.get("height")
            length = data.get("length")
            width = data.get("width")
            furnishing = data.get("furnishing", {})
            construction = data.get("construction", {})
            norm_id = data.get("norm_id")
            frequency = data.get("frequency")

            if not all([height, length, width, norm_id, frequency]):
                return JsonResponse({"error": "Brakuje wymaganych danych."}, status=400)

            norm = get_object_or_404(Norm, id=norm_id)

            calculator = RoomAcousticCalculator(
                height=height,
                length=length,
                width=width,
                furnishing=furnishing,
                construction=construction,
                norm=norm,
            )
            rt = calculator.sabine_reverberation_time(frequency)
            is_within = calculator.check_if_within_norm(rt)
            calculator.save_calculation(frequency)

            return JsonResponse(
                {
                    "reverberation_time": float(rt),
                    "is_within_norm": is_within,
                    "message": "Pomiar wykonany poprawnie.",
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
