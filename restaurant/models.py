from django.db import models


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True)
    reservation_date = models.DateField()
    reservation_hour = models.SmallIntegerField(default=10)
    numberOfPeople = models.SmallIntegerField(null=True)

    def __str__(self):
        return f"{self.first_name} - {self.phone_number}"


# Add code to create Menu model
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=False)
    menu_item_description = models.TextField(max_length=1000, default="")
    image = models.ImageField(
        upload_to="restaurant/static/img/menu-tems", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Configuration(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.key
