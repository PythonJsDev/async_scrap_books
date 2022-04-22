import csv

from httpx import AsyncClient


async def scrap(url: str, session: AsyncClient):
    return await session.get(url)


def record_csv(path: str, file_name: str, data_list: list):
    """ sauvegarde la liste des données (liste de dictionnaires) dans un fichier csv """
    separator = '\t'
    quote = "'"
    with open(path + "/" + file_name + ".csv", 'w',
              encoding="utf-8", newline='') as csvfile:
        fieldorder = ["title",
                      "product_description",
                      "universal_product_code (upc)",
                      "price_including_tax",
                      "price_excluding_tax",
                      "number_available",
                      "review_rating",
                      "product_page_url",
                      "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldorder,
                                delimiter=separator,
                                quotechar=quote)
        writer.writeheader()
        for line in data_list:
            writer.writerow(line)
