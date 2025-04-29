import json
from typing import Any

from calculations.RoomAcousticCalculator import RoomAcousticCalculator
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Norm


class AcousticCalculationView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            data: dict[str, Any] = json.loads(request.body)

            height: float | None = data.get("height")
            length: float | None = data.get("length")
            width: float | None = data.get("width")
            furnishing: dict[str, float] = data.get("furnishing", {})
            construction: dict[str, float] = data.get("construction", {})
            norm_id: int | None = data.get("norm_id")
            frequency: str | None = data.get("frequency")

            if not all([height, length, width, norm_id, frequency]):
                return JsonResponse({"error": "Brakuje wymaganych danych."}, status=400)

            norm: Norm = get_object_or_404(Norm, id=norm_id)

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
