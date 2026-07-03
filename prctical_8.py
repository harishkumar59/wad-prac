# Develop a focused crawler for local search.

# pip install requests beautifulsoup4

import requests

def local_crawler(city, amenity):

    bbox = {
        "mumbai": "18.89,72.77,19.30,73.00",
        "pune": "18.45,73.75,18.65,73.98",
        "delhi": "28.50,76.90,28.90,77.40"
    }

    city = city.lower()

    if city not in bbox:
        print("City not available.")
        return

    query = f"""
    [out:json][timeout:25];
    node["amenity"="{amenity}"]({bbox[city]});
    out body;
    """

    url = "https://overpass.kumi.systems/api/interpreter"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(
            url,
            data={"data": query},
            headers=headers,
            timeout=30
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        if not data["elements"]:
            print("No results found.")
            return

        print("\nSearch Results\n")

        for i, place in enumerate(data["elements"][:10], 1):
            tags = place.get("tags", {})
            print(f"{i}. {tags.get('name','Unknown')}")
            print("Latitude :", place["lat"])
            print("Longitude:", place["lon"])
            print("-"*40)

    except Exception as e:
        print("Error:", e)


city = input("Enter City: ")
amenity = input("Enter Amenity (hospital/school/bank/pharmacy/restaurant): ")

local_crawler(city, amenity)