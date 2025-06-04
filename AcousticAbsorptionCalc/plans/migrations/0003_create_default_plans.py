from django.db import migrations


def create_default_plans(apps, schema_editor):
    Plan = apps.get_model("plans", "Plan")

    plans = [
        {
            "name": "Base Plan",
            "type": 1,
            "description": "Basic features for individuals.",
            "price": 49.99,
            "billing_period": "30 days",
            "max_projects": 5,
            "max_rooms_per_project": 20,
            "advanced_features_enabled": False,
        },
        {
            "name": "Premium Plan",
            "type": 2,
            "description": "Premium features for professionals.",
            "price": 99.99,
            "billing_period": "30 days",
            "max_projects": 20,
            "max_rooms_per_project": 100,
            "advanced_features_enabled": True,
        },
    ]

    for plan_data in plans:
        Plan.objects.get_or_create(
            type=plan_data["type"],
            defaults=plan_data,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_plans),
    ]
