from typing import Callable, Optional

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from utils import Size

from .log import log


def launch(size: Size = Size(200, 100)) -> None:
    Window.size = size
    Window.minimum_width, Window.minimum_height = Window.size
    Window.maximum_width, Window.maximum_height = Window.size
    Window.resizable = False
    Config.set("graphics", "width", size.width)
    Config.set("graphics", "height", size.height)
    Menu().run()


Config.set("graphics", "resizable", False)


class Menu(App):
    def build(self) -> BoxLayout:
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        buttons: dict[str, Callable[[Button], None]] = {
            "Play": self.play,
            "AI": self.ai,
            "Algorithm": self.algorithm,
            "Settings": self.settings,
            "Quit": self.quit,
        }

        for text, action in buttons.items():
            button = Button(text=text, size_hint=(None, None), size=(100, 50))
            button.bind(on_press=action)
            layout.add_widget(button)

        return layout

    def play(self, instance: Button) -> None:
        log.debug(f"Play button was pressed")

    def ai(self, instance: Button) -> None:
        log.debug(f"AI button was pressed")

    def algorithm(self, instance: Button) -> None:
        log.debug(f"Algorithm button was pressed")

    def settings(self, instance: Button) -> None:
        log.debug(f"Settings button was pressed")

    def quit(self, instance: Button) -> None:
        log.debug(f"Quit button was pressed")
        self.exit()

    def exit(self) -> None:
        self.stop()
