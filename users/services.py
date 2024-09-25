import requests
import stripe
from rest_framework import status
from config import settings


def get_session(session_id):
    """Получает сессию из Stripe"""
    url = "https://api.stripe.com/v1/checkout/sessions/"
    api_key = settings.STRIPE_API_KEY

    response = requests.get(f"{url}{session_id}", auth=(api_key, ""), timeout=10)

    if response.status_code == status.HTTP_200_OK:
        return response.json()
    return


def create_product(name, amount):
    stripe.api_key = settings.STRIPE_API_KEY

    return stripe.Product.create(
        name=name,
        default_price_data={
            "currency": "rub",
            "unit_amount": amount * 100,
        },
    )


def create_session(product):
    stripe.api_key = settings.STRIPE_API_KEY

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": product.get("default_price"), "quantity": 1}],
        mode="payment",
    )

    return session.get("url"), session.get("id")
