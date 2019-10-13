# coding: utf-8


from pathlib import Path
import string
from itertools import chain
from functools import reduce
from random import choice
from collections import Counter
import re
import sys


def read_articles(p):
    for p in path.iterdir():
        yield p.read_text()

def is_bangla(ch):
    return ch == '।' or ch >= "\u0980" and ch <= "\u09ff" and ch != "\u09e4"


def is_bangla_or_punctuation_or_whitespace(ch):
    return is_bangla(ch) or (ch in string.punctuation + "‘’") or (ch in string.whitespace)


def filter_except_bangla_and_punctuation_and_whitespace(s):
    return ''.join(ch if is_bangla_or_punctuation_or_whitespace(ch) else ' ' for ch in s)


def sentence_tokenize(article):
    dari = '।'
    return filter_except_bangla_and_punctuation_and_whitespace(article).split(dari)


def mean(a): return sum(a) / len(a) if len(a) else 0


def average_sentence_count(articles):
    return mean(list(map(lambda a: len(sentence_tokenize(a)), articles)))


def unique_sentences_in_articles(articles):
    return set(sentences for a in articles for sentences in sentence_tokenize(a))


def filter_zerowidth(s):
    return s.translate(str.maketrans('', '', "\u200b\u200c\u200d\ufeff"))


def filter_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation + "‘’"))


def pad_punctuation_with_space(s):
    return ''.join(" {} ".format(ch) if ch in string.punctuation + "‘’" else ch for ch in s)


def filter_english(s):
    return s.translate(str.maketrans('', '', string.ascii_letters))


def filter_english_digit(s):
    return s.translate(str.maketrans('', '', string.digits))


def word_tokenize(sentence):
    return pad_punctuation_with_space(filter_except_bangla_and_punctuation_and_whitespace(sentence)).split()


def words_in_article(article):
    return chain(*list(map(word_tokenize, sentence_tokenize(article))))


path = Path(sys.argv[1])


articles = list(read_articles(path))


unique_chars = set(ch for article in articles for ch in article)


all_chars = ''.join(unique_chars)


print(filter_except_bangla_and_punctuation_and_whitespace(all_chars))


unique_words = Counter(
    word for article in articles for word in words_in_article(article))


print('Unique words: {}'.format(len(unique_words)))

for w in unique_words.most_common(100):
    print(w)

print('Average word length: {}'.format(mean(list(map(len, unique_words)))))


sentences = unique_sentences_in_articles(articles)


print('Average sentence per article: {}'.format(average_sentence_count(articles)))


print('Unique sentence count: {}'.format(len(sentences)))
