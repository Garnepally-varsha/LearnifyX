from mongodb import materials_collection

def generate_learning_path(user):

    level_map = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3,
        "Expert": 4
    }

    user_level = user.get("level", "").capitalize()
    numeric_level = level_map.get(user_level, 1)

    domain = user.get("domain", "")
    preference = user.get("preference", "mix")

    query = {
        "domain": {"$regex": f"^{domain}$", "$options": "i"},
        "level": {"$lte": numeric_level}
    }

    if preference and preference.lower() != "mix":
        query["type"] = {"$regex": f"^{preference}$", "$options": "i"}

    materials = list(
        materials_collection
        .find(query)
        .sort("level", 1)
    )

    print("Mongo Query:", query)
    print("Materials Found:", materials)

    return materials