from typing import Any

import stripe
from django.conf import settings
from plans.models import Plan


class StripeService:
    def __init__(self) -> None:
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_checkout_session(self, plan: Plan, user_email: str) -> Any:
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "pln",
                        "product_data": {"name": plan.name},
                        "unit_amount": int(plan.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            customer_email=user_email,
            success_url=f"{settings.STRIPE_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=settings.STRIPE_CANCEL_URL,
            metadata={"plan_id": str(plan.id)},
        )
