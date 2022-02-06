#!/Users/jack/Documents/projects/22-chinese/venv/bin/python3

import sqlite3
import os
import csv
import random

def reload_vocab():
    """
    load vocab words from a csv file to sqlite
    stores all vocab in the same table
    populates table from csv
    """
    csvs = "/Users/jack/Documents/projects/22-chinese/csvs/"
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    zi_set = set()
    for c in os.listdir(csvs):
        if c.split('.')[-1] == 'csv':
            path = csvs + c
            filename = c.split('.')[0]
            # extracrt non-duplicates from csv file
            vocab = []
            with open(path, newline='') as csvfile:
                c_row = csv.reader(csvfile, delimiter=';')
                for c in c_row:
                    if c[0] not in zi_set:
                        zi_set.add(c[0])
                        vocab.append(c)
            # remove old versions to refresh
            with con:
                cur.execute("DELETE FROM Vocab WHERE Pack = ?", (filename,))
            # load values from csvs to table
            with con:
                for row in vocab:
                    cur.execute("INSERT INTO Vocab VALUES (NULL,?,?,?,?,?)",
                                (filename, row[0], row[1], row[2], ''))
    con.close()

def search_zi():
    """
    search through the sqlite db for words including a chinese character
    ---
    returns: list of words including zi
    """
    user_zi = input("enter the chinese character you would like to search for, leave blank to quit: ")
    if user_zi == '':
        return
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    with con:
        cur.execute("""SELECT * FROM Vocab WHERE 
                        Zi LIKE (? || '%') 
                        OR Zi LIKE ('%' || ? || '%') 
                        OR Zi LIKE ('%' || ?)""", 
                    (user_zi,user_zi, user_zi))
    words = cur.fetchall()
    con.close()
    if len(words) == 0:
        print("no words found containing " + user_zi)
    for w in words:
        print(w)
        return
    return words

def tone_perms(pinyin):
    """
    support function
    generate list of tone permutations for a given pinyin
    ---
    pinyin: string to generate from
    returns: list of permutations of all tone combinations
    """
    tones = {'a': ('ā', 'á', 'â', 'à'),
             'e': ('ē', 'é', 'ê', 'è'), 
             'i': ('ī', 'í', 'î', 'ì'), 
             'o': ('ō', 'ó', 'ô', 'ò'), 
             'u': ('ū', 'ú', 'û', 'ù')}
    pinyin = pinyin.strip()
    perms = []
    perms.append(pinyin)
    pinyin = list(pinyin)
    for i, char in enumerate(pinyin):
        if char in list(tones.keys()):
            for t in tones[char]:
                pinyin[i] = t
                p = ''
                for c in pinyin:
                    p = p + c
                perms.append(p)
        pinyin = list(perms[0])
    return perms

def search_pinyin():
    """
    search through sqlite db for words including pinyin
    abstract the search to look for all permutations of tones
    ---
    returns: list of words including pinyin
    """
    user_pinyin = input("enter the pinyin you would like to search for, leave blank to quit: ")
    if user_pinyin == '':
        return
    pinyin_perms = tone_perms(user_pinyin)
    words = []
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    for p in pinyin_perms:
        with con:
            cur.execute("""SELECT * FROM Vocab WHERE
                           PinYin LIKE (? || '%')
                           OR PinYin LIKE ('%' || ? || '%')
                           OR PinYin LIKE ('%' || ?)""",
                           (p, p, p))
        rows = cur.fetchall()
        for r in rows:
            words.append(r)
    con.close()
    if len(words) == 0:
        print("no words found using " + "'" + user_pinyin + "'")
        return
    for w in words:
        print(w)
    return words

def search_trans():
    """
    search translations for occurances of given english word
    ---
    returns: list of words including trans
    """

def edit_vocab():
    """
    support function
    edit a row of the Vocab table
    """

def review_vocab():
    """
    randomly select n number of words to review
    randomly presents zi / pinyin / translations for review
    user inupts 0 / 1 to progress + keep track of progress
    ---
    returns: ratio of correct:incorrect
    """

def write_ju_zi():
    """
    randomly selects 1 sentence structure and 1 word to make a sentence with
    records sentences to sqlite db to review with tutor
    """

def write_sqlite():
    """
    directly write to the db
    """
    command = input("enter SQLite command, leave blank to quit: ")
    if command == '':
        return
    con = sqlite3.connect('zhong-wen.db')
    cur = con.cursor()
    try:
        with con:
            cur.execute(command)
    except Exception as e:
        print("could not execute command")
        print(e)
    con.close()

# ui function menu
functions = [reload_vocab,
             search_zi, 
             search_pinyin, 
             search_trans,
             review_vocab,
             write_ju_zi,
             write_sqlite]

for i, f in enumerate(functions):
    print(str(i) + ": " + f.__name__)
sel = input("select function number, leave blank to quit: ")
if sel == '':
    play = False
elif int(sel) > len(functions) - 1:
    print("please enter a number in range")
else:
    functions[int(sel)]()

