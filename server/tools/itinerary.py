def generate_itinerary(destination: str, days: int):
    itinerary = []

    for day in range(1, days + 1):
        itinerary.append({
            "day": day,
            "morning": f"Explore famous spots in {destination}",
            "afternoon": "Visit cafes and local markets",
            "evening": "Relax at scenic viewpoints"
        })

    return itinerary