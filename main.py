import sys
import urwid


class TermWindow(urwid.WidgetPlaceholder):
    def __init__(self):
        super(TermWindow, self).__init__(urwid.Pile([]))

        self.set_header()
        self.set_body()

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        else:
            self.body.set_text(self.body.get_text()[0] + key)

    def set_header(self):
        """"""

        self.header = urwid.Text('SIMSIAC', 'center')

        self.original_widget.contents.append((
            urwid.LineBox(urwid.Filler(self.header)),
            self.original_widget.options('given', 5)
        ))

    def set_body(self):
        """"""

        self.body = urwid.Text('')

        self.original_widget.contents.append((
            urwid.Filler(self.body, 'top'),
            self.original_widget.options()
        ))

if __name__ == "__main__":
    term = TermWindow()
    try:
        urwid.MainLoop(term, unhandled_input=term.unhandled_input).run()
    except Exception as e:
        print(e)
        sys.exit(1)
