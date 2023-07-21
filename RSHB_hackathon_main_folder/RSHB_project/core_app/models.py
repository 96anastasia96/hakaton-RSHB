from django.db import models

# Create your models here.


class Bank(models.Model):  # Класс банка
    name = models.CharField(max_length=50)
    bank_account = models.IntegerField()  # Денежный счёт


man = 'm'
woman = 'w'
genders = [(man, 'Мужской'), (woman, 'Женский')]


class Player(models.Model):  # Класс игрока
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=genders, default=None)
    bank_account = models.IntegerField()
    issued_loan = models.BooleanField()  # Факт оформления кредита в банке
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)


class Shop(models.Model):  # Класс магазина
    name = models.CharField(max_length=50)


class Equipment(models.Model):  # Класс используемой игроком техники
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    in_players_inventory = models.BooleanField()  # Факт наличия в инвентаре игрока
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class Plant(models.Model):  # Класс растений
    name = models.CharField(max_length=50)
    ripeness = models.CharField(max_length=50)

