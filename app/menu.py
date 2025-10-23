"""Menu data and logic for NoPickles MVP"""

from typing import List, Dict
from app.models import MenuItem

# Sample menu data
MENU_DATA = [
    # Burgers
    MenuItem(
        id="burger_classic",
        name="Classic Burger",
        category="burgers",
        price=8.99,
        description="Beef patty, lettuce, tomato, onion, pickles, and special sauce"
    ),
    MenuItem(
        id="burger_cheese",
        name="Cheeseburger",
        category="burgers",
        price=9.99,
        description="Classic burger with melted cheddar cheese"
    ),
    MenuItem(
        id="burger_double",
        name="Double Burger",
        category="burgers",
        price=12.99,
        description="Two beef patties with all the fixings"
    ),
    MenuItem(
        id="burger_veggie",
        name="Veggie Burger",
        category="burgers",
        price=9.49,
        description="Plant-based patty with fresh vegetables"
    ),
    
    # Sides
    MenuItem(
        id="fries_regular",
        name="French Fries",
        category="sides",
        price=3.49,
        description="Crispy golden french fries"
    ),
    MenuItem(
        id="fries_loaded",
        name="Loaded Fries",
        category="sides",
        price=5.99,
        description="Fries topped with cheese, bacon, and sour cream"
    ),
    MenuItem(
        id="onion_rings",
        name="Onion Rings",
        category="sides",
        price=4.49,
        description="Crispy battered onion rings"
    ),
    MenuItem(
        id="salad",
        name="Garden Salad",
        category="sides",
        price=4.99,
        description="Fresh mixed greens with your choice of dressing"
    ),
    
    # Drinks
    MenuItem(
        id="drink_cola",
        name="Cola",
        category="drinks",
        price=2.49,
        description="Classic cola soft drink"
    ),
    MenuItem(
        id="drink_sprite",
        name="Lemon-Lime Soda",
        category="drinks",
        price=2.49,
        description="Refreshing lemon-lime soda"
    ),
    MenuItem(
        id="drink_water",
        name="Bottled Water",
        category="drinks",
        price=1.99,
        description="Pure bottled water"
    ),
    MenuItem(
        id="drink_shake",
        name="Milkshake",
        category="drinks",
        price=4.99,
        description="Creamy milkshake - vanilla, chocolate, or strawberry"
    ),
    
    # Desserts
    MenuItem(
        id="dessert_pie",
        name="Apple Pie",
        category="desserts",
        price=3.49,
        description="Warm apple pie with cinnamon"
    ),
    MenuItem(
        id="dessert_sundae",
        name="Ice Cream Sundae",
        category="desserts",
        price=3.99,
        description="Vanilla ice cream with chocolate sauce and cherry"
    ),
]

# Create lookup dictionaries
MENU_BY_ID = {item.id: item for item in MENU_DATA}
MENU_BY_CATEGORY = {}
for item in MENU_DATA:
    if item.category not in MENU_BY_CATEGORY:
        MENU_BY_CATEGORY[item.category] = []
    MENU_BY_CATEGORY[item.category].append(item)


def get_menu() -> Dict:
    """Get the complete menu organized by category"""
    return {
        "categories": list(MENU_BY_CATEGORY.keys()),
        "items_by_category": {cat: [item.dict() for item in items] 
                              for cat, items in MENU_BY_CATEGORY.items()}
    }


def get_menu_items() -> List[MenuItem]:
    """Get all menu items as a list"""
    return MENU_DATA


def find_item_by_name(query: str) -> MenuItem:
    """Find a menu item by partial name match"""
    query_lower = query.lower()
    
    # Try exact match first
    for item in MENU_DATA:
        if item.name.lower() == query_lower:
            return item
    
    # Try partial match
    for item in MENU_DATA:
        if query_lower in item.name.lower():
            return item
    
    # Try category-based keywords
    keywords = {
        "burger": "burger_classic",
        "fries": "fries_regular",
        "drink": "drink_cola",
        "soda": "drink_cola",
        "water": "drink_water",
        "shake": "drink_shake",
        "salad": "salad",
        "onion": "onion_rings",
        "dessert": "dessert_pie",
        "pie": "dessert_pie",
        "ice cream": "dessert_sundae",
    }
    
    for keyword, item_id in keywords.items():
        if keyword in query_lower:
            return MENU_BY_ID.get(item_id)
    
    return None


def get_item_by_id(item_id: str) -> MenuItem:
    """Get a specific menu item by ID"""
    return MENU_BY_ID.get(item_id)


def get_recommendations(current_order_items: List) -> List[str]:
    """Get smart recommendations based on current order"""
    suggestions = []
    
    # Extract categories of current items
    current_categories = set()
    for item in current_order_items:
        menu_item = MENU_BY_ID.get(item.menu_item_id)
        if menu_item:
            current_categories.add(menu_item.category)
    
    # Suggest sides if they have a burger but no sides
    if "burgers" in current_categories and "sides" not in current_categories:
        suggestions.append("How about some fries to go with that?")
    
    # Suggest drinks if they don't have one
    if "drinks" not in current_categories:
        suggestions.append("Would you like a drink?")
    
    # Suggest dessert if order is substantial
    if len(current_order_items) >= 2 and "desserts" not in current_categories:
        suggestions.append("Don't forget dessert! Our apple pie is delicious.")
    
    return suggestions
