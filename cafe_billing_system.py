import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime


# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Retail Smart Billing System")
root.geometry("900x600")
root.resizable(False, False)
root.configure(bg="#1E1E2F")


# ================= AI DISCOUNT LOGIC =================
def get_ai_discount(subtotal, qty):
    discount = 0
    if subtotal >= 3000:
        discount = 20
    elif subtotal >= 2000:
        discount = 15
    elif subtotal >= 1000:
        discount = 10
    elif subtotal >= 500:
        discount = 5

    if qty >= 10:
        discount += 5

    return discount


# ================= ITEM SUGGESTION =================
def get_suggestion(item):
    data = {
        "Rice": "Try Dal or Chicken Curry",
        "Milk": "Buy Bread or Cereal",
        "Bread": "Pair with Butter or Jam",
        "Sugar": "Essential for Tea/Coffee",
        "Tea": "Try Biscuit combo",
        "Coffee": "Best with Snacks"
    }
    return data.get(item, "No suggestion available")


# ================= BILL FUNCTION =================
def generate_bill():
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    item = item_var.get()

    # -------- NAME VALIDATION --------
    if name == "":
        messagebox.showerror("Error", "Customer name is required")
        return

    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name must be valid")
        return

    # -------- CONTACT VALIDATION --------
    if contact == "":
        messagebox.showerror("Error", "Contact number is required")
        return

    if not contact.isdigit():
        messagebox.showerror("Error", "Contact must contain digits only")
        return

    if len(contact) < 10 or len(contact) > 13:
        messagebox.showerror("Error", "Contact must be 10–13 digits long")
        return

    # -------- ITEM VALIDATION --------
    if item == "Select Item":
        messagebox.showerror("Error", "Select item")
        return

    # -------- NUMERIC VALIDATION --------
    try:
        price = float(price_entry.get())
        qty = int(qty_entry.get())
        manual_discount = float(discount_entry.get() or 0)
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Invalid numeric input")
        return

    if price <= 0:
        messagebox.showerror("Error", "Price must be greater than 0")
        return

    if qty <= 0:
        messagebox.showerror("Error", "Quantity must be greater than 0")
        return

    if manual_discount < 0 or manual_discount > 100:
        messagebox.showerror("Error", "Discount must be between 0–100")
        return

    # -------- BILL CALCULATION --------
    subtotal = price * qty
    ai_discount = get_ai_discount(subtotal, qty)
    final_discount = max(ai_discount, manual_discount)

    discount_amount = subtotal * final_discount / 100
    tax = subtotal * 0.05
    total = subtotal - discount_amount + tax

    suggestion = get_suggestion(item)
    time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    # -------- RECEIPT --------
    receipt.delete("1.0", tk.END)

    receipt.insert(tk.END, "====================================\n")
    receipt.insert(tk.END, "        RETAIL POS SYSTEM\n")
    receipt.insert(tk.END, "====================================\n\n")

    receipt.insert(tk.END, f"Date: {time_str}\n")
    receipt.insert(tk.END, f"Customer: {name.title()}\n")
    receipt.insert(tk.END, f"Contact: {contact}\n")
    receipt.insert(tk.END, "------------------------------------\n")

    receipt.insert(tk.END, f"Item: {item}\n")
    receipt.insert(tk.END, f"Price: {price}\n")
    receipt.insert(tk.END, f"Quantity: {qty}\n")
    receipt.insert(tk.END, "------------------------------------\n")

    receipt.insert(tk.END, f"Subtotal: {subtotal}\n")
    receipt.insert(tk.END, f"Discount: {final_discount}%\n")
    receipt.insert(tk.END, f"Discount Amount: {discount_amount:.2f}\n")
    receipt.insert(tk.END, f"Tax (5% GST): {tax:.2f}\n")
    receipt.insert(tk.END, f"TOTAL: {total:.2f}\n\n")

    receipt.insert(tk.END, f"AI Suggestion: {suggestion}\n")
    receipt.insert(tk.END, "\nThank you for shopping with us!")


# ================= CLEAR =================
def clear():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    discount_entry.delete(0, tk.END)
    item_var.set("Select Item")
    receipt.delete("1.0", tk.END)


# ================= EXIT =================
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure?"):
        root.destroy()


# ================= SAVE RECEIPT =================
def save_receipt():
    content = receipt.get("1.0", tk.END).strip()

    if not content:
        messagebox.showwarning("Empty Receipt", "Generate bill first")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if file_path:
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", "Receipt saved successfully!")


# ================= LEFT PANEL =================
left_frame = tk.Frame(root, bg="#1a1a2e", highlightthickness=1,
                      highlightbackground="#00A86B")
left_frame.place(x=20, y=20, width=400, height=560)

tk.Label(left_frame, text="Retail Billing Panel",
         font=("Consolas", 15, "bold"),
         bg="#1a1a2e", fg="#00e5a0").pack(pady=12)


def add_field(parent, label):
    tk.Label(parent, text=label, bg="#1a1a2e",
             fg="#aab4c8", font=("Consolas", 9)).pack(anchor="w", padx=18)
    e = tk.Entry(parent, bg="#0d1117", fg="#e8f0fe",
                 insertbackground="white", relief="flat")
    e.pack(padx=18, pady=5, ipady=3)
    return e


name_entry = add_field(left_frame, "Customer Name")
contact_entry = add_field(left_frame, "Contact Number")

tk.Label(left_frame, text="Item", bg="#1a1a2e",
         fg="#aab4c8").pack(anchor="w", padx=18)

item_var = tk.StringVar(value="Select Item")
items = ["Rice", "Milk", "Bread", "Sugar", "Tea", "Coffee"]
tk.OptionMenu(left_frame, item_var, *items).pack(padx=18, anchor="w")

price_entry = add_field(left_frame, "Price")
qty_entry = add_field(left_frame, "Quantity")
discount_entry = add_field(left_frame, "Manual Discount (%)")


# ================= BUTTONS =================
btn_frame = tk.Frame(left_frame, bg="#1a1a2e")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Generate", bg="#00A86B", fg="white",
          command=generate_bill).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Save", bg="#1a6b9a", fg="white",
          command=save_receipt).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Clear", bg="#3a3a5c", fg="white",
          command=clear).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text="Exit", bg="#C0392B", fg="white",
          command=exit_app).grid(row=0, column=3, padx=5)


# ================= RIGHT PANEL =================
right_frame = tk.Frame(root, bg="#0d1117",
                       highlightthickness=1,
                       highlightbackground="#00A86B")
right_frame.place(x=442, y=20, width=438, height=560)

tk.Label(right_frame, text="Receipt",
         font=("Consolas", 15, "bold"),
         bg="#0d1117", fg="#00e5a0").pack(pady=10)

receipt = tk.Text(right_frame,
                  bg="#060a10", fg="#c9d8f0",
                  font=("Consolas", 10))
receipt.pack(fill="both", expand=True, padx=10, pady=10)


# ================= RUN =================
root.mainloop()