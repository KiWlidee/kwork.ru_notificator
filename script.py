from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from requests import post

from time import sleep

from data import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


def send_telegram(message):
    bot_token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    post(url, data=data)
    return "Отправил сообщение в телеграм"

def prodicts(name, min_price, max_price, description):
    with open("kwork_script_notificatior\\offer.txt", "a", encoding="utf-8") as f:
        f.write(f"{name}. Желаемая цена - {min_price}, Максимальная цена - {max_price}\n\n")
        f.write(f"Описание: {description}\n\n\n")
    return "Записал оффер."

def sourse_parcer():
    sourse = browser.page_source

    return BeautifulSoup(sourse, "lxml")

def prices_name_description():
    price = soup.find("div", class_="wants-card__right")

    wants_price = price.find("div", class_="wants-card__price")
    wants_price = wants_price.find("div", class_="d-inline").text
    wants_price = "".join(str(wants_price).split())

    max_price = price.find("div", class_="wants-card__description-higher-price")
    max_price = max_price.find("div", class_="d-inline").text
    max_price = "".join(str(max_price).split())

    description = soup.find("div", class_="breakwords first-letter overflow-hidden").text

    name = soup.find("h1", class_="wants-card__header-title breakwords pr250").text

    return wants_price, max_price, description, name


browser = webdriver.Firefox()

link = ["https://kwork.ru/projects?a=1&fc=41&attr=211", 
        "https://kwork.ru/projects?a=1&fc=41&attr=3587", 
        "https://kwork.ru/projects?a=1&fc=41&attr=7352"]

first_html1 = ""
second_html1 = ""
third_html1 = ""

while True:
    for i in link:
        browser.get(i)
        sleep(1)

        elem = browser.find_element(By.CLASS_NAME, "kw-link-dashed")
        elem.click()

        soup = sourse_parcer()

        wants_price, max_price, description, name = prices_name_description()

        prodicts(name, wants_price, max_price, description)

        html_description = description


        if i == "https://kwork.ru/projects?a=1&fc=41&attr=211":
            if first_html1 == "":
                first_html1 = description
            if first_html1 == html_description:
                print("Ничего не изменилось.++++++++++++++++++++++++++++")
            else:
                first_html1 = html_description
                send_telegram(f"""{name}\nЖелаемая цена - {wants_price}
\nМаксимальная цена - {max_price}\n
{description}""")
                print("НОВЫЙ ЗАКАЗ")
                prodicts(name, wants_price, max_price, description)

        elif i == "https://kwork.ru/projects?a=1&fc=41&attr=3587":
            if second_html1 == "":
                second_html1 = description
            if second_html1 == html_description:
                print("Ничего не изменилось.++++++++++++++++++++++++++++")
            else:
                second_html1 = html_description
                send_telegram(f"""{name}\nЖелаемая цена - {wants_price}
\nМаксимальная цена - {max_price}\n
{description}""")
                print("НОВЫЙ ЗАКАЗ")
                prodicts(name, wants_price, max_price, description)

        elif i == "https://kwork.ru/projects?a=1&fc=41&attr=7352":
            if third_html1 == "":
                third_html1 = description
            if third_html1 == html_description:
                print("Ничего не изменилось.++++++++++++++++++++++++++++")
            else:
                third_html1 = html_description
                send_telegram(f"""{name}\nЖелаемая цена - {wants_price}
\nМаксимальная цена - {max_price}\n
{description}""")
                print("НОВЫЙ ЗАКАЗ")
                prodicts(name, wants_price, max_price, description)

        sleep(30)