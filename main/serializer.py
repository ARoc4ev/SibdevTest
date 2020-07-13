from rest_framework import serializers
from .models import Purchase, Buyer, Stone



class GetSerializersList(serializers.ModelSerializer):
    gems = serializers.SerializerMethodField('gems_dict')


    def gems_dict(self, obj):
        buyer = Buyer.objects.all().order_by('-spent_money')[:5]
        gemss = dict()
        for i in obj.gems.all():
            for y in buyer:
                if obj.id != y.id:
                    for gems in y.gems.all():
                        if i == gems:
                            gemss[i.id] = i.name

        return gemss

    # def gems_dict_test(self, obj):
    #     gemss = dict()
    #     for i in obj.gems.all():
    #         gemss[i.id] = i.name
    #     return gemss

    class Meta:
        model = Buyer
        fields = ('username', 'spent_money', 'gems',)


class SerializersList(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('customer', 'item', "total", 'quantity', 'date')


class SerializersCreate(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        # list_serializer_class = SerializersCreateList
        fields = ('customer', 'item', "total", 'quantity', 'date')
