#pip install requests
#pip install beautifulsoup4
#pip install mysql-connector-python








from bs4 import BeautifulSoup
import requests
import mysql.connector

# ---------------- MYSQL CONNECTION ----------------
mydb = mysql.connector.connect(
    host="localhost",
    user="harish",
    password="mypassword",
    database="ecommerce",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

choice = 'y'

while choice.lower() == 'y':

    try:
        # ---------------- INPUT URL ----------------
        URL = input("Enter Amazon Product URL:\n")

        # ---------------- HEADERS ----------------
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.5'
        }

        # ---------------- REQUEST PAGE ----------------
        page = requests.get(URL, headers=headers)

        # ---------------- PARSE HTML ----------------
        soup = BeautifulSoup(page.content, "html.parser")

        # ---------------- PRODUCT TITLE ----------------
        title = soup.find(id='productTitle')

        if title:
            title = title.get_text().strip()
        else:
            title = "Not Available"

        # ---------------- PRICE ----------------
        price = soup.find('span', class_='a-price-whole')

        if price:
            price = price.get_text().strip()

            # Remove commas, dots, spaces
            price = price.replace(",", "")
            price = price.replace(".", "")
            price = price.replace(" ", "")

        else:
            price = "0"

        # ---------------- RATING ----------------
        rating = soup.find('span', class_='a-icon-alt')

        if rating:
            rating = rating.get_text().strip()
        else:
            rating = "No Rating"

        # ---------------- EXTRA DETAILS ----------------
        color = "Not Available"
        material = "Not Available"
        dimensions = "Not Available"

        details = soup.find_all('tr')

        for row in details:

            text = row.get_text().lower()

            if "color" in text:
                color = row.get_text().strip()

            if "material" in text:
                material = row.get_text().strip()

            if "dimensions" in text:
                dimensions = row.get_text().strip()

        # ---------------- INSERT INTO DATABASE ----------------
        sql = """
        INSERT INTO products
        (name, price, rating, color, material, dimensions)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            title[:255],
            int(price),
            rating,
            color,
            material,
            dimensions
        )

        mycursor.execute(sql, values)

        mydb.commit()

        # ---------------- OUTPUT ----------------
        print("\nData Stored Successfully!\n")

        print("Product Name :", title)
        print("Price        :", price)
        print("Rating       :", rating)
        print("Color        :", color)
        print("Material     :", material)
        print("Dimensions   :", dimensions)

    except Exception as e:
        print("Error occurred:", e)

    finally:
        choice = input("\nDo you want to scrape another product? (y/n): ")

# ---------------- CLOSE DATABASE ----------------
mydb.close()
