import csv
import spacy

from itertools import product


nlp = spacy.load('de_core_news_sm')


def read_data(data_dir):
    data = []
    with open(data_dir) as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            print(row)
            assert len(row)==3
            data.append((row[0], row[1], row[2]))
    return data


def compare_sentences(text1, text2):
    sentences1 = nlp(text1).sents
    sentences2 = nlp(text2).sents
    for sen1, sen2 in product(sentences1, sentences2):
        sim = sen1.similarity(sen2)
        if sim > 0.9:
            print('!!!')
            print(sim)
            print(sen1)
            print(sen2)


def get_sim_count(sentences1, sentences2):
    sim_counter = 0
    for sen1, sen2 in product(sentences1, sentences2):
        sim = sen1.similarity(sen2)
        if sim > 0.9:
            sim_counter = sim_counter + 1
    return sim_counter


def is_plag(text1, text2):
    sentences1 = (nlp(text1)).sents
    s1copy = (nlp(text1)).sents
    sentences2 = (nlp(text2)).sents
    sim_count = get_sim_count(sentences1, sentences2)
    number_sentences_in_text1 = sum(1 for _ in s1copy)
    if (number_sentences_in_text1 * 0.8) <= sim_count:
        return 'True, number of sentences in text1 : ' + str(number_sentences_in_text1), 'similarity count: ' + str(sim_count)
    else:
        return 'False, number of sentences in text1 : ' + str(number_sentences_in_text1), 'similarity count: ' + str(sim_count)


data = read_data('train_plag_data.txt')

count = 0
plags = []
no_plags = []
for i in range(data.__len__()):
    count = count+1
    triple = data.pop(0)
    kind = int(triple.__getitem__(0))
    is_a_plag = is_plag(triple.__getitem__(1), triple.__getitem__(2))
    if kind == 1:
        plags.append(('article pair: ' + str(count), 'is_a_plag: ' + str(is_a_plag)))
    else:
        if kind == 0:
            no_plags.append(('article pair: ' + str(count), 'is_a_plag: ' + str(is_a_plag)))

    #compare_sentences(triple.__getitem__(1), triple.__getitem__(2))


print('Plagiarisms are: ')
print(plags)

print('Not a Plagiarism is: ')
print(no_plags)

''' Not a Plagiarism = 0 '''
''' Not a Plagiarism = 1 '''
