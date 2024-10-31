from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.amazon.in/Logitech-Wireless-Customisable-Bluetooth-Easy-Switch/dp/B0CGCZCHN3"

response = requests.get(URL, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
})

soup = BeautifulSoup(response.content, "html.parser")

price_whole = soup.find(class_="a-price-whole")

price = price_whole.text
# Remove commas and convert to float
float_value = float(price.replace(',', ''))
price = float_value

title = soup.find(id="productTitle").get_text().strip()

BUY_PRICE = 1500

if price < BUY_PRICE:
    message = f'Subject:Amazon Price Alert!\n\n {title} is now {price}/-\n{URL}'
    with smtplib.SMTP(host=os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADDRESS"],
            to_addrs=os.environ["EMAIL_ADDRESS"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )

