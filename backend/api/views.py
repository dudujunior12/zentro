from django.shortcuts import render
from .serializers import CategoriesSerializer, TicketsSerializer
from .models import Categories, Tickets
from rest_framework import generics
from .permissions import IsAdministrador, IsOwnerOrAssignedOrAdmin
from rest_framework.permissions import IsAuthenticated
import logging
from django.core.cache import cache
from rest_framework.response import Response


logger = logging.getLogger('api') 
# Create your views here.
class TicketList(generics.ListCreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket = serializer.save(created_by=self.request.user)
        logger.info(f"User {self.request.user} created ticket ID {ticket.id} with title '{ticket.title}'")
        
    def list(self, request, *args, **kwargs):
        logger.debug(f"User {request.user} requested a ticket list")
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        base_queryset = Tickets.objects.all().order_by('-created_at')
        
        if user.is_staff or user.groups.filter(name='Admins').exists():
            return base_queryset
        elif user.groups.filter(name='Technicians').exists():
            return base_queryset.filter(assigned_to__in=[user, None])
        else:
            return base_queryset.filter(created_by=user)

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = [IsOwnerOrAssignedOrAdmin]
    
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"User {request.user} retrieved ticket ID {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"User {request.user} updated ticket ID {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"User {request.user} deleted ticket ID {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

class CategoryList(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdministrador]
    
    def list(self, request, *args, **kwargs):
        logger.debug(f"User {request.user} listed all categories")
        cached = cache.get('categories_list')
        if cached:
            return Response(cached)
        
        response = super().list(request, *args, **kwargs)
        cache.set('categories_list', response.data, timeout=300)
        return response

    def create(self, request, *args, **kwargs):
        logger.info(f"User {request.user} created a new category: {request.data.get('name')}")
        response = super().create(request, *args, **kwargs)
        cache.delete('categories_list')
        return response

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdministrador]
    
    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"User {request.user} retrieved category ID {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"User {request.user} updated category ID {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"User {request.user} deleted category ID {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)