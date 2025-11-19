import os
import random
import django
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arruma.settings')
django.setup()

# Import models after Django setup
from user.models import User, Company

def create_service_providers(count=10):
    fake = Faker('pt_BR')
    
    service_types = [
        'Eletricista', 'Pintor', 'Jardineiro', 'Diarista', 'Encanador',
        'Marceneiro', 'Pedreiro', 'Arquiteto', 'Dedetizador', 'Montador de Móveis'
    ]
    
    cities = [
        'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 
        'Curitiba', 'Brasília', 'Salvador', 'Recife', 'Fortaleza', 'Manaus'
    ]
    
    for _ in range(count):
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
                password='senha123',
                first_name=first_name,
                last_name=last_name,
                name=f"{first_name} {last_name}",
                is_company=True
            )
            
            # Create company profile
            service = random.choice(service_types)
            city = random.choice(cities)
            company_name = f"{service} {fake.company_suffix()}"
            
            # Generate a numeric phone number (only digits)
            phone_number = ''.join(filter(str.isdigit, fake.phone_number()))
            
            Company.objects.create(
                user=user,
                job=service,
                city=city,
                tel=int(phone_number[:15]),  # Ensure it's an integer and not too long
                cnpj=fake.random_number(digits=8)
            )
            
            print(f'✅ Created: {company_name} ({city})')
            
        except Exception as e:
            print(f'❌ Error: {str(e)}')

if __name__ == "__main__":
    num_providers = input("How many service providers would you like to create? (default: 10): ")
    try:
        num_providers = int(num_providers) if num_providers.strip() else 10
        create_service_providers(num_providers)
        print("\n✅ Done! Service providers created successfully!")
    except ValueError:
        print("Please enter a valid number.")
