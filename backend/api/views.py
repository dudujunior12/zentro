from django.shortcuts import render
from .serializers import CategoriesSerializer, TicketsSerializer
from .models import Categories, Tickets
from rest_framework import generics

# Create your views here.
class TicketList(generics.ListCreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    
class CategoryList(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer