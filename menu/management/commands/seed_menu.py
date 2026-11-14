
from decimal import Decimal

from django.core.management.base import BaseCommand
from menu.models import Category, MenuItem


class Command(BaseCommand):
    help = "Add the Indian Cafe printed menu to Caf-Nexa"

    MENU = {
        "Sandwiches": [
            ("Potato Cheese Sandwich", 60),
            ("Vegetable Sandwich", 55),
            ("Vegetable Cheese Sandwich", 65),
            ("Vegetable Corn Sandwich", 65),
            ("Vegetable Corn Cheese Sandwich", 75),
            ("Pasta Sandwich", 60),
            ("Pasta Cheese Sandwich", 70),
            ("Mexican Sandwich", 65),
            ("Mexican Cheese Sandwich", 75),
            ("Paneer Sandwich", 70),
            ("Paneer Cheese Sandwich", 80),
            ("Veg Club Sandwich", 110),
        ],

        "Hot Dogs": [
            ("Veg Hot Dog", 35),
            ("Veg Cheese Hot Dog", 45),
            ("Tikki Hot Dog", 55),
            ("Cheese Tikki Hot Dog", 65),
            ("Panner/Corn Hot Dog", 0),
        ],

        "Crushers": [
            ("Green Apple", 45),
            ("Litchi", 45),
            ("Mango", 45),
            ("Watermelon", 45),
            ("Strawberry", 45),
            ("Orange", 45),
            ("Black Current", 45),
            ("Masala Soda", 45),
            ("Lemon Soda", 45),
            ("Masala Thumsup", 50),
            ("Orange Juice", 45),
        ],

        "Shakes": [
            ("Chocolate Shake", 60),
            ("Mango Shake", 60),
            ("Strawberry Shake", 60),
            ("Butter Scotch Shake", 60),
            ("Pineapple Shake", 60),
            ("Banana Shake", 60),
            ("Watermelon Shake", 60),
            ("Kit-Kat Shake", 70),
            ("Orea Shake", 70),
            ("Cold Coffee", 70),
            ("Ice-Cream", 15),
        ],

        "Maggi": [
            ("Vegetable Maggi", 40),
            ("Veg Cheese Maggi", 50),
            ("Veg Corn Maggi", 50),
            ("Veg Corn Cheese Maggi", 60),
            ("Baked Maggie", 110),
        ],

        "Juices": [
            ("Mosambi Juice", 0),
            ("Anar Juice", 0),
            ("Orange Juice", 0),
            ("Pineapple Juice", 0),
            ("Beat Juice", 0),
        ],

        "Snacks": [
            ("French Fries", 50),
            ("Smiles (4 pcs)", 40),
            ("Momo (5 pcs)", 50),
        ],

        "Momos": [
            ("Ferrari Momo", 0),
            ("Steam Momo", 0),
        ],

        "Pizza": [
            ("Plain Cheese Pizza", 80),
            ("Veg Cheese Pizza", 90),
            ("Corn/Paneer Pizza", 100),
            ("Pasta Cheese Pizza", 100),
            ("Classic Italian Pizza", 110),
            ("Mix Pizza", 110),
            ("Cheese Burst Pizza", 120),
            ("Special Pizza", 160),
        ],

        "Burgers": [
            ("Veg Burger", 55),
            ("Cheese Burger", 65),
            ("Paneer Burger", 75),
            ("Paneer Cheese Burger", 85),
            ("Mexican Burger", 85),
            ("Mexican Cheese Burger", 95),
        ],

        "Pasta": [
            ("Red Sauce Pasta", 90),
            ("White Sauce Pasta", 90),
            ("Mix Sauce Pasta", 100),
            ("Special Pasta", 110),
            ("Baked Pasta", 140),
        ],
    }

    def handle(self, *args, **options):
        added_categories = 0
        added_items = 0

        for category_name, products in self.MENU.items():

            category, created = Category.objects.get_or_create(
                name=category_name
            )

            if created:
                added_categories += 1

            for item_name, price in products:

                _, created = MenuItem.objects.get_or_create(
                    category=category,
                    name=item_name,
                    defaults={
                        "price": Decimal(str(price)),
                        "is_available": True,
                    },
                )

                if created:
                    added_items += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Menu setup complete! "
                f"{added_categories} categories and "
                f"{added_items} new items added."
            )
        )
