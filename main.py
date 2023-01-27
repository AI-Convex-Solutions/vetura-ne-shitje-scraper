import random
import string
import time
from pathlib import Path

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import config

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

if __name__ == '__main__':
    Path(config.DATASET_FOLDER).mkdir(parents=True, exist_ok=True)
    session = HTMLSession()
    page = session.get(config.URL, headers=headers)
    content = BeautifulSoup(page.content, "html.parser")
    car_list = content.find('ul', class_="car-list").select("li[class='row']")
    for car in car_list:
        car_url = car.find("a", href=True)["href"]
        car_title = car.find("h2", class_="lead")
        car_manufacturer = car.find("strong").text
        car_model = car_title.text.replace(f"Vetura ne shitje {car_manufacturer}", "")
        specs = car.find_all("div", class_="car-tech-detail")
        car_year = ""
        for spec in specs:
            year_location = spec.find("img", src=True)["src"]
            if year_location and "time" in year_location:
                car_year = spec.get_text("\n", True)
                break
        car_page = session.get(url=f"{config.BASE_URL}{car_url}", headers=headers)
        car_content = BeautifulSoup(car_page.content, "html.parser")
        car_images = car_content.find("div", class_="carousel-inner").find_all("img", src=True)
        folder_name = f"{car_manufacturer.strip()}_{car_model.strip()}_{car_year.strip()}"
        print(folder_name)
        for image in car_images:
            if "bannerimages" not in str(image).lower():
                filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
                file_path = f"{config.DATASET_FOLDER}/{folder_name}"
                Path(file_path).mkdir(parents=True, exist_ok=True)
                with open(f"{file_path}/{filename}.jpg", "wb") as w:
                    w.write(session.get(url=f"{config.BASE_URL}{image['src']}").content)
                    time.sleep(1)

        time.sleep(1)
