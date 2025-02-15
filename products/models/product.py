from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField(default=0)  #bazadagi qoldiq


    def __str__(self):
        return self.name

# bazada mahsulot bor yoki yo'qligini tekshirish
    def is_in_stock(self):
        return self.stock > 0

#bazadan olish
    def reduce_stock(self, quantity):
        if quantity > self.stock:
            return False
        self.stock -= quantity
        self.save()
        return True

#bazaga tovar qo'shish
    def increase_stock(self, amount):
        self.stock += amount
        self.save()
        return True
