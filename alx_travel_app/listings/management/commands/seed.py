from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        sample_listings = [
            {"title": "Beachside Villa", "description": "A beautiful villa by the beach.", "price_per_night": 150.00, "location": "Lagos"},
            {"title": "Mountain Cabin", "description": "Cozy cabin in the mountains.", "price_per_night": 90.00, "location": "Jos"},
            {"title": "City Apartment", "description": "Modern apartment in the city center.", "price_per_night": 120.00, "location": "Abuja"},
        ]

        for listing_data in sample_listings:
            obj, created = Listing.objects.get_or_create(**listing_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created listing: {obj.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Listing already exists: {obj.title}"))

        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
