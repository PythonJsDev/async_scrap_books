import asyncio
from bs4 import BeautifulSoup
from httpx import AsyncClient
from time import time
import os

import constants as csts
from async_scrap_category import scrap_category
from utils import scrap, record_csv


async def scrap_urls_categories(session: AsyncClient) -> list:
    response = await scrap(csts.URL_SITE, session=session)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")
    a_list = soup.find('ul', {"class": "nav nav-list"}).find_all('a')[1:]
    return [csts.URL_SITE + '/' + url['href'] for url in a_list]


async def scrap_images(url_image: str, session: AsyncClient) -> list:
    return await scrap(url_image, session=session)


async def main():
    start = time()
    os.makedirs(csts.PATH_DATA, exist_ok=True)
    os.makedirs(csts.PATH_DATA_CSV, exist_ok=True)
    os.makedirs(csts.PATH_DATA_IMG, exist_ok=True)

    tasks = []
    tasks_image = []
    urls_images = []
    async with AsyncClient() as session:
        urls_categories = await scrap_urls_categories(session=session)
        for url in urls_categories:
            tasks.append(scrap_category(url, session))
        datas = await asyncio.gather(*tasks)
        for data in datas:
            urls_images.extend([data[1:][i].get('image_url') for i in range(len(data[1:]))])

        for url in urls_images:
            tasks_image.append(scrap_images(url, session))
        files_image = await asyncio.gather(*tasks_image)

    for data in datas:
        record_csv(csts.PATH_DATA_CSV, data[0], data[1:])

    for img, file in enumerate(files_image):
        img_name = "image_" + str(img) + ".jpg"
        with open(os.path.join(csts.PATH_DATA_IMG, img_name), 'wb') as picfile:
            picfile.write(file.content)
    print(f"finished scraping in: {time() - start:.1f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
