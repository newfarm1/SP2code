from django.db import models

# class Items(models.Model):
#     item = models.CharField(max_length=100, primary_key=True)

# class Item(models.Model):
#     EAN = models.IntegerField(primary_key=True)
#     item = models.ForeignKey(Items.item, on_delete=models.CASCADE)
#     default_amount = models.IntegerField()

# class Dry_storage(models.Model):
#     EAN = models.ForeignKey(Item.EAN, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     expiredate = models.DateField()

# class Fridge_storage(models.Model):
#     EAN = models.ForeignKey(Item.EAN, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     expiredate = models.DateField()

# class Freezer_storage(models.Model):
#     EAN = models.ForeignKey(Item.EAN, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     expiredate = models.DateField()





# Create your models here.
