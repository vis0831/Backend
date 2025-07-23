import pytest
from rest_framework.test import APIClient
from core.models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_checkout_and_order_history():
    client = APIClient()

    # Create user and login
    user = User.objects.create_user(email="order@example.com", password="test123")
    client.force_authenticate(user=user)

    # Create category and product
    category = Category.objects.create(name="Mobiles", slug="mobiles")
    product = Product.objects.create(
        name="iPhone",
        description="Apple phone",
        price=60000,
        stock=5,
        category=category
    )

    # Add to cart
    client.post("/api/cart/add/", {
        "product_id": product.id,
        "quantity": 1
    })

    # Checkout
    response = client.post("/api/checkout/")
    assert response.status_code == 201
    assert response.data["total"] == "60000.00"

    # Order history (paginated)
    response = client.get("/api/orders/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["status"] == "PENDING"