import urwid


class TermWindow(urwid.Frame):
    """This class manage the whole screen"""

    def __init__(self):
        self.screen = urwid.raw_display.Screen()

        # fill frame with all parts
        super(TermWindow, self).__init__(
            body=None,
            header=None,
            focus_part='body'
        )

    @property
    def screen_w(self):
        return self.screen.get_cols_rows()[0]

    @property
    def screen_h(self):
        return self.screen.get_cols_rows()[1]

    @property
    def body_content_max_w(self):
        """Get body content max width if set,
        or all the available space if not"""

        if self.main_body is not None:
            return self.main_body.max_w
        else:
            # body_content does not exist so return the screen width
            return self.screen_w

    @property
    def body_content_max_h(self):
        """Get body content max hight if set,
        or all the available space if not"""

        if self.main_body is not None:
            return self.main_body.max_h
        elif self.main_header is not None:
            # return the place available for the body content
            # which equals to : screen height - header hight
            return self.screen_h - self.main_header.rows((self.screen_w,))
        else:
            # no header so full place available
            return self.screen_h

    def unhandled_input(self, key):
        """Handle unhandled key pressed"""

        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    @property
    def main_header(self):
        """Get header widget"""

        try:
            return self.contents['header'][0]
        except:
            return None

    @main_header.setter
    def main_header(self, value):
        """Set header widget"""

        self.contents['header'] = (value, self.options())

    @property
    def main_body(self):
        """Get body widget"""

        try:
            return self.contents['body'][0]
        except:
            return None

    @main_body.setter
    def main_body(self, value):
        """Set body widget"""

        self.contents['body'] = (value, self.options())

    def keypress(self, size, key):
        """Handle key pressed when body has focus"""

        if hasattr(self.focus, 'keypress'):
            return self.focus.keypress(size, key)
        else:
            return key
