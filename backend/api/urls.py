from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import TicketList, TicketDetail, CategoryList, CategoryDetail
from drf_yasg import openapi
from rest_framework import permissions

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Zentro API",
        default_version='v1',
        description="Documentação da API do sistema de chamados Zentro",
        contact=openapi.Contact(email="dudu12310@hotmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tickets/', TicketList.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetail.as_view(), name='ticket-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),  
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]