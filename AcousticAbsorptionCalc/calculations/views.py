import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .acoustic_calculator import AcousticCalculator
from .models import Calculation, Room


class RoomAcousticCalculationView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            room_id = data.get("room_id")
            if not room_id:
                return JsonResponse({"error": "Missing room_id"}, status=400)

            room = get_object_or_404(Room, id=room_id)

            room_dimensions = {
                "width": float(room.width),
                "length": float(room.length),
                "height": float(room.height),
            }

            construction_surfaces = [
                {"material": surface.material, "area_m2": float(surface.area)}
                for surface in room.surfaces.all()
            ]

            furnishing_elements = [
                {"material": furnishing.material, "area_m2": float(furnishing.quantity)}
                for furnishing in room.furnishings.all()
            ]

            calculator = AcousticCalculator(
                norm=room.norm,
                room_dimensions=room_dimensions,
                construction_surfaces=construction_surfaces,
                furnishing_elements=furnishing_elements,
                freq_band="500",
            )

            results = calculator.result()

            # Update or create Calculation
            Calculation.objects.update_or_create(
                room=room,
                defaults={
                    "norm": room.norm,
                    "room_height": room.height,
                    "room_volume": results["volume_m3"],
                    "room_surface_area": results["surface_area_m2"],
                    "reverberation_time": results["reverberation_time_s"],
                    "sti": results["estimated_sti"],
                    "required_absorption": results["absorption_required"],
                    "achieved_absorption": results["absorption_achieved"],
                    "is_within_norm": results["norm_passed"],
                },
            )

            return JsonResponse(
                {
                    "volume_m3": results["volume_m3"],
                    "surface_area_m2": results["surface_area_m2"],
                    "absorption_achieved": results["absorption_achieved"],
                    "absorption_required": results["absorption_required"],
                    "reverberation_time_s": results["reverberation_time_s"],
                    "estimated_sti": results["estimated_sti"],
                    "norm_passed": results["norm_passed"],
                    "message": "Calculation completed successfully.",
                }
            )

        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
