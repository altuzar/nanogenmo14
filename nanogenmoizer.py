import urllib2
import re
import sys
from collections import defaultdict
from random import random
import curses
import os
import sys
from subprocess import call
import datetime
import time

# My NaNoGenMo14 submit. Verse novels in spanish, even if it's possible to change the source text
# Credits: 
# And the Python Markov Chain taken from a Hacker News Headline Generator taken somewhere, called hngen.py, but could not find the source. 
# Vicente Huidobro for Altazor, the poetry book. It was published in 1919, so maybe it's legal to distribute it

words_limit = 50000

def sample(items):
    next_word = None
    t = 0.0
    for k, v in items:
        t += v
        if t and random() < v/t:
            next_word = k
    return next_word

def get_samples(markov_map,lookback,limit):
    sentences = []
    while len(sentences) < limit:
        sentence = []
        next_word = sample(markov_map[''].items())
        while next_word != '':
            sentence.append(next_word)
            next_word = sample(markov_map[' '.join(sentence[-lookback:])].items())
        sentence = ' '.join(sentence)
        flag = True
        for title in titles: #Prune titles that are substrings of actual titles
            if sentence in title:
                flag = False
                break
        if flag:
            sentences.append(sentence)
    return sentences

def titlelize(t):
    # Here I should make uppers and remove strange chars or something for the title
    return t.replace(" ","_")

# Here starts this thing
print("Hi.")

archive = open('huidobro_altazor.txt')
titles = archive.read().split("\n")
archive.close()
markov_map = defaultdict(lambda:defaultdict(int))

lookback = 2

#Generate map in the form word1 -> word2 -> occurences of word2 after word1
for title in titles[:-1]:
    title = title.split()
    if len(title) > lookback:
        for i in xrange(len(title)+1):
            markov_map[' '.join(title[max(0,i-lookback):i])][' '.join(title[i:i+1])] += 1

#Convert map to the word1 -> word2 -> probability of word2 after word1
for word, following in markov_map.items():
    total = float(sum(following.values()))
    for key in following:
        following[key] /= total

title_time_stamp = str(int(time.time()))
the_title = get_samples(markov_map,lookback,1)
out_file = title_time_stamp + "_o_" + titlelize( the_title[0] ) + ".txt"

print("Generating the following novel with " + str(words_limit) + " words: " + out_file)

open(out_file,"a").write(title_time_stamp + " o " + the_title[0] + "\n\n")

words = 0
lines = []
while words < words_limit:
    a_line = ""
    while True:
        a_line = get_samples(markov_map,lookback,1)
        # Removes duplicated lines 
        if not a_line[0] in lines:
            words = words + a_line[0].count(" ") + 1
            if words >= words_limit:
                # Last line. Adds a final dot
                a_line[0] = a_line[0] + "."
            lines.append(a_line[0])
            break
    open(out_file,"a").write(lines[len(lines)-1] + "\n")
    if len(lines) > 1 and len(lines) % 1000 == 0:
        print("Working like crazy. Lines: " + str(len(lines)) + ", Words: " + str(words))

print("Novel generated \\o/: " + out_file)
