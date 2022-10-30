from tkinter import Widget
from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.message import Message, MessageTarget
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Static, Button, Header, Footer, Input
from textual import events

class TuiGrid(App):
    CSS_PATH = "grid0.css"

    def compose(self) -> ComposeResult:
        input_error = "Quantity:\ncontains non-integers"

        yield Container(
                Horizontal(
                    Static("Vegetable Stand"),
                    id="header",
                ),
                Container(
                    Container(
                        Button("Insert", id="insert"),
                        Button("Select", id="select"),
                        Button("Create Table", id="create"),
                        id="top-left",
                    ),
                    Container(
                        # Static("Enter vegetable:", id="request-text"),
                        Input("Enter vegetable", id="vegetable"),
                        # Static("Enter quantity: ", id="request-text"),
                        Input("Enter quantity", id="quantity"),
                        Container(
                            Static("Error", id="one"),
                            Static(input_error, id="int-error"),
                            Static("Enter additional information", id="two"),
                            Static("Everything looks good", id="three"),
                            id="middle-pane",
                        ),
                        id="top-right",
                    ),
                    Vertical(
                    *[Static(f"Vertical layout, child {number}") for number in range(4)],
                    id="bottom-pane",
                    ),
                    Vertical(
                        Button("Submit  ", id="box1"),
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

class HandleButton(Static):

    class Selected(Message):

        def __init__(self, sender: MessageTarget, offset: Button.offset) -> None:
            self.offset = offset
            super().__init__(sender)
    
    def __init__(self, offset: Button.offset) -> None:
        self.offset = offset
        super().__init__()

    async def on_click(self) -> None:
        await self.emit(self.Selected(self, self.offset))   
    

class HandlePull(App):
    def compose(self) -> ComposeResult:
        yield HandleButton(Button.offset.parse("1,1"))

    def on_handel_click(self, message: HandleButton.Selected) -> None:
        self.screen.styles.animate("offset", message.handle, duration=0.5)

if __name__ == "__main__":
    app = TuiGrid(css_path="grid0.css")
    app.run()


