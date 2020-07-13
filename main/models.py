from django.db import models


class MyManager(models.Manager):

    def create(self, customer, item, total, quantity, date):

        try:
            stone = Stone.objects.get(name=item)

        except Stone.DoesNotExist:
            stone = Stone(name=item).save()

        try:
            buyer = Buyer.objects.get(username=customer)
            buyer.spent_money += total
            if stone in buyer.gems.all():
                buyer.save()
            else:
                buyer.gems.add(stone)
        except Buyer.DoesNotExist:
            buyer = Buyer(username=customer, spent_money=total)
            buyer.save()
            buyer.gems.add(stone)
            buyer.save()

        purchase = Purchase(customer=customer, item=item, total=total, quantity=quantity, date=date, buyer=buyer)
        purchase.save()

        return purchase


class Stone(models.Model):
    name = models.TextField('Название камня')

    def __str__(self):
        return self.name


class Buyer(models.Model):
    """Клиенты"""
    username = models.TextField("Логин")
    spent_money = models.DecimalField("Cумма", max_digits=9, decimal_places=2)
    gems = models.ManyToManyField(Stone)

    def __str__(self):
        return self.username



class Purchase(models.Model):
    """Покупки"""
    customer = models.TextField("Логин")
    item = models.TextField("Наименование товара")
    total = models.DecimalField("Сумма сделки", max_digits=9, decimal_places=2)
    quantity = models.DecimalField("Количество товара", max_digits=9, decimal_places=0)
    date = models.DateTimeField("Время")
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    objects = MyManager()

    def __str__(self):
        return self.customer

# Create your models here.
