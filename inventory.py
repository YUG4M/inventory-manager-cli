import json

try:
    with open("inventory.json", "r") as f:
        inventory = json.load(f)
    print("Inventory loaded.")
except FileNotFoundError:
    inventory = []
    print("No previous data. Starting fresh!")

def add_item():
    while True:
        name = input("Enter item name: ")
        price = int(input("Enter item price: "))
        quantity = int(input("Enter item quantity: "))

        item = {"name": name, "price": price, "quantity": quantity}
        inventory.append(item)
        print("Item added Succesfully! ")
        ch = input("Do you want to add another item? (y/n): ")
        if ch.lower() != 'y':
            break

def view_items():
    print("All items: ")
    for item in inventory:
            print(item)

def update_item():
    name = input("Enter item name to update: ")
    for item in inventory:
        if item["name"] == name:
            new_qty = int(input("Enter new quantity: "))
            item["quantity"] = new_qty
            print("Quantity updated.")
            return
    print("Item not found! ")

def delete_item():
    name = input("Enter item name to delete: ")
    for i, item in enumerate(inventory):
        if item["name"] == name:
            del inventory[i]
            print("Item deleted.")
            return
    print("Item not found.")        

def save_inventory():
    with open("inventory.json", "w") as f:
        json.dump(inventory, f)
    print("Inventory saved!")

def menu():
    while True:    
        print("Select Function:" \
        " 1) Add Item, 2) View All, 3) Update Item, 4) Delete Item, 5) Exit")
        ch=int(input("Choose function in numbers (1,2,3,....): "))
        if ch == 1:
            add_item()
        elif ch == 2:
            view_items()
        elif ch == 3:
            update_item()
        elif ch == 4:
            delete_item()
        elif ch == 5:
            save_inventory()
            print("Thank you for using our system!")
            break
        else:
            print("Error! choose from 1,2 or 3 ")

menu()