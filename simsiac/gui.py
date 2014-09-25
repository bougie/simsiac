import urwid

from simsiac.menu import Menu


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
            {
                'name': '01 - Informations',
                'align': 'center',
                'width': 42,
                'height': 3
            }
        ]
        self.body_content = Menu(
            self,
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
