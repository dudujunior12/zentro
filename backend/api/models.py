from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tickets(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('High', 'High'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Open', choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, default='Normal', choices=PRIORITY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"