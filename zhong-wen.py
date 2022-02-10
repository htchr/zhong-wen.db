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
        for i, l in enumerate(lists, 1):
            print(str(i) + ": " + l)
        new_list_i = ask_for_int("enter the index of the new list, enter '0' to quit: ")
        if new_list_i == 0:
            return
        path = csvs + lists[new_list_i - 1]
    filename = path.split('/')[-1].split('.')[0] #isolate filename without '.csv'
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    vocab = []
    with open(path, newline='') as csvfile:
        c_row = csv.reader(csvfile, delimiter=';')
        for r in c_row:
            # confirm the word is not a duplicate inside the db
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
    support function to search through pinyin easier
    generate list of tone permutations for a given pinyin
    assumes only one tone is present in the string
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

def ask_for_int(message):
    """
    support function to ask users for an integer
    to use in place of regular input() method
    ---
    message: string asking the user for an integer
    returns i: user input integer
    """
    while True:
        i = input(message)
        try:
            i = int(i)
            return i
        except:
            print("please enter an integer")

def edit_vocab(i=0, zi='', pinyin='', trans='', gram=''):
    """
    edit a row of the Vocab table
    ---
    i: integer of the primary key of the row to edit
    zi: string of the new chinese character to use
    pinyin: string of new pinyin
    trans: string of new translation
    gram: string of new grammar notes
    returns: tuple of the editted row
    """
    if i == 0:
        i = ask_for_int("enter the index of the row to edit, enter '0' to quit: ")
    if i == 0:
        return
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    with con:
        cur.execute("SELECT * FROM Vocab WHERE ID = ?", (i,))
    row = cur.fetchone()
    # map of col name to old and new values
    properties = {'zi': [zi, row[2]], 
                  'pinyin': [pinyin, row[3]],
                  'trans': [trans, row[4]],
                  'gram': [gram, row[5]]}
    if __name__ == '__main__':
        # if in command line ui: ask for new values
        print(row)
        for key in properties:
            print(key + ": " + properties[key][1])
            new = input("change " + key + ", leave blank to keep current value: ")
            if new == '':
                continue
            else:
                properties[key][0] = new
    # if new value == '', use old value, else new value
    update = []
    for key in properties:
        if properties[key][0] != '':
            update.append(properties[key][0])
        else:
            update.append(properties[key][1])
    with con:
        cur.execute("""UPDATE Vocab 
                       SET Zi = ?,
                           PinYin = ?,
                           Trans = ?,
                           Grammar = ?
                       WHERE ID = ?""",
                    (update[0], update[1], update[2], update[3], i))
    # select same row to return confirmed change
    with con:
        cur.execute("SELECT * FROM Vocab Where ID = ?", (i, ))
    row = cur.fetchone()
    con.close()
    return row

def review_vocab(n=0):
    """
    randomly select n number of words to review
    randomly presents zi / pinyin / translations for review
    user inupts 0 / 1 to progress + keep track of progress
    ---
    n: int of how many words to review
    returns: ratio of correct:incorrect
    """
    if n == 0:
        n = ask_for_int("enter the number of vocab you want to review, enter '0' to quit: ")
    if n == 0:
        return
    correct = 0
    con = sqlite3.connect("zhong-wen.db")
    cur = con.cursor()
    with con:
        cur.execute("SELECT * FROM Vocab ORDER BY random() LIMIT ?", (n,))
    words = cur.fetchall()
    con.close()
    for w in words:
        i = random.randrange(2, 5)
        input(w[i])
        print(w)
        correct += ask_for_int("did you know this word? 0/1: ")
    return correct / n

def write_ju_zi():
    """
    randomly selects 1 sentence structure and 1 word to make a sentence with
    records sentences to sqlite db to review with tutor
    """

def write_sqlite(command=''):
    "directly write to the db"
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
    "command line ui"
    functions = [load_vocab,
                 search_zi, 
                 search_pinyin, 
                 search_trans,
                 edit_vocab,
                 review_vocab,
                 write_ju_zi,
                 write_sqlite]

    for i, f in enumerate(functions, 1):
        print(str(i) + ": " + f.__name__)
    sel = ask_for_int("select function index, enter '0' to quit: ")
    if sel == 0:
        return
    elif sel > len(functions) - 1:
        print("please enter a valid index")
        return
    else:
        print(functions[sel - 1]())

if __name__ == '__main__':
    main()
