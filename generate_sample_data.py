import pickle
import os

# Sample inventory data
inventory = {
    "Zigzag": {"price": 10, "stock": 5000},
    "I-shape": {"price": 12, "stock": 3000},
    "Square": {"price": 8, "stock": 7000}
}

# Sample labour data
labours = [
    {"id": 1, "name": "Ravi", "role": "Loader", "wage": 300},
    {"id": 2, "name": "Sita", "role": "Mixer", "wage": 350},
    {"id": 3, "name": "Mohit", "role": "Supervisor", "wage": 500}
]

# Sample order data
orders = [
    {"customer": "Anil Sharma", "contact": "9876543210", "brick": "Zigzag", "qty": 1000, "total": 10000}
]

# Make sure the folder exists
os.makedirs("sample_data", exist_ok=True)

# Save files to sample_data/
with open("sample_data/inventory_sample.pkl", "wb") as f:
    pickle.dump(inventory, f)

with open("sample_data/labour_sample.pkl", "wb") as f:
    pickle.dump(labours, f)

with open("sample_data/orders_sample.pkl", "wb") as f:
    pickle.dump(orders, f)

print("✅ Sample data created in sample_data/")
