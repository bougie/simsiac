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

    def __init__(self, items=None, max_w=0, max_h=0, scroll_type='page'):
        # max width of widget
        self.max_w = max_w
        # max hight of widget
        self.max_h = max_h

        # first item ID which is displayed on screen
        self.first_item = 0
        # last item ID which is displayed on screen
        self.last_item = 0

        # list of all items in the menu (displayed or not)
        self._items = []

        # how to scroll menu item (list for item one by one or page)
        self.scroll_type = scroll_type

        # init the Pile with an empty widgets array
        super(Menu, self).__init__([])

        if items is not None:
            self.add_items(items=items)

    @property
    def max_w(self):
        return self.__max_w

    @max_w.setter
    def max_w(self, value):
        if value > 0:
            self.__max_w = value

    @property
    def max_h(self):
        return self.__max_h

    @max_h.setter
    def max_h(self, value):
        if value > 0:
            self.__max_h = value

    def add_item(self, item):
        """Add an item"""

        if type(item) == dict:
            _item = MenuItem(**item)
        elif type(item) == MenuItem:
            _item = item
        else:
            raise Exception('Bad object type for a menu item')

        if hasattr(_item, 'height'):
            # no item is not displayed
            # and it can be displayed
            if (len(self._items) == len(self.contents)
                    and self.rows((self.max_w,)) + _item.height <= self.max_h):
                self.contents.append((_item, self.get_item_options(item=_item)))
                self.last_item = len(self.contents) - 1

            # add item in the items list
            # even if it can't be displayed at this moment
            self._items.append(_item)
        else:
            raise Exception('Object does not have a height')

    def add_items(self, items):
        """Add a list of items in the menu"""

        if items is None:
            raise Exception('Bad menu items list')

        for item in items:
            self.add_item(item=item)

    def get_item_options(self, item):
        """Get options associated to the item according of his parameters"""

        if hasattr(item, 'height'):
            opts = self.options('given', item.height)
        else:
            opts = self.options()

        return opts

    def keypress(self, size, key):
        """Handle menu key pressed"""

        if key in ('q', 'Q'):
            return key

        if key == 'up':
            if self.scroll_type == 'list':
                self.scroll_up()
            elif self.scroll_type == 'page':
                self.scroll_page_up()
        elif key == 'down':
            if self.scroll_type == 'list':
                self.scroll_down()
            elif self.scroll_type == 'page':
                self.scroll_page_down()
        else:
            return key

        return None

    def scroll_up(self):
        """Scroll the menu to the top"""

        if self.first_item > 0 and self.last_item < len(self._items):
            # change the first item id which will be displayed
            self.first_item -= 1

            _item = self._items[self.first_item]
            opts = self.get_item_options(item=_item)

            self.contents.insert(0, (_item, opts))

            # remove the last item on screen
            # until all block can't be totally displayed
            while self.rows((self.max_w,)) >= self.max_h:
                self.contents.pop()
                # change the last item id which will be displayed
                self.last_item -= 1

    def scroll_page_up(self):
        """Scroll the manu to the bottom by a page"""

        # set the last previous item will displayed
        if self.first_item > 0:
            self.first_item -= 1
            self.last_item = self.first_item

            del self.contents[:]

            while True:
                _item = self._items[self.first_item]
                opts = self.get_item_options(item=_item)

                # add item while there is available place on screen
                if self.rows((self.max_w,)) + _item.height <= self.max_h:
                    self.contents.insert(0, (_item, opts))

                    if self.first_item > 0:
                        self.first_item -= 1
                    else:
                        break
                else:
                    self.first_item += 1
                    break

    def scroll_down(self):
        """Scroll the menu to the bottom"""

        if self.first_item < len(self._items) - len(self.contents):
            # change the last item id which will be displayed
            self.last_item += 1

            # item and item's options to add
            _item = self._items[self.last_item]
            opts = self.get_item_options(item=_item)

            self.contents.append((_item, opts))

            # remove the first item on screen
            # until all block can't be totally displayed
            while self.rows((self.max_w,)) >= self.max_h:
                self.contents.remove(self.contents[0])
                # change the first item id which will be displayed
                self.first_item += 1

    def scroll_page_down(self):
        """Scroll the manu to the bottom by a page"""

        # set the first next item will displayed
        if self.last_item < len(self._items) - 1:
            self.last_item += 1
            self.first_item = self.last_item

            del self.contents[:]

            while True:
                _item = self._items[self.last_item]
                opts = self.get_item_options(item=_item)

                # add item ahile there is available place on screen
                if self.rows((self.max_w,)) + _item.height <= self.max_h:
                    self.contents.append((_item, opts))

                    if self.last_item < len(self._items) - 1:
                        self.last_item += 1
                    else:
                        break
                else:
                    self.last_item -= 1
                    break


class TermWindow(urwid.Frame):
    """This class manage the whole screen"""

    def __init__(self, w=0, h=0):
        self.screen_w = w
        self.screen_h = h

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

    @property
    def body_content_max_w(self):
        """Get body content max width if set,
        or all the available space if not"""

        if hasattr(self, 'body_content'):
            return self.body_content.max_w
        else:
            # body_content does not exist so return the screen width
            return self.screen_w

    @property
    def body_content_max_h(self):
        """Get body content max hight if set,
        or all the available space if not"""

        if hasattr(self, 'body_content'):
            return self.body_content.max_h
        else:
            # return the place available for the body content
            # which equals to : screen height - header hight
            return self.screen_h - self.header_content.rows((self.screen_w,))

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
            {'name': '1 - BOUGIE', 'align': 'center', 'width': 42, 'height': 3},
            {'name': '2 - IS', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '3 - MAGIC', 'align': 'center', 'width': 42, 'height': 7},
            {'name': '4 - ALL', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '5 - THE', 'align': 'center', 'width': 42, 'height': 3},
            {'name': '6 - TIME', 'align': 'center', 'width': 42, 'height': 3},
            {'name': '7 - TIME', 'align': 'center', 'width': 42, 'height': 4},
            {'name': '8 - TIME', 'align': 'center', 'width': 42, 'height': 9},
            {'name': '9 - TIME', 'align': 'center', 'width': 42, 'height': 9},
            {'name': '10 - TIME', 'align': 'center', 'width': 42, 'height': 3},
            {'name': '11 - TIME', 'align': 'center', 'width': 42, 'height': 3},
            {'name': '12 - TIME', 'align': 'center', 'width': 42, 'height': 5},
            {'name': '13 - TIME', 'align': 'center', 'width': 42, 'height': 9}
        ]
        self.body_content = Menu(
            max_w=self.body_content_max_w,
            max_h=self.body_content_max_h
        )
        self.body_content.add_items(items)

    def keypress(self, size, key):
        """Handle key pressed when body has focus"""

        if hasattr(self.focus, 'keypress'):
            return self.focus.keypress(size, key)
        else:
            return key

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
