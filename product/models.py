from django.db import models
from users.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'


class Product(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name_plural = 'products'


class Image(BaseModel):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'image'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    message = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='comments/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')


class Attribute(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class AttributeValue(BaseModel):
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.value


class ProductAttribute(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
