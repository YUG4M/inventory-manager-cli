import tkinter as tk
import json
from tkinter import messagebox
import os

#load inventory from json file
inventory = []
if os.path.exists("inventory.json") and os.path.getsize("inventory.json") > 0:
    with open("inventory.json", "r") as f:
        try:
            inventory = json.load(f)
            print("Inventory loaded.")
        except json.JSONDecodeError:
            print("File is not valid JSON. Starting with empty inventory.")
            inventory = []
else:
    print("No inventory file found or file is empty. Starting fresh!")

#add Item Function
def add_item():
    name = entry_name.get()
    price = entry_price.get()
    quantity = entry_quantity.get()

    if not name or not price or not quantity:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    try:
        price = int(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Price and Quantity must be numbers!")
        return

    item = {"name": name, "price": price, "quantity": quantity}
    inventory.append(item)

    with open("inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

    messagebox.showinfo("Success", f"Item '{name}' added!")

    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

#save inventory function
def save_inventory():
    with open("inventory.json", "w") as f:
        json.dump(inventory, f)

#delete item function
def delete_item(index, view_window):
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
    if confirm:
        del inventory[index]
        save_inventory()
        messagebox.showinfo("Deleted", "Item deleted successfully.")
        view_window.destroy()
        view_items()  # refresh view

#update item fucntion
def edit_item(index):
    edit_win = tk.Toplevel(window)
    edit_win.title("Edit Item")
    edit_win.geometry("300x200")

    item = inventory[index]

    tk.Label(edit_win, text="Edit Price:").pack()
    new_price = tk.Entry(edit_win)
    new_price.insert(0, str(item['price']))
    new_price.pack()

    tk.Label(edit_win, text="Edit Quantity:").pack()
    new_quantity = tk.Entry(edit_win)
    new_quantity.insert(0, str(item['quantity']))
    new_quantity.pack()

    def save_changes():
        try:
            price = int(new_price.get())
            quantity = int(new_quantity.get())
            inventory[index]['price'] = price
            inventory[index]['quantity'] = quantity
            save_inventory()
            messagebox.showinfo("Updated", "Item updated successfully.")
            edit_win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be numbers!")

    tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=10)

#view items function
def view_items():
    if not inventory:
        messagebox.showinfo("Inventory", "No items to show.")
        return

    view_win = tk.Toplevel(window)
    view_win.title("Inventory Items")
    view_win.geometry("500x400")

    for index, item in enumerate(inventory):
        item_frame = tk.Frame(view_win)
        item_frame.pack(fill=tk.X, pady=5)

        info = f"{index+1}. Name: {item['name']} | Price: {item['price']} | Quantity: {item['quantity']}"
        tk.Label(item_frame, text=info).pack(side=tk.LEFT)

        # Edit button
        tk.Button(item_frame, text="Edit", command=lambda i=index: edit_item(i)).pack(side=tk.RIGHT, padx=5)
        # Delete button
        tk.Button(item_frame, text="Delete", command=lambda i=index: delete_item(i, view_win)).pack(side=tk.RIGHT)

#gui setup
window = tk.Tk()
window.title("InventoryShell")
window.geometry("600x400")
window.resizable(False, False)

tk.Label(window, text="Welcome to InventoryShell!", font=("Times New Roman", 16)).pack(pady=20)

tk.Label(window, text="Item Name:").pack()
entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(window, text="Price:").pack()
entry_price = tk.Entry(window)
entry_price.pack()

tk.Label(window, text="Quantity:").pack()
entry_quantity = tk.Entry(window)
entry_quantity.pack()

tk.Button(window, text="Add Item", command=add_item).pack(pady=10)
tk.Button(window, text="View Items", command=view_items).pack(pady=10)
window.mainloop()
