menu = {
    "Coffee": 2.50,
    "Tea": 2.00,
    "Sandwich": 5.00, 
    "Salad": 4.50,
    "Cake": 3.00,
}

set_menu = {
    "Set A1": {"items": ["Salad", "Coffee", "Egg Rice"], "price": 11.50},
    "Set B1": {"items": ["Chicken Rice", "Lemon Tea", "Vegetable"], "price": 10.50}
}

cart = []

def list_menu():
    print("\n--- Menu Items ---")
    for item, price in menu.items():
        print(f"  {item}: ${price:.2f}")

    print("\n--- Combo Sets ---")
    for set_name, details in set_menu.items():
        items_str = ", ".join(details["items"])
        print(f"  {set_name} (${details['price']:.2f}): {items_str}")

def find_item(item_name):
    if item_name in menu:
        return (item_name, menu[item_name])
    return (None, None)

def add_item():
    item_name = input("Enter the name of the new item: ").strip()
    if not item_name:
        print("Invalid name. Item not added.")
        return
    try:
        item_price = float(input("Enter the price of the new item: "))
        menu[item_name] = item_price
        print(f"{item_name} added to the menu (${item_price:.2f}).")
    except ValueError:
        print("Invalid price. Item not added.")

def delete_item():
    item_name = input("Enter the name of the item to delete: ").strip()
    if item_name in menu:
        del menu[item_name]
        print(f"{item_name} removed from the menu.")
    else:
        print(f"{item_name} is not in the menu.")

def search_item():
    query = input("Enter item name to search: ").strip()
    key, price = find_item(query)
    if price is not None:
        print(f"Found: {key} - ${price:.2f}")
    else:
        print(f"'{query}' not found in individual menu items.")

def order_mode(active_cart):
    print("\n1. Order a Combo Set")
    print("2. Order Separate Items")
    sub_choice = input("Choose order type (1 or 2): ").strip()
    
    if sub_choice == "1":
        print("\nAvailable Sets:")
        for s_name, s_info in set_menu.items():
            print(f"  {s_name} - ${s_info['price']:.2f} ({', '.join(s_info['items'])})")
        chosen_set = input("Enter the exact set name to order: ").strip()
        if chosen_set in set_menu:
            bundle = set_menu[chosen_set]
            active_cart.append((chosen_set, bundle["price"]))
            print(f"Added {chosen_set} (${bundle['price']:.2f}) to your order!")
        else:
            print("Set not found.")
            
    elif sub_choice == "2":
        raw_input = input("Enter separate items separated by commas: ")
        items_to_order = [item.strip() for item in raw_input.split(",") if item.strip()]
        for item_name in items_to_order:
            key, price = find_item(item_name)
            if price is not None:
                print(f"Added {key} (${price:.2f}) to your order.")
                active_cart.append((key, price))
            else:
                print(f"'{item_name}' is not available in the menu.")
    else:
        print("Invalid order type.")

def checkout(active_cart):
    print("\n--- Receipt ---")
    if not active_cart:
        print("No items ordered.")
    else:
        total = 0.0
        for name, price in active_cart:
            print(f"  {name}: ${price:.2f}")
            total += price
        print(f"Total: ${total:.2f}")
    print("Thank you for your order! Goodbye.")

print("Welcome to Cafe Menu")

while True:
    print("\n--- Main Menu ---")
    print("1. List (Show all items & sets)")
    print("2. Order (Sets or separate items)")
    print("3. Add (Add new item)")
    print("4. Delete (Remove item)")
    print("5. Quit (Exit & checkout)")
    print("6. Search (Search for item)")

    try:
        choice = int(input("Enter your choice (1-6): "))
        match choice:
            case 1:
                list_menu()        
            case 2:
                order_mode(cart)
            case 3:
                add_item()
            case 4:
                delete_item()
            case 5:
                checkout(cart)
                break
            case 6:
                search_item()
            case _:
                print("Invalid choice. Please enter a number between 1 and 6.")
    except ValueError:
        print("Please enter a valid number.")

