import csv
import requests
from bs4 import BeautifulSoup

# Создаем CSV файл и открываем его для записи
with open('CSV.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    # Записываем новые заголовки CSV файла
    writer.writerow(['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена', 'Ссылка'])

    # Список URL всех категорий
    category_urls = [
        'https://parsinger.ru/html/index1_page_1.html',
        'https://parsinger.ru/html/index2_page_1.html',
        'https://parsinger.ru/html/index3_page_1.html',
        'https://parsinger.ru/html/index4_page_1.html',
        'https://parsinger.ru/html/index5_page_1.html'
    ]

    # Обходим каждую категорию
    for category_url in category_urls:
        # Получаем количество страниц в текущей категории
        response = requests.get(category_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = soup.find('div', class_='pagen')
        num_pages = len(pages.find_all('a')) if pages else 1

        # Обходим каждую страницу в текущей категории
        for page_num in range(1, num_pages + 1):
            page_url = f"{category_url.split('_')[0]}_page_{page_num}.html"
            response = requests.get(page_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # Извлекаем ссылки на карточки товаров
            product_links = [link['href'] for link in soup.select('.sale_button a')]

            # Обходим каждую ссылку на карточку товара
            for product_link in product_links:
                # Получаем данные о товаре со страницы карточки
                product_page_url = f"https://parsinger.ru/html/{product_link}"
                product_response = requests.get(product_page_url)
                product_response.encoding = 'utf-8'
                product_soup = BeautifulSoup(product_response.text, 'html.parser')

                # Извлекаем данные о товаре
                name = product_soup.find('p', id='p_header').text.strip()
                article = product_soup.find('p', class_='article').text.split(': ')[1].strip()
                brand = product_soup.find('li', id='brand').text.split(': ')[1].strip()
                model = product_soup.find('li', id='model').text.split(': ')[1].strip()
                in_stock = product_soup.find('span', id='in_stock').text.split(': ')[1].strip()
                price = product_soup.find('span', id='price').text.strip()
                old_price = product_soup.find('span', id='old_price').text.strip()

                # Записываем данные в CSV
                writer.writerow([name, article, brand, model, in_stock, price, old_price, product_page_url])

print('Файл CSV.csv создан')
