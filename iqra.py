import sqlite3
from tkinter import *
from tkinter import messagebox

# Database setup
conn = sqlite3.connect("iqra_marketing.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    total REAL
)
""")

conn.commit()

# UI
root = Tk()
root.title("IQRA MARKETING Billing Software")
root.geometry("600x500")

# Labels
Label(root, text="IQRA MARKETING", font=("Arial", 16, "bold")).pack()
Label(root, text="Karuvanpadi 679305 | Ph: 8089305300").pack()

# Product Section
frame = Frame(root)
frame.pack(pady=10)

name_var = StringVar()
price_var = DoubleVar()
qty_var = IntVar()

Entry(frame, textvariable=name_var, width=20).grid(row=0, column=0)
Entry(frame, textvariable=price_var, width=10).grid(row=0, column=1)
Entry(frame, textvariable=qty_var, width=10).grid(row=0, column=2)

def add_product():
    cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
                   (name_var.get(), price_var.get(), qty_var.get()))
    conn.commit()
    messagebox.showinfo("Success", "Product Added")

Button(frame, text="Add Product", command=add_product).grid(row=0, column=3)

# Billing Section
Label(root, text="Billing", font=("Arial", 14)).pack(pady=10)

bill_frame = Frame(root)
bill_frame.pack()

product_name = StringVar()
bill_qty = IntVar()

Entry(bill_frame, textvariable=product_name, width=20).grid(row=0, column=0)
Entry(bill_frame, textvariable=bill_qty, width=10).grid(row=0, column=1)

def bill_product():
    cursor.execute("SELECT price, quantity FROM products WHERE name=?", (product_name.get(),))
    result = cursor.fetchone()

    if result:
        price, stock = result
        if bill_qty.get() <= stock:
            total = price * bill_qty.get()

            cursor.execute("INSERT INTO sales (product, quantity, total) VALUES (?, ?, ?)",
                           (product_name.get(), bill_qty.get(), total))

            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE name=?",
                           (bill_qty.get(), product_name.get()))

            conn.commit()
            messagebox.showinfo("Bill", f"Total Amount: ₹{total}")
        else:
            messagebox.showerror("Error", "Not enough stock")
    else:
        messagebox.showerror("Error", "Product not found")

Button(bill_frame, text="Generate Bill", command=bill_product).grid(row=0, column=2)

root.mainloop()