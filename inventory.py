a = {"name": "Maggi", "price": 12, "quantity": 1}
inventory= []
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

def menu():
    while True:    
        print("Select Function:" \
        " 1) Add Item, 2) View All, 3) Exit")
        ch=int(input("Choose function (1,2 or 3): "))
        if ch == "1":
            add_item(inventory)
        elif ch == "2":
            view_items(inventory)
        elif ch == "3":
            update_item(inventory)
        elif ch == "4":
            delete_item(inventory)
        elif ch=="5":
            print("Thank you for using our system!")
            break
        else:
            print("Error! choose from 1,2 or 3 ")

menu()