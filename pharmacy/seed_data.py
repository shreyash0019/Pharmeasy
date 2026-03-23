# pharmacy/seed_data.py
from django.contrib.auth import get_user_model
from pharmacy.models import Medicine, MedicalStore, StoreInventory
import random

def seed():
    User = get_user_model()

    # ✅ Avoid duplicates if already seeded
    if User.objects.filter(username="user1").exists():
        return

    print("Seeding test users, stores, medicines, and inventories...")

    # --- Create 15 users and stores ---
    users = []
    stores = []
    for i in range(1, 16):
        username = f"user{i}"
        user = User.objects.create_user(username=username, password="password123")
        users.append(user)

        store_name = f"Pharmacy {i}"
        store = MedicalStore.objects.create(user=user, store_name=store_name, address=f"{i} Main Street")
        stores.append(store)

    # --- Create 20 medicines ---
    med_names = [
        "Paracetamol", "Ibuprofen", "Amoxicillin", "Ciprofloxacin",
        "Metformin", "Aspirin", "Cetirizine", "Loratadine",
        "Omeprazole", "Azithromycin", "Vitamin C", "Vitamin D",
        "Hydrochlorothiazide", "Atorvastatin", "Simvastatin",
        "Prednisone", "Levothyroxine", "Losartan", "Gabapentin", "Clindamycin"
    ]
    medicines = []
    for name in med_names:
        med = Medicine.objects.create(name=name, description=f"{name} description")
        medicines.append(med)

    # --- Create inventory for all stores ---
    for store in stores:
        selected_meds = random.sample(medicines, 10)  # each store has 10 random medicines
        for med in selected_meds:
            price = random.randint(20, 200)
            stock = random.randint(10, 100)
            StoreInventory.objects.create(store=store, medicine=med, price=price, stock=stock)

    print("✅ Seeding completed successfully.")
