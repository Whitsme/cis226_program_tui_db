"""
Aaron Whitaker
10/22/2022
CRN: 10235
Class name: CIS 226: Advanced Python Programming
Aprox time to complete: 8 hours
"""

import sqlite3

from main import setup, insert_vegetable, select_vegetable, update_vegetable, delete_vegetable, show_all


def test_setup(capsys):
    # tests main.setup()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        setup()
        captured = capsys.readouterr()
        assert captured.out == "\nVegetable table created!\n"

def test_insert(capsys):
    # tests main.insert_vegetable()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        insert_vegetable("carrot", 10)
        captured = capsys.readouterr()
        assert captured.out == "\nAdded carrot as a new vegetable.\n"

def test_select(capsys):
    # tests main.select_vegetable()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        select_vegetable("carrot", 10)
        captured = capsys.readouterr()
        assert captured.out == "\ncarrot found!\n10 in stock.\n"

def test_update(capsys):
    # tests main.update_vegetable()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        update_vegetable("turnip", 10)
        captured = capsys.readouterr()
        assert captured.out == "\nturnip not found!\n\nAdding turnip as a new vegetable.\n\nAdded turnip as a new vegetable.\n\nturnip found!\n10 in stock.\n"
        update_vegetable("turnip", 20)
        captured = capsys.readouterr()
        assert captured.out == "\nturnip found!\n20 in stock.\n"
        update_vegetable("celery", 20)
        captured = capsys.readouterr()
        assert captured.out == "\ncelery not found!\n\nAdding celery as a new vegetable.\n\nAdded celery as a new vegetable.\n\ncelery found!\n20 in stock.\n"

def test_show_all_data(capsys):
    # tests main.show_all()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        show_all()
        captured = capsys.readouterr()
        assert captured.out == "\nAll vegetables: quantities\ncarrot: 10\nturnip: 20\ncelery: 20\n"

def test_delete(capsys):
    # tests main.delete_vegetable()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        delete_vegetable("lettuce", 0)
        captured = capsys.readouterr()
        assert captured.out == "\nlettuce not found!\n"
        delete_vegetable("carrot", 10)
        captured = capsys.readouterr()
        assert captured.out == "\ncarrot found!\n10 in stock.\n\ncarrot deleted!\n"
        delete_vegetable("turnip", 20)
        captured = capsys.readouterr()
        assert captured.out == "\nturnip found!\n20 in stock.\n\nturnip deleted!\n"
        delete_vegetable("celery", 20)
        captured = capsys.readouterr()
        assert captured.out == "\ncelery found!\n20 in stock.\n\ncelery deleted!\n"

def test_show_all_no_data(capsys):
    # tests main.show_all()
    with sqlite3.connect(':memory:') as conn:
        c = conn.cursor()
        show_all()
        captured = capsys.readouterr()
        assert captured.out == "\nAll vegetables: quantities\n"