import nltk
import random

categories = {'cosmetics': 'Косметология', 'medicine': 'Медицина', 'fitnes': 'Фитнес', 'games': 'Компьютерные игры', 'theatre': 'Театр', 'films': 'Кино', 'hoby': 'Отдых и развлечения', 'economics': 'Экономика', 'companies': 'Крупные компании', 'e-cont': 'E-Contneta', 'startup': 'Стартапы', 'bussines': 'Бизнес', 'eco_buss': 'Экономика и бизнес', 'out_politic': 'Внешняя политика', 'in_politic': 'Внутренняя политика', 'goto': 'GoTo', 'extra_edu': 'Дополнительное образование', 'university': 'Высшее образование', 'school': 'Школьное образование', 'education': 'Образование', 'literature': 'Литература', 'ml': 'Анализ данных', 'bb': 'Биоинформатика', 'informatics': 'Информатика', 'math': 'Математика', 'chemistry': 'Химия', 'physics': 'Физика', 'science': 'Наука', 'edu_sci': 'Наука и образование'}

key_words = open('key_words.txt', 'w')

#импортируем обучающую выборку
f = open('feeds_list.txt', 'r')
#создаем сет из всех встречающихся слов
all_words = set(f.read().split())

for researched_cat in categories.keys():
    #создаем массив, на котором алгоритм будет обучаться
    training_set = []

    #считываем данные еще раз, построчно. данные представлены в формате "КАТЕГОРИЯ - ТЕКСТ"
    f.seek(0)
    #категория первого текста
    category = f.readline()
    while category:
        item = f.readline()
        word_set = set(item.split())
        features = {}
        #для каждого слова, встречающегося в файле, запишем, есть ли оно в рассматриваемом тексте
        for w in all_words:
            features[w] = (w in word_set)
        if researched_cat in category:
            training_set.append((features, 1))
        else:
            training_set.append((features, 0))
        category = f.readline()

    random.shuffle(training_set)
    #N = 80 # размер выборки, на которой будет проводиться обучение
    #test_set, train_set = training_set[:N], training_set[N:]
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    #print(researched_cat + ': ' + str(nltk.classify.accuracy(classifier, test_set)))
    top_words = list(classifier.most_informative_features(30))
    key_words.write(categories[researched_cat] + '\n')
    for tup in top_words:
        if tup[1] == True:
            key_words.write(tup[0] + ' ')
    key_words.write('\n')

f.close()
key_words.close()