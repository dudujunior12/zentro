from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        from django.contrib.auth.models import Group

        def create_groups(sender, **kwargs):
            grupos = ['Requesters', 'Technicians', 'Admins']
            for grupo_nome in grupos:
                Group.objects.get_or_create(name=grupo_nome)

        post_migrate.connect(create_groups, sender=self)
