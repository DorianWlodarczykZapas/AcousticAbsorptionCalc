# Generated by Django 5.1.7 on 2025-06-01 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        help_text="Material category (e.g., ceiling panel, wall absorber)",
                        max_length=100,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("freq_125", models.DecimalField(decimal_places=2, max_digits=4)),
                ("freq_250", models.DecimalField(decimal_places=2, max_digits=4)),
                ("freq_500", models.DecimalField(decimal_places=2, max_digits=4)),
                ("freq_1000", models.DecimalField(decimal_places=2, max_digits=4)),
                ("freq_2000", models.DecimalField(decimal_places=2, max_digits=4)),
                ("freq_4000", models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name="Norm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "application_type",
                    models.CharField(
                        choices=[
                            ("1", "Height-dependent"),
                            ("2", "No dependency"),
                            ("3", "Volume-dependent"),
                            ("4", "Speech Transmission Index"),
                        ],
                        default="2",
                        max_length=2,
                    ),
                ),
                (
                    "rt_max",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Maximum allowed reverberation time in seconds (T ≤ ...)",
                        max_digits=5,
                        null=True,
                    ),
                ),
                (
                    "sti_min",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Minimum allowed STI value (STI ≥ ...)",
                        max_digits=5,
                        null=True,
                    ),
                ),
                (
                    "absorption_min_factor",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Minimum required sound absorption as a factor of surface area (A ≥ x × S)",
                        max_digits=5,
                        null=True,
                    ),
                ),
                ("slug", models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Calculation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "room_height",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "room_volume",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "room_surface_area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "reverberation_time",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "sti",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "required_absorption",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "achieved_absorption",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("is_within_norm", models.BooleanField(null=True)),
                (
                    "norm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calculations.norm",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SurfaceElement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "area_m2",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Surface area of the element in m²",
                        max_digits=10,
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        help_text="Where this surface is located (e.g., ceiling, wall A)",
                        max_length=100,
                    ),
                ),
                (
                    "calculation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="surfaces",
                        to="calculations.calculation",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="calculations.material",
                    ),
                ),
            ],
        ),
    ]
