import os
from app import app, db
from models.database import PredictionHistory

def verify_database():
    print("--- 🔍 Starting Task 1 Database Verification ---")
    
    # Check if DB file exists
    if not os.path.exists('ecopack.db'):
        print("⚠️ Warning: ecopack.db not found. Running create_all()...")

    with app.app_context():
        try:
            # Step 1: Force table creation if they don't exist
            db.create_all()

            # Step 2: Create a test entry using EXACT names from our schema
            # We use product_weight_kg to match your API input logic
            test_entry = PredictionHistory(
                product_weight_kg=1.5,
                category="Electronics",
                predicted_cost_index=0.82,
                predicted_co2_impact=0.41
            )
            
            # Step 3: Add and Commit to the SQLite database
            db.session.add(test_entry)
            db.session.commit()
            
            print("✅ SUCCESS: PredictionHistory record created without naming errors!")
            
            # Step 4: Query the data back to verify persistence
            record = PredictionHistory.query.order_by(PredictionHistory.id.desc()).first()
            print(f"📊 Verified Record in DB -> ID: {record.id}, Weight: {record.product_weight_kg}kg, Category: {record.category}")
            print("\n--- ✅ Task 1 is 100% Validated ---")

        except Exception as e:
            print(f"❌ ERROR: Database verification failed.")
            print(f"Details: {str(e)}")
            print("\n💡 ACTION: If you see 'invalid keyword argument', delete ecopack.db and restart app.py.")

if __name__ == "__main__":
    verify_database()