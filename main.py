import sys
import urwid


class MenuItem(urwid.Padding):
    """This class represent an item in the menu"""

    def __init__(self, name, callback=None, shortcut=None, **kwargs):
        self.name = name
        self.callback = callback
        self.shortcut = shortcut

        # init the Padding with a Text widget with a border arround it
        super(MenuItem, self).__init__(
            urwid.LineBox(
                urwid.Filler(
                    urwid.Text(name)
                )
            )
        )

        # add attr according to kwargs.
        # Used for override Padding attributs
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)


class Menu(urwid.Pile):
    """Manage a menu"""

    def __init__(self, items=None):
        # init the Pile with an empty widgets array
        super(Menu, self).__init__([])

        if items is not None:
            self.add_items(items=items)

    def add_item(self, item):
        """Add an item"""

        if type(item) == dict:
            _item = MenuItem(**item)
        elif type(item) == MenuItem:
            _item = item
        else:
            raise Exception('Bad object type for a menu item')

        if hasattr(_item, 'height'):
            self.contents.append((_item, self.options('given', _item.height)))
        else:
            self.contents.append((_item, self.options()))

    def add_items(self, items):
        """Add a list of items in the menu"""

        if items is None:
            raise Exception('Bad menu items list')

        for item in items:
            self.add_item(item=item)

    def keypress(self, size, key):
        """Handle menu key pressed"""

        if key not in ('q', 'Q'):
            return None
        else:
            return key


class TermWindow(urwid.Frame):
    """This class manage the whole screen"""

    def __init__(self):
        self.__screen_w = 0
        self.__screen_h = 0

        # init the header part
        self.set_header()
        # init the body part
        self.set_body()

        # fill frame with all parts
        super(TermWindow, self).__init__(
            body=self.body_content,
            header=self.header_content
        )

    @property
    def screen_w(self):
        return self.__screen_w

    @screen_w.setter
    def screen_w(self, value):
        if value > 0:
            self.__screen_w = value

    @property
    def screen_h(self):
        return self.__screen_h

    @screen_h.setter
    def screen_h(self, value):
        if value > 0:
            self.__screen_h = value

    def unhandled_input(self, key):
        """Handle unhandled key pressed"""

        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def set_header(self):
        """Create the header"""

        self.header_text_content = urwid.Text('SIMSIAC', 'center')

        self.header_content = urwid.BoxAdapter(
            urwid.LineBox(urwid.Filler(self.header_text_content)),
            5
        )

    def set_body(self):
        """Create the body"""

        items = [
            {'name': '1 - BOUGIE', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '2 - IS', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '3 - MAGIC', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '4 - ALL', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '5 - THE', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '6 - TIME', 'align': 'center', 'width': 42, 'height': 5}
        ]
        self.body_content = Menu(items)

    def keypress(self, size, key):
        """Handle key pressed when body has focus"""

        if hasattr(self.focus, 'keypress'):
            return self.focus.keypress(size, key)
        else:
            return key

if __name__ == "__main__":
    term = TermWindow()
    try:
        main = urwid.MainLoop(term, unhandled_input=term.unhandled_input)
        term.screen_w = main.screen.get_cols_rows()[0]
        term.screen_h = main.screen.get_cols_rows()[1]

        main.run()
    except Exception as e:
        print(e)
        sys.exit(1)
