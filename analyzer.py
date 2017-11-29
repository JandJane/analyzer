import urllib.request
from bs4 import BeautifulSoup
import pymorphy2
import nltk
import math

url = str(input('Введите url: '))

#парсим HTML код с указанного url
site = urllib.request.urlopen(url)
html = site.read()

#очищаем от HTML-тегов
soup = BeautifulSoup(html, 'html.parser')
raw = soup.get_text()
#добавляем к данных title, содержимое тэгов h и мета-тегов с разными весами
raw += 10 * soup.title.string
#очищаем строку от знаков препинания и приводим к нижнему регистру
for symbol in ',.!?«»:;()':
    raw = raw.replace(symbol, '')
raw = raw.lower()
#отделим от всех слов английские и те технические, которые все-таки затесались
all_words = list(raw.split())
words = []
for word in all_words:
    if word[0] in 'йцукенгшщзхфвапролджэячсмитбю':
        words.append(word)

#приведем слова к нормальной форме
morph = pymorphy2.MorphAnalyzer()
for i in range(len(words)):
    words[i] = morph.parse(words[i])[0].normal_form

lenght = len(words)

f = open('key_words.txt', 'r')
states = {}
category = f.readline()
while category:
    key_words = list(f.readline().split())
    state = 0
    for w in key_words:
        state += words.count(w) / lenght
    states[category[:-1]] = state
    category = f.readline()

f.close()

# вывод данных

states['Отдых и развлечения'] = states['Отдых и развлечения'] + states['Кино'] + states['Театр'] + states['Компьютерные игры']
states['Здоровье и красота'] = states['Фитнес'] + states['Медицина'] + states['Косметология']
states['Стартапы'] = states['Стартапы'] + states['E-Contneta']
states['Бизнес'] =  states['Бизнес']  + states['Стартапы'] + states['Крупные компании']
states['Экономика и бизнес'] = states['Экономика и бизнес'] + states['Экономика'] + states['Бизнес']
states['Политика'] =  states['Внутренняя политика'] + states['Внешняя политика']
states['Дополнительное образование'] = states['Дополнительное образование'] + states['GoTo']
states['Образование'] =  states['Образование'] + states['Школьное образование'] + states['Высшее образование'] + states['Дополнительное образование']
states['Информатика'] = states['Информатика'] + states['Биоинформатика']  + states['Анализ данных']
states['Наука'] = states['Наука'] + states['Математика'] + states['Физика'] + states['Химия'] + states['Информатика']
states['Наука и образование'] = states['Наука и образование'] + states['Наука'] + states['Образование']

categories = states.keys()
for category in categories:
    states[category] = min(10, math.ceil(states[category] * 1000))

for n in range(10, -1, -1):
    for category in categories:
        if states[category] == n:
            print(category + ': ' + str(states[category]))












