from django.db import models
from django.http import JsonResponse
import json

# Create your models here.
# !!! Возможно, класс растений не нужен вовсе !!!


class Bank(models.Model):  # Класс банка
    name = models.CharField(max_length=50)
    bank_account = models.IntegerField(default=1000)  # Денежный счёт


class Shop(models.Model):  # Класс магазина
    name = models.CharField(max_length=50)


class Plant(models.Model):  # Класс растений
    name = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(default=1)


class Game(models.Model):  # Класс мини-игр
    name = models.CharField(max_length=50, unique=True)
    completed = models.BooleanField(default=False)
    result = models.IntegerField(default=0)

    def game_complete(self):  # TODO
        self.completed = True


class Equipment(models.Model):  # Класс используемой игроком техники
    name = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True if id == 1 else False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def become_available(self, game_id):  # Получение доступа к технике
        game = Game.objects.get(id=game_id)
        if game.id == self.id and game.completed:
            self.available = True
        self.save()

    def add_to_inventory(self, player_id=int):  # Добавление в инвентарь
        player = Player.objects.get(id=player_id)
        player.inventory.add(self.id)
        player.bank_accout -= self.price
        player.save()
        self.save()


man = 'Мужской'
woman = 'Женский'
genders = [(man, 'Мужской'), (woman, 'Женский')]


class Player(models.Model):  # Класс игрока
    name = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=genders, default=None)
    bank_account = models.IntegerField(default=100)  # Кошелёк игрока
    credit = models.IntegerField(default=0)  # Размер кредита
    inventory = tuple()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    equipment = models.ManyToManyField(Equipment, through='PlayerEquipment')
    game = models.ManyToManyField(Game, through='PlayerGame')

    def get_a_credit(self, credit=int):  # Оформление кредита
        self.credit = credit
        self.bank_account += credit
        self.save()

    def return_a_credit(self):  # Возврат кредита
        if self.bank_account >= self.credit:
            self.bank_account -= self.credit
            self.save()
        else:
            raise ValueError('На вашем счёте недостаточно средств для возврата кредита!')

    def add_to_bank_account(self, total=int):  # Добавление выйгранных монет в кошелёк игрока
        self.bank_account += total
        self.save()


class PlayerEquipment(models.Model):  # Промежуточный класс
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class PlayerGame(models.Model):  # Промежуточный класс
    equipment = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class RobotCard(models.Model):  # Класс карточек роботов
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    image_path = models.CharField(max_length=500)  # в БД сохраняется относительный путь до файла

    def get_data(self):  # возврат данных

        data = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_path': self.image_path,
        }
        return JsonResponse(data)