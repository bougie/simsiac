import sys
import signal
from time import time
import curses


def __signal_handler(signal, frame):
    """Callback for CTRL-C"""

    engine.end()
    sys.exit(0)


class Timer():
    """The timer class. A simple chronometer."""

    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time() + self.duration

    def reset(self):
        self.start()

    def set(self, duration):
        self.duration = duration

    def finished(self):
        return time() > self.target


class Window():
    """This class manage the display"""

    def __init__(self, args=None):
        self.args = args

        # Init the curses screen
        self.screen = curses.initscr()
        if not self.screen:
            sys.exit(1)

        # init term width / height
        self.screen_x = self.screen.getmaxyx()[1]  # width
        self.screen_y = self.screen.getmaxyx()[0]  # height

        # Set curses options
        if hasattr(curses, 'start_color'):
            curses.start_color()
        if hasattr(curses, 'use_default_colors'):
            curses.use_default_colors()
        if hasattr(curses, 'noecho'):
            curses.noecho()
        if hasattr(curses, 'cbreak'):
            curses.cbreak()

        # init title window
        self.title_nlines = 5
        self.title_window = self.screen.subwin(
            self.title_nlines, self.screen_x,
            0, 0
        )
        # init main window
        self.term_window = self.screen.subwin(
            self.screen_y - self.title_nlines, self.screen_x,
            self.title_nlines - 1, 0
        )

    def close(self):
        """Shutdown the curses window"""

        if hasattr(curses, 'echo'):
            curses.echo()
        if hasattr(curses, 'nocbreak'):
            curses.nocbreak()
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(1)
            except Exception:
                pass
        curses.endwin()

    def display_title(self):
        """Display the title window"""

        self.title_window.border('|', '|', '_', '_', ' ', ' ', '|', '|')

    def display_term(self):
        """Display the term (main) window"""

        self.term_window.border('|', '|', '_', '_', '|', '|', '|', '|')

    def display(self):
        self.display_title()
        self.display_term()

    def flush(self):
        """Erase the content of the screen"""

        self.title_window.clear()
        self.term_window.clear()
        self.display()
        self.title_window.refresh()
        self.term_window.refresh()

    def update(self):
        self.flush()

        countdown = Timer(3)
        while not countdown.finished():
            curses.napms(100)


class Engine():
    def __init__(self):
        self.window = Window()

    def end(self):
        self.window.close()

    def serve_forever(self):
        """Main loop"""
        while True:
            self.window.update()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, __signal_handler)

    engine = Engine()
    engine.serve_forever()
