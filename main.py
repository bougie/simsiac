import sys
import urwid

from simsiac.gui import TermWindow


if __name__ == "__main__":
    # init screen use to display "things"
    screen = urwid.raw_display.Screen()

    # create the terminal window
    term = TermWindow(
        w=screen.get_cols_rows()[0],
        h=screen.get_cols_rows()[1]
    )

    try:
        main = urwid.MainLoop(
            term,
            screen=screen,
            unhandled_input=term.unhandled_input
        )
        main.run()
    except Exception as e:
        print(e)
        sys.exit(1)
