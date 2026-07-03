import requests

def local_crawler(location, amenity):

    if location.lower() != "mumbai":
        print("Currently only Mumbai is supported.")
        return

    query = f"""
    [out:json];
    node["amenity"="{amenity}"](18.89,72.77,19.27,72.99);
    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    headers = {
        "User-Agent": "Python Local Crawler"
    }

    response = requests.post(
        url,
        data={"data": query},
        headers=headers
    )

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        if not data["elements"]:
            print("No results found.")
            return

        for i, place in enumerate(data["elements"], 1):
            print(i, place.get("tags", {}).get("name", "Unknown"))
            print(place["lat"], place["lon"])
            print()

    else:
        print(response.text)


city = input("Enter city: ")
amenity = input("Enter search (hospital/school/pharmacy/bank/restaurant): ")

local_crawler(city, amenity)