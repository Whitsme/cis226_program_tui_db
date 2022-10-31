"""
Aaron Whitaker
10/30/2022
CRN: 10235
Class name: CIS 226: Advanced Python Programming
Aprox time to complete: 15 hours
"""
from signal import pause
from tkinter import Widget
from turtle import delay
from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.message import Message, MessageTarget
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Static, Button, Input, DataTable
from textual import events

import sqlite3
import time

conn = sqlite3.connect(':memory:')
c = conn.cursor()

name = ""
quantity = 0

INSERT: object = Button("Insert", id="insert")
SELECT: object = Button("Select", id="select")
CREATE: object = Button("Create", id="create")
ERROR: object = Static("error", id="error")
WARNING: object = Static("warning", id="warning")
CONFIRM: object = Static("confirm", id="confirm")
OUTPUT: object = Static("No Vegetables Here!")
VEGETABLE: object = Input(placeholder="Enter vegetable", id="vegetable")
QUANTITY: object = Input(placeholder="Enter quantity", id="quantity")

import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

def setup() -> bool:
    # builds database
    try: 
        c.execute("CREATE TABLE IF NOT EXISTS vegetable (name text, quantity integer)")
        conn.commit()
        if CONFIRM.display == True:
            CONFIRM.display = False
        CONFIRM.update(renderable="Database created!")
        return True
    except:
        return False

def insert_vegetable( name, quantity):
    # inserts a vegetable and quantity into the database
    try:
        c.execute("INSERT INTO vegetable VALUES (?, ?)", [name, quantity])
        OUTPUT.update(renderable=f"\nAdded {name} as a new vegetable.")
        return True
    except:
        ERROR.update(renderable=f"\nError inserting {name} into database.")
        return False

def select_vegetable(name, quantity) -> bool:
    # finds vegetable in database or notify user if not found
    c.execute("SELECT quantity, name FROM vegetable WHERE name=?", [name, ])
    row = c.fetchone() 
    if name == "":
        name = "Vegetable"
    if row is None:
        ERROR.update(renderable=f"{name} not found!")
        return False
    else:
        OUTPUT.update(renderable=f"{row[0]} found! {row[1]} in stock.")
        return True
    
        

def update_vegetable( name, quantity):
    # updates vegetable name and/or quantity in database
    found = select_vegetable(name, quantity)
    if found:
        c.execute("UPDATE vegetable SET quantity=? WHERE name=?", [quantity, name])
    else:
        CONFIRM.update(renderable=f"\nAdding {name} as a new vegetable.")
        insert_vegetable(name, quantity)
        c.execute("UPDATE vegetable SET quantity=? WHERE name=?", [quantity, name])
        select_vegetable(name, quantity)

def delete_vegetable(name, quantity):
    # deletes vegetable from database
    if select_vegetable(name, quantity):
        found = c.execute("SELECT quantity, name FROM vegetable WHERE name=?", [name, ])
        c.execute("DELETE FROM vegetable WHERE name=?", [name])
        conn.commit()
        CONFIRM.update(renderable=f"\n{name} deleted!")
        
def show_all():
    # prints all vegetables in database
    print("\nAll vegetables: quantities")
    for row in c.execute("SELECT * FROM vegetable"):
        DataTable.add_row(f"Vegetable = {row[0]}: Quantity = {row[1]}")


def db_check() -> bool:
    # checks if database has been created
    try:
        c.execute("SELECT * FROM vegetable")
        return True
    except:
        return False

def display_error():
    if ERROR.display == False:
        if CONFIRM.display == True:
            CONFIRM.display = False
        if WARNING.display == True:
            WARNING.display = False
        ERROR.display = True

def display_warning():
    if WARNING.display == False:
        if CONFIRM.display == True:
            CONFIRM.display = False
        if ERROR.display == True:
            ERROR.display = False
        WARNING.display = True

def display_confirm():
    if CONFIRM.display == False:
        if ERROR.display == True:
            ERROR.display = False
        if WARNING.display == True:
            WARNING.display = False
        CONFIRM.display = True

class TuiGrid(App):
    CSS_PATH = "grid.css"

    def compose(self) -> ComposeResult:
        yield Container(
                Horizontal(
                    Static("Vegetable Stand"),
                    id="header",
                ),
                Container(
                    Container(
                        INSERT,
                        SELECT,
                        CREATE,
                        id="top-left",
                    ),
                    Container(
                        VEGETABLE,
                        QUANTITY,
                        Container(
                            ERROR,
                            WARNING,
                            CONFIRM,
                            id="middle-pane",
                        ),
                        id="top-right",
                    ),
                    Vertical(OUTPUT, DataTable(), id="output"),
                    id="app-grid",
                ),
                Horizontal(
                    Static("@ 2022 AWW"),
                    id="footer",
                ),
                )
                
    def on_mount(self):
        ERROR.display = False
        WARNING.display = False
        CONFIRM.display = False
        table = self.query_one(DataTable)
        table.add_columns('Vegetables', 'Quantity')
        DataTable.display=False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """buttons and their function calls etc"""
        button_id = event.button.id

        if button_id == "create":
            if setup() == True:
                display_confirm()
            elif setup() == False:
                if ERROR.display == True:
                    ERROR.display = False
                ERROR.update(renderable="ERROR\n\nNo Database Created!")
                display_error()
 
        elif button_id == "insert":
            if db_check() == True:
                name = ""
                quantity = 0
                if VEGETABLE.value != "":
                        name = VEGETABLE.value
                else:
                    ERROR.update(renderable="ERROR\n\nNo Vegetable Entered!")
                    display_error()
                if QUANTITY.value != "":
                    quantity = VEGETABLE.value
                else:
                    ERROR.update(renderable="ERROR\n\nNo Quantity Entered!")
                    display_error()
                CONFIRM.update(renderable=f"\nAdding {name} as a new vegetable.")
                if insert_vegetable(name, quantity) == True:
                    display_confirm()
                else:
                    display_error()
            elif db_check() == False:
                if ERROR.display == True:
                    ERROR.display = False
                ERROR.update(renderable="No Database Available!\nPlease create a database.")
                display_error()

        elif button_id == "select":
            if db_check() == True:
                if VEGETABLE.value != "":
                    name = VEGETABLE.value
                else:
                    name = ""
                quantity = 0
                if VEGETABLE.value == "":
                    if VEGETABLE.value == "":                    
                        WARNING.update(renderable="WARNING\n\nEnter a quantity.")
                    display_warning()
                CONFIRM.update(renderable=f"Looking for a {name}...")
                if select_vegetable(name, quantity) == True:
                    display_confirm()
                else:
                    display_error()
        
            elif db_check() == False:
                if ERROR.display == True:
                    ERROR.display = False
                ERROR.update(renderable="No Database Available!\nPlease create a database.")
                display_error()

if __name__ == "__main__":
    app = TuiGrid(css_path="grid.css")
    app.run()


"""
Design: I intended to use the textual library again. It had been updated to version 0.2.1. Documentation was released with the v0.2.0 release. 
Develop: I did indeed use the textual library. Some of the changes took time to adapt. The documentation was helpful, but there are many ways to accomplish a task in textual. 
Test: I tested all the buttons, input, visibility changes, etc. I also tested the buttons with input's added vs left blank. Testing is still manual at this point.
Documentation: The above program is to build, update, and read data to and from a database via terminal user interface. Adjustments can be made to color, position, etc via the included css file.  
"""


