# import pytest
# from rest_framework.test import APIClient

import pytest
from rest_framework.test import APIClient
from core.models import Product, Category, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_add_to_cart_and_update_quantity():
    client = APIClient()

    # Create normal user
    user = User.objects.create_user(email="user@example.com", password="userpass")
    client.force_authenticate(user=user)

    # Create product
    category = Category.objects.create(name="Books", slug="books")
    product = Product.objects.create(name="Django Book", description="Learn Django", price=500, stock=20, category=category)

    # Add to cart
    response = client.post("/api/cart/add/", {
        "product_id": product.id,
        "quantity": 2
    })
    assert response.status_code == 200
    assert response.data["total_price"] == "1000.00"

    # Update cart item quantity
    cart_item = CartItem.objects.first()
    response = client.put(f"/api/cart/item/{cart_item.id}/", {
        "quantity": 3
    })
    assert response.status_code == 200
    assert response.data["total_price"] == "1500.00"
