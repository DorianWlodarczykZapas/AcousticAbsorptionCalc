from django.db import migrations


def create_trial_plan(apps, schema_editor):
    Plan = apps.get_model("plans", "Plan")

    Plan.objects.get_or_create(
        type=3,
        defaults={
            "name": "Trial Plan",
            "description": "7-day free trial plan",
            "price": 0.00,
            "billing_period": "7 days",
            "max_projects": 1,
            "max_rooms_per_project": 1,
            "advanced_features_enabled": False,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(create_trial_plan),
    ]
