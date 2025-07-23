from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from django.utils.html import format_html
from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import (
    Product, Category, Cart, CartItem, Order
)
from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    UserSerializer  # ← You likely have this already created for signup/login
)

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug']
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity += quantity if not created else 0
        cart_item.quantity = quantity if created else cart_item.quantity
        cart_item.save()

        cart.update_total()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.data.get('quantity', 0))

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        cart_item.cart.update_total()
        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)

        if not cart.items.exists():
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user,
            total=cart.total_price
        )
        order.items.set(cart.items.all())
        order.save()

        cart.items.all().delete()
        cart.update_total()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
class UserListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.values('id', 'email', 'is_staff', 'is_superuser', 'is_active')
        return Response(users)
class AllOrdersView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, order_id):
        status_value = request.data.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = status_value
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_orders = Order.objects.count()
        revenue = Order.objects.aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
        orders_by_status = Order.objects.values('status').annotate(count=Count('id'))

        return Response({
            'total_users': total_users,
            'total_orders': total_orders,
            'total_revenue': revenue,
            'orders_by_status': orders_by_status,
        })
