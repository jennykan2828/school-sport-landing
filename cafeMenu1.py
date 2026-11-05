menu = {
     'Coffee': 3.2,
     'Tea': 2.5,
     'Sandwich':5.0,
     'Salad': 4.0,
     'Cake': 2.0,
}

set_menu = {
     'Set A1': {'items': ['Salad', 'Coffee', 'Egg Rice'], 'price':20},
     'Set B1': {'items': ['Chicken Rice', 'Lemon tea', 'Vegetable'], 'price':19}

}


def list_item():
     print("General Menu:")
     for item, price in menu.items():
          print(f"{item}: ${price:02f}")

     for set_name, set_info in set_menu.items():
          print(f"{set_name}: ${set_info.values}")




                


print("welcome to the School Sports Cafe!")

while True:
    print("1. List Menu")
    print("2. Add Item")
    print("3. Delete Item")
    print("4. Order Item")
    print("5. Checkout")

    choice = int(input("Enter your choice: "))
    match choice:
        case 1:
             list_item()
        case 2:
             add_item()
        case 3:
             delete_item()
        case 4:
              order_item()
        case 5:
             checkout()
             break            
        case _:
              print("invalid choice. Please try again.")

    