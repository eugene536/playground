#!/usr/bin/python3

"""
sudo apt install python3-nltk python3-matplotlib translate-shell
import nltk
nltk.download('stopwords')
nltk.download ('punkt')
nltk.download('wordnet')

mkvinfo film_name.mkv # found number of track with english subtitles
mkvextract tracks film_name.mkv track_number:subtitle_new_file_name.txt
"""

import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.stem.wordnet import WordNetLemmatizer
import matplotlib.pyplot as plt
import re
patterns = [r'\<.*?\>']


ps = PorterStemmer()
lem = WordNetLemmatizer()
stop_words = stopwords.words('english')

path = sys.argv[1]

# basic_words = open("basic_words").read().splitlines()
# basic_words = set(list(map(ps.stem, basic_words)))

with open(path) as f:
    txt = f.read()
    for p in patterns:
        txt = re.sub(p, '', txt)

    for c in ['\0', '(', '[', ')', ']', ',', '♪', ':', '.', '-', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '"', '/']:
        txt = txt.replace(c, '')


    words = [x.lower() for x in txt.split()]
    words = [x.split("'")[0] for x in words]
    words = [w for w in words if w not in stop_words]
    fdist = FreqDist(words)

    stem_words = set()
    new_words = []

    for w in fdist:
        s_w = ps.stem(w)
        l_w = lem.lemmatize(w, "v")

        if s_w not in stem_words and l_w not in stem_words:
            #if s_w not in basic_words:
          new_words.append(w)

        stem_words.add(s_w)
        stem_words.add(l_w)

    print("\n".join(new_words))


