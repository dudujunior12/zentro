from rest_framework import serializers
from .models import Categories, Tickets

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'
        read_only_fields = ('created_by', 'assigned_to')