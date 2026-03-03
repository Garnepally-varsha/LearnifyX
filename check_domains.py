from mongodb import materials_collection

# Get exact domains
domains = materials_collection.distinct('domain')

print("Exact domains in database:")
for d in sorted(domains):
    count = materials_collection.count_documents({"domain": d})
    print(f'  Value: "{d}" (length: {len(d)}, materials: {count})')

# Check each domain for Full Stack variants
print("\nChecking 'Full Stack' variants:")
variants = ["Full Stack", "FullStack", "full stack", "Full stack"]
for variant in variants:
    count = materials_collection.count_documents({"domain": variant})
    if count > 0:
        print(f'  "{variant}" → {count} materials ✓')

# Check each domain for Data Science variants
print("\nChecking 'Data Science' variants:")
variants = ["Data Science", "DataScience", "data science", "Data science"]
for variant in variants:
    count = materials_collection.count_documents({"domain": variant})
    if count > 0:
        print(f'  "{variant}" → {count} materials ✓')
