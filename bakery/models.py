from django.db import models

from authentication.models import User


class PromotionModel(models.Model):
    description = models.CharField(max_length=150)
    discount = models.FloatField()


class CategoryModel(models.Model):
    title = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)


class ProductModel(models.Model):
    title = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/')
    upload_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.OneToOneField(CategoryModel, on_delete=models.CASCADE)
    promotions = models.ManyToManyField(PromotionModel)


class OrderModel(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLATE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLATE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    create_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()


class AddressModel(models.Model):
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    customer = models.OneToOneField(User, on_delete=models.CASCADE)


class CartModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
