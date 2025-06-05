import re
from decimal import Decimal

from calculations.models import Material
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import materials from SQL dump file"

    def handle(self, *args, **kwargs):
        SQL_DUMP_PATH = "calculations/acoustic_database.sql"
        materials_to_create = []

        with open(SQL_DUMP_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(
            r"COPY public.materials \(.*?\) FROM stdin;(.*?)\\.", content, re.S
        )

        if match:
            materials_data = match.group(1).strip().split("\n")

            for line in materials_data:
                fields = line.split("\t")
                if len(fields) != 8:
                    continue

                (
                    _,
                    material_type,
                    name,
                    freq_125,
                    freq_250,
                    freq_500,
                    freq_1000,
                    freq_2000,
                    freq_4000,
                ) = fields

                material = Material(
                    type=material_type.strip(),
                    name=name.strip(),
                    freq_125=Decimal(freq_125),
                    freq_250=Decimal(freq_250),
                    freq_500=Decimal(freq_500),
                    freq_1000=Decimal(freq_1000),
                    freq_2000=Decimal(freq_2000),
                    freq_4000=Decimal(freq_4000),
                )

                materials_to_create.append(material)

        Material.objects.bulk_create(materials_to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {len(materials_to_create)} materials."
            )
        )
