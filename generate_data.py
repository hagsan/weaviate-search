"""
Generate sample supermarket product data and insert into Weaviate.
"""
from weaviate_client import WeaviateClient
import random


def generate_sample_products():
    """Generate a list of sample supermarket products."""
    products = []
    
    # Product categories with sample products
    categories = {
        "Fruits": [
            {"name": "Organic Red Apples", "description": "Fresh, crisp organic red apples. Perfect for snacking or baking. Rich in fiber and vitamin C.", "price": 4.99, "brand": "Nature's Best"},
            {"name": "Bananas", "description": "Sweet, ripe bananas. Great source of potassium and natural energy. Perfect for breakfast or smoothies.", "price": 2.49, "brand": "Tropical Fresh"},
            {"name": "Strawberries", "description": "Juicy, sweet strawberries. Packed with antioxidants and vitamin C. Ideal for desserts or fresh eating.", "price": 5.99, "brand": "Berry Farm"},
            {"name": "Blueberries", "description": "Fresh blueberries loaded with antioxidants. Great for breakfast, baking, or as a healthy snack.", "price": 6.99, "brand": "Mountain Berry"},
            {"name": "Oranges", "description": "Sweet, juicy oranges. High in vitamin C. Perfect for fresh juice or eating whole.", "price": 3.99, "brand": "Citrus Grove"},
            {"name": "Mangoes", "description": "Sweet and juicy mangoes, perfect for smoothies or desserts. High in vitamin A and C.", "price": 5.49, "brand": "Tropical Orchard"},
            {"name": "Pineapple", "description": "Fresh pineapple with tangy sweetness. Great for grilling, smoothies, or fruit salads.", "price": 4.79, "brand": "Island Fresh"},
            {"name": "Grapes", "description": "Seedless table grapes. Sweet and crisp. Perfect for snacking or cheese boards.", "price": 4.59, "brand": "Vine Valley"},
            {"name": "Kiwi", "description": "Tangy kiwi fruits rich in vitamin C. Great for fruit salads or smoothies.", "price": 3.49, "brand": "Green Orchard"},
        ],
        "Vegetables": [
            {"name": "Organic Carrots", "description": "Fresh organic carrots. Crunchy and sweet. Rich in beta-carotene and vitamin A. Great for salads or cooking.", "price": 2.99, "brand": "Garden Fresh"},
            {"name": "Broccoli", "description": "Fresh green broccoli. High in vitamins C and K. Perfect for steaming, roasting, or stir-frying.", "price": 3.49, "brand": "Green Valley"},
            {"name": "Spinach", "description": "Fresh baby spinach leaves. Nutrient-dense leafy green. Perfect for salads, smoothies, or cooking.", "price": 3.99, "brand": "Leafy Greens"},
            {"name": "Tomatoes", "description": "Ripe, juicy tomatoes. Perfect for salads, sandwiches, or cooking. Rich in lycopene and vitamin C.", "price": 3.49, "brand": "Sunny Farms"},
            {"name": "Bell Peppers", "description": "Colorful bell peppers. Sweet and crisp. Great for salads, stir-fries, or roasting. High in vitamin C.", "price": 4.99, "brand": "Rainbow Produce"},
            {"name": "Cucumbers", "description": "Cool and crisp cucumbers. Great for salads, pickling, or snacking. Refreshing and hydrating.", "price": 2.79, "brand": "Green Meadow"},
            {"name": "Sweet Potatoes", "description": "Naturally sweet root vegetables rich in fiber and vitamin A. Perfect for roasting or mashing.", "price": 3.29, "brand": "Farmstead"},
            {"name": "Zucchini", "description": "Tender zucchini squash. Great for grilling, roasting, or spiralizing into noodles.", "price": 2.69, "brand": "Summer Fields"},
            {"name": "Cauliflower", "description": "Fresh cauliflower florets. Ideal for roasting, mashing, or low-carb rice substitutes.", "price": 3.59, "brand": "Garden Pride"},
        ],
        "Dairy": [
            {"name": "Whole Milk", "description": "Fresh whole milk. Rich and creamy. Great source of calcium and protein. Perfect for drinking or cooking.", "price": 4.49, "brand": "Farm Fresh Dairy"},
            {"name": "Greek Yogurt", "description": "Creamy Greek yogurt. High in protein and probiotics. Perfect for breakfast or as a healthy snack.", "price": 5.99, "brand": "Mediterranean Delight"},
            {"name": "Cheddar Cheese", "description": "Sharp cheddar cheese. Aged for rich flavor. Perfect for sandwiches, cooking, or cheese boards.", "price": 6.99, "brand": "Cheese Masters"},
            {"name": "Butter", "description": "Premium butter. Rich and creamy. Made from fresh cream. Perfect for baking and cooking.", "price": 4.99, "brand": "Golden Farms"},
            {"name": "Eggs", "description": "Farm-fresh eggs. Free-range and organic. High in protein. Perfect for breakfast or baking.", "price": 5.49, "brand": "Happy Hens"},
            {"name": "Mozzarella", "description": "Fresh mozzarella cheese. Soft and creamy. Ideal for pizzas, salads, and sandwiches.", "price": 6.49, "brand": "Italian Creamery"},
            {"name": "Almond Milk", "description": "Unsweetened almond milk. Dairy-free and vegan. Great for cereals, coffee, and smoothies.", "price": 3.99, "brand": "NutriChoice"},
            {"name": "Parmesan Cheese", "description": "Aged Parmesan cheese with a nutty flavor. Perfect for grating over pasta and salads.", "price": 7.99, "brand": "Rustic Dairy"},
            {"name": "Cottage Cheese", "description": "Low-fat cottage cheese. High in protein and great for snacks or salads.", "price": 4.79, "brand": "Valley Dairy"},
        ],
        "Meat": [
            {"name": "Ground Beef", "description": "Fresh ground beef. 80/20 lean to fat ratio. Perfect for burgers, meatballs, or tacos.", "price": 7.99, "brand": "Premium Meats"},
            {"name": "Chicken Breast", "description": "Boneless, skinless chicken breast. Lean protein source. Perfect for grilling, baking, or pan-frying.", "price": 8.99, "brand": "Farm Raised"},
            {"name": "Salmon Fillet", "description": "Fresh Atlantic salmon fillet. Rich in omega-3 fatty acids. Perfect for grilling or baking.", "price": 12.99, "brand": "Ocean Fresh"},
            {"name": "Pork Chops", "description": "Bone-in pork chops. Tender and flavorful. Perfect for grilling or pan-searing.", "price": 9.99, "brand": "Heritage Farms"},
            {"name": "Turkey Breast", "description": "Lean turkey breast. High in protein, low in fat. Perfect for sandwiches or roasting.", "price": 6.99, "brand": "Free Range"},
            {"name": "Bacon", "description": "Smoked pork bacon. Crispy and flavorful. Perfect for breakfast or sandwiches.", "price": 6.49, "brand": "Smoky Ridge"},
            {"name": "Shrimp", "description": "Raw peeled shrimp. Great for grilling, stir-fries, or pasta dishes. High in protein.", "price": 11.99, "brand": "Sea Harvest"},
            {"name": "Lamb Chops", "description": "Tender lamb chops. Rich flavor, ideal for grilling or roasting.", "price": 14.99, "brand": "Pasture Prime"},
            {"name": "Sliced Ham", "description": "Honey-glazed sliced ham. Ready for sandwiches or charcuterie boards.", "price": 7.49, "brand": "Cured Classics"},
        ],
        "Beverages": [
            {"name": "Orange Juice", "description": "Fresh squeezed orange juice. 100% pure. Rich in vitamin C. Perfect for breakfast.", "price": 4.99, "brand": "Sunshine Juice"},
            {"name": "Coffee Beans", "description": "Premium arabica coffee beans. Medium roast. Rich and smooth flavor. Perfect for morning brew.", "price": 12.99, "brand": "Mountain Roast"},
            {"name": "Green Tea", "description": "Organic green tea. High in antioxidants. Light and refreshing. Great for health and wellness.", "price": 5.99, "brand": "Zen Tea"},
            {"name": "Sparkling Water", "description": "Natural sparkling water. Zero calories, no sugar. Refreshing and hydrating.", "price": 3.99, "brand": "Pure Springs"},
            {"name": "Apple Juice", "description": "100% pure apple juice. No added sugar. Sweet and refreshing. Great for kids and adults.", "price": 4.49, "brand": "Orchard Fresh"},
            {"name": "Kombucha", "description": "Organic kombucha tea. Lightly effervescent with probiotics. Great for gut health.", "price": 4.29, "brand": "Culture Brew"},
            {"name": "Protein Shake", "description": "Ready-to-drink protein shake with 20g protein. Perfect post-workout beverage.", "price": 3.99, "brand": "PowerFuel"},
            {"name": "Coconut Water", "description": "Hydrating coconut water with natural electrolytes. Great post-workout drink.", "price": 3.49, "brand": "Island Hydrate"},
            {"name": "Herbal Tea", "description": "Caffeine-free herbal tea blend with chamomile and mint. Calming and soothing.", "price": 4.19, "brand": "Calm Leaf"},
        ],
        "Snacks": [
            {"name": "Potato Chips", "description": "Classic potato chips. Crispy and salty. Perfect for snacking or parties.", "price": 3.99, "brand": "Crunchy Delights"},
            {"name": "Dark Chocolate", "description": "Premium dark chocolate. 70% cocoa. Rich and indulgent. High in antioxidants.", "price": 5.99, "brand": "Cocoa Masters"},
            {"name": "Trail Mix", "description": "Mixed nuts, dried fruits, and chocolate chips. Energy-packed snack. Perfect for hiking or on-the-go.", "price": 6.99, "brand": "Nature's Trail"},
            {"name": "Granola Bars", "description": "Healthy granola bars. Made with oats, nuts, and honey. Great for breakfast or snacks.", "price": 4.99, "brand": "Healthy Bites"},
            {"name": "Popcorn", "description": "Light and fluffy popcorn. Low calorie snack. Perfect for movie nights or anytime snacking.", "price": 2.99, "brand": "Popped Fresh"},
            {"name": "Pretzels", "description": "Baked pretzel twists. Lightly salted and crunchy. Great for dipping or snacking.", "price": 3.49, "brand": "Twist & Crunch"},
            {"name": "Fruit Gummies", "description": "Assorted fruit gummies made with real fruit juice. Chewy and sweet.", "price": 2.99, "brand": "Sweet Orchard"},
            {"name": "Protein Bars", "description": "High-protein bars with nuts and whey. Ideal for post-workout or on-the-go snacks.", "price": 2.79, "brand": "Muscle Bite"},
            {"name": "Rice Cakes", "description": "Light and crunchy rice cakes. Low calorie base for spreads or snacks.", "price": 2.49, "brand": "Crispy Rice"},
        ],
        "Bakery": [
            {"name": "Whole Wheat Bread", "description": "Fresh baked whole wheat bread. High in fiber. Perfect for sandwiches or toast.", "price": 3.99, "brand": "Bakery Fresh"},
            {"name": "Croissants", "description": "Buttery, flaky croissants. Fresh baked daily. Perfect for breakfast or brunch.", "price": 4.99, "brand": "French Bakery"},
            {"name": "Bagels", "description": "Fresh bagels. Chewy and delicious. Perfect with cream cheese or as a sandwich.", "price": 4.49, "brand": "City Bakery"},
            {"name": "Chocolate Chip Cookies", "description": "Homemade chocolate chip cookies. Soft and chewy. Made with real chocolate chips.", "price": 5.99, "brand": "Sweet Treats"},
            {"name": "Sourdough Bread", "description": "Artisan sourdough bread. Tangy flavor, crispy crust. Perfect for sandwiches or toast.", "price": 5.49, "brand": "Artisan Bakers"},
            {"name": "Banana Bread", "description": "Moist banana bread with walnuts. Perfect with coffee or tea.", "price": 5.79, "brand": "Home Bakery"},
            {"name": "Muffins", "description": "Assorted muffins: blueberry, chocolate chip, and banana nut. Freshly baked.", "price": 5.29, "brand": "Morning Delight"},
            {"name": "Cinnamon Rolls", "description": "Soft cinnamon rolls with icing. Perfect warm breakfast treat.", "price": 6.49, "brand": "Sweet Swirl"},
            {"name": "Pita Bread", "description": "Fresh pita pockets. Great for sandwiches, dips, or wraps.", "price": 3.69, "brand": "Mediterranean Oven"},
        ],
        "Frozen": [
            {"name": "Frozen Peas", "description": "Frozen green peas. Flash frozen at peak freshness. Perfect for quick side dishes.", "price": 2.99, "brand": "Frozen Fresh"},
            {"name": "Ice Cream", "description": "Premium vanilla ice cream. Rich and creamy. Made with real vanilla beans.", "price": 6.99, "brand": "Creamy Delights"},
            {"name": "Frozen Pizza", "description": "Frozen margherita pizza. Ready to bake. Perfect for quick meals.", "price": 7.99, "brand": "Pizza Express"},
            {"name": "Frozen Berries", "description": "Mixed frozen berries. Great for smoothies, baking, or yogurt. Flash frozen for freshness.", "price": 4.99, "brand": "Berry Blend"},
            {"name": "Frozen Vegetables Mix", "description": "Mixed frozen vegetables. Broccoli, carrots, and peas. Perfect for stir-fries or sides.", "price": 3.49, "brand": "Garden Mix"},
            {"name": "Frozen Lasagna", "description": "Family-size cheese lasagna. Oven-ready meal for quick dinners.", "price": 9.99, "brand": "Italian Table"},
            {"name": "Veggie Burgers", "description": "Plant-based veggie burger patties. High in protein and fiber. Grill or pan-sear.", "price": 7.49, "brand": "Green Grill"},
            {"name": "Frozen Waffles", "description": "Toaster-ready waffles. Quick breakfast option. Serve with syrup or fruit.", "price": 3.99, "brand": "Morning Toast"},
            {"name": "Frozen Dumplings", "description": "Assorted vegetable dumplings. Steam or pan-fry for quick meals.", "price": 5.99, "brand": "Asian Kitchen"},
        ]
    }
    
    # Use local "image not available" image for all products
    image_not_available = "/static/image_not_available.png"
    
    for category, category_products in categories.items():
        for product in category_products:
            product_data = {
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "category": category,
                "brand": product["brand"],
                "image_url": image_not_available
            }
            products.append(product_data)
    
    return products


def main():
    """Main function to generate and insert sample data."""
    print("Initializing Weaviate client...")
    client = WeaviateClient()
    
    print("Creating schema...")
    client.initialize_schema()
    
    print("Generating sample products...")
    products = generate_sample_products()
    
    print(f"Inserting {len(products)} products into Weaviate...")
    client.insert_products(products)
    
    print("Sample data generation complete!")
    print(f"Total products inserted: {len(products)}")


if __name__ == "__main__":
    main()

