from mongodb import users_collection

users_to_migrate = users_collection.find({"goal": {"$exists": True}, "domain": None})

count = 0
for user in users_to_migrate:
    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$rename": {
                "goal": "domain",
                "time": "motive"
            }
        }
    )
    count += 1
    print(f"✓ Migrated: {user.get('email')}")

print(f"\n✅ Total users migrated: {count}")


print("\n--- Verification ---")
test_user = users_collection.find_one({"email": "garnepallyvarshagoud@gmail.com"})
print(f"Domain: {test_user.get('domain')}")
print(f"Motive: {test_user.get('motive')}")
print(f"Level: {test_user.get('level')}")
