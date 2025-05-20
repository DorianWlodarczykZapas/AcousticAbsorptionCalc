from decimal import Decimal

from .models import Norm, NormCalculationType


class NormComplianceChecker:
    def __init__(
        self, norm: Norm, height: float, volume: float, sti: float | None = None
    ):
        self.norm = norm
        self.height = height
        self.volume = volume
        self.sti = sti

    def is_within(self, rt: Decimal) -> bool:
        try:
            if self.norm.application_type == NormCalculationType.HEIGHT:
                req = self.norm.norms_reverb_time_height_req
                if self.height < 4:
                    return rt <= Decimal(req.h_less_4)
                elif 4 <= self.height <= 16:
                    return rt <= Decimal(req.h_between_4_16)
                else:
                    return rt <= Decimal(req.h_more_16)

            elif self.norm.application_type == NormCalculationType.VOLUME:
                req = self.norm.norms_reverb_time_volume_req
                v = self.volume
                if v < 120:
                    return rt <= Decimal(req.less_120)
                elif v < 250:
                    return rt <= Decimal(req.between_120_250)
                elif v < 500:
                    return rt <= Decimal(req.between_250_500)
                elif v < 1000:
                    return rt <= Decimal(req.between_500_1000)
                else:
                    return rt <= Decimal(req.more_1000)

            elif self.norm.application_type == NormCalculationType.STI:
                return self.sti is not None and self.sti >= Decimal("0.6")

            elif self.norm.application_type == NormCalculationType.NONE:
                req = self.norm.norms_reverb_time_no_req
                return rt <= Decimal(req.no_cubature_req)

        except AttributeError:
            return False

        return False
