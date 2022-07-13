from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup

isFirstTimeLoad = True

themes = ['world', 'politics', 'science']
url = 'https://ria.ru/services/{}/more.html?date={}'
mainLink = 'https://ria.ru'

result = []

dateStart = date(2015, 12, 31)
dateEnd = date(2016, 1, 16)


def make(text):
    return text.replace('\xa0', ' ').replace('\n', ' ').lower()


ans = input('load last state? y/n')

for theme in themes:
    dateTemp = dateEnd
    nextUrl = url.format(theme, dateTemp.strftime('%Y%m%d'))
    if isFirstTimeLoad:
        if ans == 'y':
            nUrl = input('Введите url: ')
            if nUrl.split('/')[4] != theme:
                continue
            nextUrl = nUrl
            tt = nUrl.split('date=')[1].split('T')[0]
            dateTemp = date(int(tt[:4]), int(tt[4:6]), int(tt[6:]))
        isFirstTimeLoad = False
    print(nextUrl)
    while dateTemp.toordinal() > dateStart.toordinal():
        try:
            data = requests.get(nextUrl)
        except Exception:
            print('Main error occurred', nextUrl)
            continue
        soup = BeautifulSoup(data.text, 'html.parser')
        nextUrl = mainLink + soup.find('div', {'class': 'list-items-loaded'})['data-next-url']
        allItems = soup.find_all('div', {'class': 'list-item'})
        for item in allItems:
            link = item.find('a', {'class': 'list-item__content'})['href']
            try:
                if 'http' in link:
                    articleData = requests.get(link)
                else:
                    articleData = requests.get(mainLink + link)
            except Exception:
                print('Error occurred', nextUrl)
                continue
            articleSoup = BeautifulSoup(articleData.text, 'html.parser')
            title = articleSoup.find('h1', {'class': 'article__title'}).text
            allText = articleSoup.find_all('div', {'class': 'article__text'})
            allText = [i.text for i in allText]
            allText = [i.strip() for i in allText]
            allText = ' '.join(allText)
            allText = allText[allText.find('. ') + 2:]
            result.append({'theme': theme, 'title': make(title), 'text': make(allText)})
            print(dateTemp, result[-1])
        tt = str(nextUrl).split('date=')[1].split('T')[0]
        dateTemp = date(int(tt[:4]), int(tt[4:6]), int(tt[6:]))
        print(nextUrl, dateTemp, tt)
        newData = pd.DataFrame(result)
        try:
            pastData = pd.read_csv(theme + '.csv').drop(columns=['Unnamed: 0'])
            finData = pd.concat([pastData, newData], axis=0, sort=False)
            finData.to_csv(theme + '.csv')
            print('File saved!')
        except Exception:
            newData.to_csv(theme + '.csv')
            print('File updated!')

        result = []
