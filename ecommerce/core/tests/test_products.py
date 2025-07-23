import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from core.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_product_creation_and_listing():
    client = APIClient()

    # Create admin user
    admin = User.objects.create_superuser(email="admin@example.com", password="adminpass")
    client.force_authenticate(user=admin)

    # Create category
    category = Category.objects.create(name="Electronics", slug="electronics")

    # ✅ Create a valid image using PIL
    image_io = io.BytesIO()
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # red square
    image.save(image_io, format='PNG')
    image_io.seek(0)

    uploaded_image = SimpleUploadedFile(
        name="test_image.png",
        content=image_io.read(),
        content_type="image/png"
    )

    # Product data
    product_data = {
        "name": "Laptop",
        "description": "A great laptop",
        "price": "75000.00",
        "stock": 10,
        "category_id": category.id,
        "is_active": True,
        "image": uploaded_image,
    }

    # POST create product
    response = client.post("/api/products/", product_data, format='multipart')
    print("POST response data:", response.data)
    assert response.status_code == 201

    # GET all products
    response = client.get("/api/products/")
    print("GET response data:", response.data)
    assert response.status_code == 200
    assert response.data["count"] == 1
