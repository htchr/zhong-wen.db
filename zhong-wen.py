#!/Users/jack/Documents/projects/22-chinese/venv/bin/python3

import sqlite3
import os
import csv
import random

def load_vocab(path=''):
    """
    load vocab words from a user selected csv file to sqlite
    stores all vocab in the same table
    populates table from csv
    ---
    path: string to the location of the new vocab list
    """
    csvs = "/Users/jack/Documents/projects/22-chinese/csvs/"
    if path == '':
        lists = []
        for c in os.listdir(csvs):
            if c.split('.')[-1] == 'csv':
                lists.append(c)
        for i, l in enumerate(lists):
            print(str(i) + ": " + l)
        new_list_i = input("enter the index of the new list, leave blank to quit: ")
        if new_list_i == '':
            return
        path = csvs + lists[int(new_list_i)]
    filename = path.split('/')[-1].split('.')[0] #isolate filename without '.csv'
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    vocab = []
    with open(path, newline='') as csvfile:
        c_row = csv.reader(csvfile, delimiter=';')
        for r in c_row:
            cur.execute("SELECT * FROM Vocab WHERE Zi = ?", (r[0],))
            if len(cur.fetchall()) == 0:
                vocab.append(r)
    with con:
        for word in vocab:
            cur.execute("INSERT INTO Vocab VALUES (NULL,?,?,?,?,?)",
                        (filename, word[0], word[1], word[2], ''))
    con.close()

def search_zi(user_zi=''):
    """
    search through the sqlite db for words including a chinese character
    ---
    user_zi: string of chinese character(s) to search for
    returns: list of words including zi / None
    """
    if user_zi == '':
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

def search_pinyin(user_pinyin=''):
    """
    search through sqlite db for words including pinyin
    abstract the search to look for all permutations of tones
    ---
    user_pinyin: string of english characters (without tones) to look for
    returns: list of words including pinyin / None
    """
    if user_pinyin == '':
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
        return
    return words

def search_trans(user_eng=''):
    """
    search translations for occurances of given english word
    ---
    eng: string of english text to search for in the translations of chinese words
    returns: list of words including trans / None
    """
    if user_eng == '':
        user_eng = input("enter the english text you would like to search for, leave blank to quit: ")
    if user_eng == '':
        return
    user_eng = user_eng.strip()
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    with con:
        cur.execute("""SELECT * FROM Vocab WHERE
                       Trans LIKE (? || '%')
                       OR Trans LIKE ('%' || ? || '%')
                       OR Trans LIKE ('%' || ?)""",
                    (user_eng, user_eng, user_eng))
    words = cur.fetchall()
    con.close()
    if len(words) == 0:
        return
    return words

def edit_vocab():
    """
    support function
    edit a row of the Vocab table
    """

def review_vocab(n=0):
    """
    randomly select n number of words to review
    randomly presents zi / pinyin / translations for review
    user inupts 0 / 1 to progress + keep track of progress
    ---
    n: int of how many words to review
    returns: ratio of correct:incorrect
    """

def write_ju_zi():
    """
    randomly selects 1 sentence structure and 1 word to make a sentence with
    records sentences to sqlite db to review with tutor
    """

def write_sqlite(command=''):
    """directly write to the db"""
    if command == '':
        command = input("enter SQLite command, leave blank to quit: ")
    if command == '':
        return
    con = sqlite3.connect('zhong-wen.db')
    cur = con.cursor()
    try:
        with con:
            cur.execute(command)
    except Exception as e:
        con.close()
        return "could not execute command" + str(e)
    con.close()

def main():
    """command line ui"""
    functions = [load_vocab,
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
        return
    elif int(sel) > len(functions) - 1:
        print("please enter a number in range")
    else:
        print(functions[int(sel)]())

if __name__ == '__main__':
    main()
