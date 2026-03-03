from mongodb import materials_collection

def generate_learning_path(user):

    level_map = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3,
        "Expert": 4
    }

    user_level = user.get("level", "Beginner")
    numeric_level = level_map.get(user_level, 1)

    domain = user.get("domain", "").strip()
    preference = user.get("preference", "").strip().lower()

    
    preference_map = {
        "text": ["pdf"],
        "slides": ["ppt"],
        "video": ["video"],
        "mixed": ["pdf", "ppt", "video"]
    }

    allowed_types = preference_map.get(preference, ["pdf", "ppt", "video"])

    print("User Domain:", domain)
    print("User Level:", numeric_level)
    print("User Preference:", preference)

    
    materials = list(materials_collection.find({
        "domain": {"$regex": domain, "$options": "i"}
    }))

    print("After domain filter:", len(materials))

    
    filtered = []
    for m in materials:
        mat_level = m.get("level")

        if isinstance(mat_level, int):
            if mat_level <= numeric_level:
                filtered.append(m)

        elif isinstance(mat_level, str):
            if level_map.get(mat_level, 1) <= numeric_level:
                filtered.append(m)

    print("After level filter:", len(filtered))


    final = []
    for m in filtered:
        if m.get("type", "").lower() in allowed_types:
            final.append(m)

    print("After preference filter:", len(final))

    return final