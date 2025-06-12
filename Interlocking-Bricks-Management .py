import pickle
import os

# ----------------------- Data Persistence Helpers -----------------------

def save_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}

# ------------------------ Brick Inventory Class -------------------------

class BrickInventory:
    def __init__(self):
        self.inventory = load_data("inventory.pkl")

    def add_brick(self, brick_type, price, stock):
        self.inventory[brick_type] = {'price': price, 'stock': stock}
        save_data(self.inventory, "inventory.pkl")
        print(f"{brick_type} added successfully.")

    def update_stock(self, brick_type, qty):
        if brick_type in self.inventory:
            self.inventory[brick_type]['stock'] += qty
            save_data(self.inventory, "inventory.pkl")
            print("Stock updated.")
        else:
            print("Brick type not found.")

    def view_inventory(self):
        print("\n📦 Available Bricks:")
        for i, (brick, details) in enumerate(self.inventory.items(), start=1):
            print(f"{i}. {brick} - ₹{details['price']} per piece - Stock: {details['stock']}")

    def get_brick_by_index(self, index):
        keys = list(self.inventory.keys())
        if 0 <= index < len(keys):
            return keys[index]
        return None

    def reduce_stock(self, brick_type, qty):
        if brick_type in self.inventory and self.inventory[brick_type]['stock'] >= qty:
            self.inventory[brick_type]['stock'] -= qty
            save_data(self.inventory, "inventory.pkl")  # 🔧 Fixed
            return True
        return False

# ----------------------- Labour Management Class ------------------------

class LabourManagement:
    def __init__(self):
        self.labours = load_data("labour.pkl")

    def add_labour(self, labour_id, name, role, wage):
        self.labours[labour_id] = {'name': name, 'role': role, 'wage': wage, 'attendance': 0}
        save_data(self.labours, "labour.pkl")
        print("Labour added successfully.")

    def update_labour(self, labour_id, role=None, wage=None):
        if labour_id in self.labours:
            if role:
                self.labours[labour_id]['role'] = role
            if wage:
                self.labours[labour_id]['wage'] = wage
            save_data(self.labours, "labour.pkl")
            print("Labour info updated.")
        else:
            print("Labour not found.")

    def mark_attendance(self, labour_id):
        if labour_id in self.labours:
            self.labours[labour_id]['attendance'] += 1
            save_data(self.labours, "labour.pkl")
            print("Attendance marked.")
        else:
            print("Labour not found.")

    def view_labours(self):
        for id, details in self.labours.items():
            print(f"ID: {id}, Name: {details['name']}, Role: {details['role']}, Wage: ₹{details['wage']}, Attendance: {details['attendance']}")

# ------------------------ Customer Order Class --------------------------

class CustomerOrder:
    def __init__(self, inventory_obj):
        self.orders = load_data("orders.pkl")
        self.inventory_obj = inventory_obj

    def place_order(self, name, contact, brick_type, qty):
        if brick_type not in self.inventory_obj.inventory:
            print("Brick type not available.")
            return
        if self.inventory_obj.reduce_stock(brick_type, qty):
            price = self.inventory_obj.inventory[brick_type]['price']
            total = price * qty
            self.orders[len(self.orders) + 1] = {
                'name': name, 'contact': contact,
                'brick_type': brick_type, 'qty': qty, 'total': total
            }
            save_data(self.orders, "orders.pkl")  # 🔧 Ensure order is saved
            print(f"✅ Order placed successfully!\nBill Amount: ₹{total}")
            print("💸 Please pay in cash or via UPI when the order is delivered to your location.")  # ✅ FIXED message
        else:
            print("❌ Not enough stock.")

    def view_orders(self):
        if not self.orders:
            print("No orders yet.")
            return
        for oid, details in self.orders.items():
            print(f"Order ID: {oid}, Name: {details['name']}, Brick: {details['brick_type']}, Qty: {details['qty']}, Total: ₹{details['total']}")

# ---------------------------- Login System ------------------------------

def owner_menu():
    inventory = BrickInventory()
    labour = LabourManagement()
    orders = CustomerOrder(inventory)

    while True:
        print("\n📋 Owner Menu:\n1. View Inventory\n2. Add Brick\n3. Update Stock\n4. View Labours\n5. Add Labour\n6. Update Labour\n7. Mark Attendance\n8. View Orders\n9. Exit")
        choice = input("Choose: ")
        if choice == '1':
            inventory.view_inventory()
        elif choice == '2':
            b = input("Brick type: ")
            p = int(input("Price: "))
            s = int(input("Stock: "))
            inventory.add_brick(b, p, s)
        elif choice == '3':
            b = input("Brick type: ")
            s = int(input("Add stock: "))
            inventory.update_stock(b, s)
        elif choice == '4':
            labour.view_labours()
        elif choice == '5':
            lid = input("ID: ")
            n = input("Name: ")
            r = input("Role: ")
            w = int(input("Wage: "))
            labour.add_labour(lid, n, r, w)
        elif choice == '6':
            lid = input("ID: ")
            r = input("New Role (leave blank to skip): ")
            w = input("New Wage (leave blank to skip): ")
            labour.update_labour(lid, role=r if r else None, wage=int(w) if w else None)
        elif choice == '7':
            lid = input("ID: ")
            labour.mark_attendance(lid)
        elif choice == '8':
            orders.view_orders()
        elif choice == '9':
            break

def customer_menu():
    inventory = BrickInventory()
    order = CustomerOrder(inventory)

    while True:
        print("\n🧾 Customer Menu:\n1. View Inventory\n2. Place Order\n3. Exit")
        choice = input("Choose: ")
        if choice == '1':
            inventory.view_inventory()
        elif choice == '2':
            inventory.view_inventory()
            try:
                index = int(input("Enter brick number from above list: ")) - 1
                brick_type = inventory.get_brick_by_index(index)
                if not brick_type:
                    print("Invalid choice.")
                    continue
                name = input("Your Name: ")
                contact = input("Contact Number: ")
                qty = int(input(f"Quantity of {brick_type}: "))
                order.place_order(name, contact, brick_type, qty)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '3':
            break

# --------------------------- Main Program -------------------------------

def main():
    while True:
        print("\n🔐 Login as:\n1. Owner\n2. Customer\n3. Exit")
        user = input("Choose: ")
        if user == '1':
            pwd = input("Enter Owner Password: ")
            if pwd == 'admin123':
                owner_menu()
            else:
                print("❌ Incorrect password!")
        elif user == '2':
            customer_menu()
        elif user == '3':
            break

if __name__ == "__main__":
    main()
