from mongodb import materials_collection, users_collection
from ai_engine import generate_learning_path


print("=" * 50)
print("TEST 1: Check materials in database")
print("=" * 50)

total_materials = materials_collection.count_documents({})
print(f"Total materials in database: {total_materials}")


domains = materials_collection.distinct("domain")
print(f"\nDomains in database: {domains}")

levels = materials_collection.distinct("level")
print(f"Levels in database: {levels}")


types = materials_collection.distinct("type")
print(f"Types in database: {types}")


print(f"\nSample documents (first 3):")
samples = list(materials_collection.find().limit(3))
for i, doc in enumerate(samples, 1):
    print(f"\n{i}. {doc.get('title')}")
    print(f"   Domain: {doc.get('domain')}, Level: {doc.get('level')}, Type: {doc.get('type')}")


print("\n" + "=" * 50)
print("TEST 2: Test with real user data")
print("=" * 50)

test_user = users_collection.find_one({"email": "garnepallyvarshagoud@gmail.com"})
if test_user:
    print(f"\nFound test user:")
    print(f"  Email: {test_user.get('email')}")
    print(f"  Domain: {test_user.get('domain')}")
    print(f"  Level: {test_user.get('level')}")
    print(f"  Preference: {test_user.get('preference')}")
    
    
    print(f"\nGenerating learning path...")
    materials = generate_learning_path(test_user)
    print(f"Materials found: {len(materials)}")
    
    if materials:
        print("\nFirst 3 materials:")
        for i, mat in enumerate(materials[:3], 1):
            print(f"  {i}. {mat.get('title')} - Domain: {mat.get('domain')}, Level: {mat.get('level')}")
    else:
        print("\n⚠ No materials found. Debugging query...")
        
    
        level_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
        numeric_level = level_map.get(test_user.get("level"), 1)
        
        query = {
            "domain": test_user.get("domain"),
            "level": {"$lte": numeric_level}
        }
        
        print(f"\nQuery being used: {query}")
        

        count = materials_collection.count_documents(query)
        print(f"Materials matching query: {count}")
        
    
        print(f"\nTesting individual conditions:")
        
        domain_count = materials_collection.count_documents({"domain": test_user.get("domain")})
        print(f"  Materials with domain '{test_user.get('domain')}': {domain_count}")
        
        
        level_count = materials_collection.count_documents({"level": {"$lte": numeric_level}})
        print(f"  Materials with level <= {numeric_level}: {level_count}")
        
        
        sample = materials_collection.find_one({"domain": test_user.get("domain")})
        if sample:
            print(f"\nSample material for domain '{test_user.get('domain')}':")
            print(f"  Title: {sample.get('title')}")
            print(f"  Domain: {sample.get('domain')}")
            print(f"  Level: {sample.get('level')} (type: {type(sample.get('level')).__name__})")
            print(f"  Type: {sample.get('type')}")
        else:
            print(f"\n✗ NO materials found for domain '{test_user.get('domain')}'")

else:
    print("✗ No test user found. Create a user first!")
