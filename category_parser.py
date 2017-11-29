import urllib.request
from bs4 import BeautifulSoup
import pymorphy2

urls = ['',
        '',
        '']
category = ''


f = open('feeds_list.txt', 'a')
for url in urls:
    # парсим HTML код с указанного url
    site = urllib.request.urlopen(url)
    html = site.read()

    # очищаем от HTML-тегов, знаков препинания и приводим строку к нижнему регистру
    soup = BeautifulSoup(html, 'html.parser')
    raw = soup.get_text()
    for symbol in ',.!?«»:;()':
        raw = raw.replace(symbol, '')
    raw = raw.lower()

    # отделим от всех слов английские и те технические, которые все-таки затесались
    all_words = list(raw.split())
    words = []
    for word in all_words:
        if word[0] in 'йцукенгшщзхфвапролджэячсмитбю':
            words.append(word)

    # приведем слова к нормальной форме
    morph = pymorphy2.MorphAnalyzer()
    for i in range(len(words)):
            words[i] = morph.parse(words[i])[0].normal_form

    f.write(category + '\n')
    f.write(' '.join(map(str, words)) + '\n')
f.close()
