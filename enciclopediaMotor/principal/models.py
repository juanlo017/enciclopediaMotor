from django.db import models


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FuelType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class GearboxType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100)
    price = models.IntegerField()
    warranty = models.IntegerField()
    year = models.IntegerField()
    num_doors = models.IntegerField()
    num_seats = models.IntegerField()
    cc = models.IntegerField()
    cv = models.IntegerField()
    color = models.CharField(max_length=100)

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    gearbox_type = models.ForeignKey(GearboxType, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name
