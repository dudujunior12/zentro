from rest_framework import serializers
from .models import Categories, Tickets
from django.contrib.auth.models import User

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class TicketsSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Tickets
        fields = '__all__'
        read_only_fields = ('created_by',)