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
    view_win.geometry("520x400")

    #scroll
    canvas = tk.Canvas(view_win, borderwidth=0)
    scrollbar = tk.Scrollbar(view_win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for index, item in enumerate(inventory):
        item_frame = tk.Frame(scroll_frame, bd=1, relief=tk.RIDGE, padx=10, pady=5)
        item_frame.pack(fill=tk.X, pady=5, padx=5)

        info = f"{index+1}. Name: {item['name']} | Price: {item['price']} | Quantity: {item['quantity']}"
        tk.Label(item_frame, text=info).pack(side=tk.LEFT)

        tk.Button(item_frame, text="Edit", command=lambda i=index: edit_item(i)).pack(side=tk.RIGHT, padx=5)
        tk.Button(item_frame, text="Delete", command=lambda i=index: delete_item(i, view_win)).pack(side=tk.RIGHT)


def search_item_from_bar(query):
    query = query.strip().lower()
    if not query:
        messagebox.showerror("Error", "Please enter an item name to search.")
        return

    results = [item for item in inventory if query in item['name'].lower()]

    if not results:
        messagebox.showinfo("Search", "No matching items found.")
        return

    result_win = tk.Toplevel(window)
    result_win.title("Search Results")
    result_win.geometry("500x400")

    for item in results:
        item_frame = tk.Frame(result_win)
        item_frame.pack(fill=tk.X, pady=5, padx=10)

        info = f"Name: {item['name']} | Price: {item['price']} | Quantity: {item['quantity']}"
        tk.Label(item_frame, text=info).pack(side=tk.LEFT)
        

#gui setup
window = tk.Tk()
window.title("CNS CLI")
window.geometry("700x350")
window.configure(bg="#f0f4f8")
window.resizable(False, False)

#fonts and colors
FONT_LABEL = ("Segoe UI", 12)
FONT_TITLE = ("Unispace", 20, "bold")
FONT_TITLE2 = ("Unispace", 8, "bold")
ENTRY_WIDTH = 30
BUTTON_BG = "#007ACC"
BUTTON_FG = "white"

#title
title_frame = tk.Frame(window, bg="#f0f4f8")
title_frame.pack(pady=20)
tk.Label(
    title_frame, text="CRATES&STUFF", font=FONT_TITLE, bg="#f0f4f8", fg="#333"
).pack()
tk.Label(
    title_frame, text="(command-line interface)", font=FONT_TITLE2, bg="#f0f4f8", fg="#333"
).pack()

#form
form_frame = tk.Frame(window, bg="#f0f4f8")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Item Name:", font=FONT_LABEL, bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_name = tk.Entry(form_frame, width=ENTRY_WIDTH)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Price (₹):", font=FONT_LABEL, bg="#f0f4f8").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_price = tk.Entry(form_frame, width=ENTRY_WIDTH)
entry_price.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Quantity:", font=FONT_LABEL, bg="#f0f4f8").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_quantity = tk.Entry(form_frame, width=ENTRY_WIDTH)
entry_quantity.grid(row=2, column=1, pady=5)

#buttons
button_frame = tk.Frame(window, bg="#f0f4f8")
button_frame.pack(pady=20)

add_btn = tk.Button(
    button_frame,
    text="Add Item",
    width=15,
    font=FONT_LABEL,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    command=add_item,
    relief=tk.FLAT
)
add_btn.grid(row=0, column=0, padx=10)

view_btn = tk.Button(
    button_frame,
    text="View Item",
    width=15,
    font=FONT_LABEL,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    command=view_items,
    relief=tk.FLAT
)
view_btn.grid(row=0, column=1, padx=10)

search_entry = tk.Entry(
    button_frame,
    width=20,
    font=("Arial", 12)
)
search_entry.grid(row=0, column=2, padx=10)

search_btn = tk.Button(
    button_frame,
    text="Search",
    width=10,
    font=FONT_LABEL,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    command=lambda: search_item_from_bar(search_entry.get()),
    relief=tk.FLAT
)
search_btn.grid(row=0, column=3, padx=10)

#footer
footer = tk.Label(window, text="Built by Yugam Akharia", bg="#f0f4f8", fg="#888", font=("TImes New Roman", 9))
footer.pack(side="bottom", pady=10)

window.iconbitmap("C:/yug4m/Coding/Python/RE/projects/inventory-manager-cli/cnsicon.ico")

window.mainloop()