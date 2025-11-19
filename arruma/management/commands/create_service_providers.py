import random
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from django.db import transaction

# Import the Company model directly from user.models
from user.models import Company

# Get the User model
User = get_user_model()

class Command(BaseCommand):
    help = 'Creates multiple service providers with random data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of service providers to create')

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker('pt_BR')
        count = options['count']
        
        # Service types that match your business
        service_types = [
            'Eletricista', 'Pintor', 'Jardineiro', 'Diarista', 'Encanador',
            'Marceneiro', 'Pedreiro', 'Arquiteto', 'Dedetizador', 'Montador de Móveis',
            'Técnico em Ar Condicionado', 'Chaveiro', 'Vidraceiro', 'Gesseiro', 'Azulejista'
        ]
        
        cities = [
            'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 
            'Curitiba', 'Brasília', 'Salvador', 'Recife', 'Fortaleza', 'Manaus'
        ]
        
        for i in range(count):
            try:
                # Create user data
                first_name = fake.first_name()
                last_name = fake.last_name()
                username = f"{first_name.lower()}.{last_name.lower()}"
                email = f"{username}@example.com"
                
                # Create user with company role
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='senha123',  # Default password
                    first_name=first_name,
                    last_name=last_name,
                    name=f"{first_name} {last_name}",
                    is_company=True
                )
                
                # Create company profile
                service = random.choice(service_types)
                city = random.choice(cities)
                company_name = f"{service} {fake.company_suffix()}"
                
                Company.objects.create(
                    user=user,
                    job=service,
                    city=city,
                    tel=fake.phone_number(),
                    cnpj=fake.random_number(digits=8)
                )
                
                self.stdout.write(self.style.SUCCESS(f'Created service provider: {company_name} ({city})'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating service provider: {str(e)}'))
