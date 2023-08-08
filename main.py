import requests
from bs4 import BeautifulSoup, Tag
from typing import List
import json
import csv

def get_html(url: str):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        raise Exception('Сайт не отвечает')


def get_soup(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_cards_from_soup(soup: BeautifulSoup) -> List[Tag]:
    cards = soup.find_all('div', {'class': 'dep-item'})
    return cards


def get_data_from_cards(cards: List[Tag]) -> List[dict]:
    data = []
    for card in cards:
        try:
            people = {
                'full_name': card.find('a', {'class': 'name'}).text,
                'fraction': card.find('div', {'class': 'info'}).text,
                'phone': card.find('div', {'class': 'bottom-info'}).find('a', {'class': 'phone-call'}).get('href'),
                'email': card.find('div', {'class': 'bottom-info'}).find('a', {'class': 'mail'}).get('href'),
            }
            data.append(people)
        except Exception:
            people['phone'] = 'нет номера телефона'
            people['email'] = 'нет почты'
        
    return data



# def get_all_pages(html) -> List[Tag]:
#     soup = BeautifulSoup(html, 'lxml')
#     pages_div = soup.find('div', {'class': 'pagination mt-60'})
#     pages_a = pages_div.find_all('a', {'class': 'item'})
#     pages_a_list = list(pages_a)
#     # print(pages_a_list)
#     print(dir(pages_a_list))

def write_to_json(data: List[Tag]):
    with open('deputaty.json', 'w') as deputs:
        json.dump(data, deputs, indent= 4, ensure_ascii= False)


def write_to_csv(data: List[Tag]):
    with open('deputaty.csv', 'w') as deputs:
        fieldsnames = data[0].keys()
        writer = csv.DictWriter(deputs, fieldnames=fieldsnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    url = 'http://kenesh.kg/ru/deputy/list/35'
    pages = '?pages'
    html = get_html(url)
    # get_all_pages(html)
    soup = get_soup(html)
    cards = get_cards_from_soup(soup)
    data = get_data_from_cards(cards)
    write_to_json(data)
    write_to_csv(data)
    print(data)

if __name__ == '__main__':
    main()