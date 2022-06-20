#!/Users/jack/Documents/projects/22-chinese/venv/bin/python3

import sqlite3

db = "/Users/jack/Documents/projects/22-chinese/zhong-wen.db"

def vocab_table():
    """create the table to load all vocab into"""
    con = sqlite3.connect(db)
    cur = con.cursor()
    with con:
        cur.execute("""CREATE TABLE IF NOT EXISTS Vocab (
                       ID INTEGER PRIMARY KEY,
                       Pack TEXT,
                       Zi TEXT NOT NULL,
                       PinYin TEXT NOT NULL,
                       Trans TEXT NOT NULL,
                       Grammar TEXT)""")
    con.close()

def sentence_structure_table():
    """create the table to save sentence structures into"""
    con = sqlite3.connect(db)
    cur = con.cursor()
    with con:
        cur.execute("""CREATE TABLE IF NOT EXISTS Structures (
                       ID INTEGER PRIMARY KEY,
                       Pack TEXT,
                       Structure TEXT NOT NULL,
                       Translation TEXT NOT NULL,
                       Notes TEXT)""")
    con.close()


def ju_zi_table():
    """create the table to save all sentences into"""
    con = sqlite3.connect(db)
    cur = con.cursor()
    with con:
        cur.execute("""CREATE TABLE IF NOT EXISTS Ju_Zi (
                       ID INTEGER PRIMARY KEY,
                       Structure TEXT,
                       Zi TEXT,
                       Ju_Zi TEXT,
                       Translation TEXT,
                       Valid INT)""")
    con.close()

vocab_table()
sentence_structure_table()
ju_zi_table()
