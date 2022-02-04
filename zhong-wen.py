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
    for c in os.listdir(csvs):
        if c.split('.')[-1] == 'csv':
            path = csvs + c
            filename = c.split('.')[0]
            # remove old versions to refresh
            with con:
                cur.execute("DELETE FROM Vocab WHERE Pack = ?", (filename,))
            # load values from csvs to table
            with con:
                with open(path, newline='') as csvfile:
                    vocab = csv.reader(csvfile, delimiter=';')
                    for row in vocab:
                        cur.execute("INSERT INTO Vocab VALUES (NULL,?,?,?,?,?)",
                                    (filename, row[0], row[1], row[2], ''))
    con.close()

def search_zi():
    """
    search through the sqlite db for words including a chinese character

    returns: list of words including zi
    """

def tone_perms(pinyin):
    """
    support function
    generate list of tone permutations for a given pinyin
    
    pinyin: string to generate from
    returns: list of permutations of all tone combinations
    """

def search_pinyin():
    """
    search through sqlite db for words including pinyin
    abstract the search to look for all permutations of tones

    returns: list of words including pinyin
    """

def search_trans():
    """
    search translations for occurances of given english word

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
