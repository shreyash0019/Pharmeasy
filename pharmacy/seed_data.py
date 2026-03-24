# pharmacy/seed_data.py
from django.contrib.auth import get_user_model
from pharmacy.models import Medicine, MedicalStore, StoreInventory
import random

def seed():
    User = get_user_model()

    # ✅ Avoid duplicates if already seeded
    if User.objects.filter(username="patient1").exists():
        return

    print("Seeding test users, stores, medicines, and inventories...")

    # --- Create 3 patients ---
    patients_data = [
        {"username": "patient1", "email": "patient1@example.com", "password": "password123"},
        {"username": "patient2", "email": "patient2@example.com", "password": "password123"},
        {"username": "patient3", "email": "patient3@example.com", "password": "password123"},
    ]
    patients = []
    for pdata in patients_data:
        user = User.objects.create_user(username=pdata["username"], email=pdata["email"], password=pdata["password"], role="patient")
        patients.append(user)

    # --- Create 3 sellers ---
    sellers_data = [
        {"username": "seller1", "email": "seller1@example.com", "password": "password123"},
        {"username": "seller2", "email": "seller2@example.com", "password": "password123"},
        {"username": "seller3", "email": "seller3@example.com", "password": "password123"},
    ]
    sellers = []
    stores = []
    for sdata in sellers_data:
        seller = User.objects.create_user(username=sdata["username"], email=sdata["email"], password=sdata["password"], role="seller")
        sellers.append(seller)

        # Create a store for each seller
        store = MedicalStore.objects.create(
            user=seller,
            store_name=f"{seller.username.capitalize()} Pharmacy",
            address=f"{random.randint(1, 100)} Market Street"
        )
        stores.append(store)

    # --- Create 10 medicines ---
    med_names = [
        "Paracetamol", "Ibuprofen", "Amoxicillin", "Ciprofloxacin",
        "Metformin", "Aspirin", "Cetirizine", "Loratadine",
        "Omeprazole", "Azithromycin"
    ]
    medicines = []
    for name in med_names:
        med = Medicine.objects.create(name=name, description=f"{name} description")
        medicines.append(med)

    # --- Add inventory for each store ---
    for store in stores:
        selected_meds = random.sample(medicines, 5)  # each store has 5 random medicines
        for med in selected_meds:
            price = random.randint(20, 200)
            stock = random.randint(10, 50)
            StoreInventory.objects.create(store=store, medicine=med, price=price, stock=stock)

    print("✅ Seeding completed successfully.\n")
    print("Patient Credentials:")
    for p in patients:
        print(f"Username: {p.username}, Email: {p.email}, Password: password123")
    print("\nSeller Credentials:")
    for s in sellers:
        print(f"Username: {s.username}, Email: {s.email}, Password: password123, Store: {s.medical_store.store_name}")
