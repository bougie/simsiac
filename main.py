import sys
import urwid

from simsiac.gui import TermWindow
from simsiac.menu import generate_application_menu


class Engine:
    def __init__(self):
        # create the terminal window
        self.term = TermWindow()

    def set_header(self):
        """Create the header"""

        header_text_content = urwid.Text('SIMSIAC', 'center')
        self.term.main_header = urwid.BoxAdapter(
            urwid.LineBox(urwid.Filler(header_text_content)),
            5
        )

    def load_main_application(self):
        self.set_header()

        try:
            generate_application_menu(self.term)
        except Exception as e:
            print(e)
            sys.exit(1)

    def run_forever(self):
        try:
            main = urwid.MainLoop(
                self.term,
                screen=self.term.screen,
                unhandled_input=self.term.unhandled_input
            )
            main.run()
        except Exception as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    engine = Engine()

    engine.load_main_application()
    engine.run_forever()
