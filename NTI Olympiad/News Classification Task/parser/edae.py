import csv

import requests
from bs4 import BeautifulSoup

final = [['theme', 'title', 'text']]


def find_dot(stroka):
    count = 0
    for i in stroka:
        if i == '.':
            return stroka[count + 2:]
        count += 1
    return stroka


def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            try:
                writer.writerow([str(i) for i in line])
            except:
                pass


def make(num):
    if len(str(num)) == 1:
        return '0' + str(num)
    else:
        return str(num)


def minus_one_day(whole):
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    whole = [int(i) for i in whole]
    if whole[2] == 1:
        if whole[1] == 1:
            return [str(whole[0] - 1), '12', '31']
        else:
            return [str(whole[0]), make(whole[1] - 1), str(days_in_month[whole[1] - 1])]
    else:
        return [str(whole[0]), make(whole[1]), make(whole[2] - 1)]


main_link = 'https://ria.ru'
themes = ['culture', 'economy', 'society', 'religion', 'world', 'politics', 'science']
url = 'https://ria.ru/services/{}/more.html?id=1547948333&date={}T180000'
for theme in themes:
    date = ['2016', '01', '15']
    while date[2] != '31':
        try:
            data = requests.get(url.format(theme, ''.join(date)))
            soup = BeautifulSoup(data.text, 'html.parser')
            all_items = soup.find_all('div', {'class': 'list-item'})
            for item in all_items:
                link = item.find('a', {'class': 'list-item__content'})['href']
                url_link = main_link + link
                if 'http' in link:
                    article_data = requests.get(link)
                else:
                    article_data = requests.get(main_link + link)
                article_soup = BeautifulSoup(article_data.text, 'html.parser')
                title = article_soup.find('h1', {'class': 'article__title'}).text
                title = title.replace('\xa0', ' ').lower()
                title = title.replace('\u200d', ' ')
                all_text = article_soup.find_all('div', {'class': 'article__text'})
                all_text = [i.text for i in all_text]
                all_text = [i.replace('\xa0', ' ').lower() for i in all_text]
                all_text = [i.strip() for i in all_text]
                all_text = ' '.join(all_text)
                all_text = find_dot(all_text)
                all_text = all_text.replace('\u200d', ' ')
                all_text = all_text.replace('\n', ' ')
                if [theme, title, all_text] not in final and theme and title and all_text:
                    final.append([theme, title, all_text])
                print(*date, final[-1])
        except:
            print('kek')
        date = minus_one_day(date)

    csv_writer(final, theme + '.csv')
    final = [['theme', 'title', 'text']]
