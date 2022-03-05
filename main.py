from multiprocessing import connection
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import lxml
import requests
import smtplib
import os

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

GMAIL = os.getenv("GMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")


header = {
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}

response = requests.get(URL, headers=header)
content = response.text

soup = BeautifulSoup(content, "lxml")
price_tag = soup.find(name="span", class_="a-size-base a-color-price a-color-price")
price_book = float(price_tag.string.split("$")[1])

if price_book <= 21: 
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=GMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=f"{GMAIL}",
        to_addrs=f"{GMAIL}",
        msg=f"""Subject:Amazon Price Alert \n\n
        Principles for Dealing with the Changing World Order: Why Nations Succeed and Fail
        now price is: ${price_book}
        The link is below:
        {URL}
        """
    )
    connection.close()

else:
    pass