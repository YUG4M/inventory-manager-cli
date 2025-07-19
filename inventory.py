a = {"name": "Maggi", "price": 12, "quantity": 1}
l= []
def add_items():
    while True:
        name = input("Enter item name: ")
        price = int(input("Enter item price: "))
        quantity = int(input("Enter item quantity: "))

        item = {"name": name, "price": price, "quantity": quantity}
        l.append(item)

        ch = input("Do you want to add another item? (y/n): ")
        if ch.lower() != 'y':
            break

def readall():
    print("All items: ")
    for item in l:
            print(item)

def menu():
    while True:    
        print("Select Function:" \
        " 1) Add Item, 2) View All, 3) Exit")
        ch=int(input("Choose function (1,2 or 3): "))
        if ch==1:
            add_items()
        elif ch==2:
            readall()
        elif ch==3:
            print("Thank you for using our system!")
            break
        else:
            print("Error! choose from 1,2 or 3 ")

menu()