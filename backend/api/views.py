from django.shortcuts import render
from .serializers import CategoriesSerializer, TicketsSerializer
from .models import Categories, Tickets
from rest_framework import generics
from .permissions import IsAdministrador, IsOwnerOrAssignedOrAdmin
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TicketList(generics.ListCreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.groups.filter(name='Administrator').exists():
            return Tickets.objects.all()
        elif user.groups.filter(name='Technician').exists():
            return Tickets.objects.filter(assigned_to__in=[user, None])
        else:
            return Tickets.objects.filter(created_by=user)

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = [IsOwnerOrAssignedOrAdmin]

class CategoryList(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdministrador]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdministrador]