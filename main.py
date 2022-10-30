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
from textual.widgets import Static, Button, Header, Footer, Input
from textual import events

import sqlite3
import time

conn = sqlite3.connect(':memory:')
c = conn.cursor()
error = ["error"]
warning = ["warning"]
confirm = ["confirm"]
i = [0]
INSERT: object = Button("Insert", id="insert")
SELECT: object = Button("Select", id="select")
CREATE: object = Button("Create", id="create")
ERROR: object = Static(error[0], id="error")
WARNING: object = Static(warning[0], id="warning")
CONFIRM: object = Static(confirm[0], id="confirm")
SUBMIT: object = Button("Submit", id="submit")

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
                        Input(placeholder="Enter vegetable", id="vegetable"),
                        Input(placeholder="Enter quantity", id="quantity"),
                        Container(
                            ERROR,
                            WARNING,
                            CONFIRM,
                            id="middle-pane",
                        ),
                        id="top-right",
                    ),
                    Vertical(
                    *[Static(f"Vertical layout, child {number}") for number in range(4)],
                    id="bottom-pane",
                    ),
                    Vertical(
                        SUBMIT,
                        Static("", id="box2"),
                        Static("", id="box3"),
                        id="right-pane",
                    ),
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

    def animate_button(self) -> None:
        SUBMIT.styles.offset = (1, int(i[0]))


    def on_button_pressed(self, event: Button.Pressed) -> None:

        button_id = event.button.id

        if button_id == "create":
            # setup()
            if CONFIRM.display == True:
                CONFIRM.display = False
            elif CONFIRM.display == False:
                if ERROR.display == True:
                    ERROR.display = False
                if WARNING.display == True:
                    WARNING.display = False
                CONFIRM.display = True
 
        elif button_id == "insert":
            # if self.query(Input.id) == "vegetable":
            #     name = Input.value
            # if self.query(Input.id) == "quantity":
            #     quantity = Input.value
            # insert_vegetable(name, quantity)
            if WARNING.display == True:
                WARNING.display = False
            elif WARNING.display == False:
                if CONFIRM.display == True:
                    CONFIRM.display = False
                if ERROR.display == True:
                    ERROR.display = False
                WARNING.display = True

        elif button_id == "select":
            # if self.query(Input.id) == "vegetable":
            #     name = Input.value
            # if self.query(Input.id) == "quantity":
            #     quantity = Input.value
            # select_vegetable(name, quantity)
            if ERROR.display == True:
                ERROR.display = False
            elif ERROR.display == False:
                if CONFIRM.display == True:
                    CONFIRM.display = False
                if WARNING.display == True:
                    WARNING.display = False
                ERROR.display = True

        elif button_id == "submit":
            if i[0] in range(0, 15):
                time.sleep(0.1)
                while i[0] in range(0, 15):
                    i[0] = i[0] + 1
                    SUBMIT.styles.offset = (1, int(i[0]))
            elif i[0] == 15:
                i[0] = 14
                time.sleep(0.1)
                while 1 <= i[0] <= 14:
                    i[0] = i[0] - 1
                    SUBMIT.styles.offset = (1, int(i[0]))
            if 0 > i[0] > 15:
                i.clear()
                i.append(0)



            

if __name__ == "__main__":
    app = TuiGrid(css_path="grid.css")
    app.run()


