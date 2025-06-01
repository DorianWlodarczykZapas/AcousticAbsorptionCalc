import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views import View

from .acoustic_calculator import AcousticCalculator
from .models import Material, Norm


class AcousticCalculationView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            data: dict[str, Any] = json.loads(request.body)

            height = data.get("height")
            length = data.get("length")
            width = data.get("width")
            norm_id = data.get("norm_id")
            frequency = data.get("frequency", "500")

            construction_data = data.get("construction", [])
            furnishing_data = data.get("furnishing", [])

            if not all([height, length, width, norm_id]):
                return JsonResponse({"error": _("Missing required data.")}, status=400)

            norm = get_object_or_404(Norm, id=norm_id)

            def parse_surfaces(
                surface_data: list[dict[str, Any]]
            ) -> list[dict[str, Any]]:
                surfaces = []
                for entry in surface_data:
                    material_id = entry.get("material_id")
                    area = entry.get("area_m2")
                    if material_id is None or area is None:
                        continue
                    material = get_object_or_404(Material, id=material_id)
                    surfaces.append({"material": material, "area_m2": area})
                return surfaces

            construction_surfaces = parse_surfaces(construction_data)
            furnishing_elements = parse_surfaces(furnishing_data)

            calculator = AcousticCalculator(
                norm=norm,
                room_dimensions={"width": width, "length": length, "height": height},
                construction_surfaces=construction_surfaces,
                furnishing_elements=furnishing_elements,
                freq_band=frequency,
            )

            results = calculator.result()

            return JsonResponse(
                {
                    "volume_m3": results["volume_m3"],
                    "surface_area_m2": results["surface_area_m2"],
                    "absorption_achieved": results["absorption_achieved"],
                    "absorption_required": results["absorption_required"],
                    "reverberation_time_s": results["reverberation_time_s"],
                    "estimated_sti": results["estimated_sti"],
                    "norm_passed": results["norm_passed"],
                    "message": _("Calculation completed successfully."),
                }
            )

        except Material.DoesNotExist:
            return JsonResponse(
                {"error": _("One or more materials not found.")}, status=404
            )
        except Norm.DoesNotExist:
            return JsonResponse({"error": _("Norm not found.")}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
