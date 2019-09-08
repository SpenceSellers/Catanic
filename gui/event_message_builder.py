import tkinter


class EventMessageBuilder:
    def __init__(self, textbox: tkinter.Text):
        self.segments = []
        self.textbox = textbox

    def text(self, msg, tag=None):
        self.segments.append((msg, tag))
        return self

    def player(self, player_id, msg=None):
        if not msg:
            msg = 'Player ' + str(player_id)

        return self.text(msg, 'player_' + str(player_id))

    def insert(self):
        # Tkinter text boxes cannot be written to when disabled, even programmatically
        self.textbox.config(state=tkinter.NORMAL)

        for text, tag in self.segments:
            self.textbox.insert(tkinter.END, text, tag)

        self.textbox.insert(tkinter.END, '\n')
        self.textbox.see(tkinter.END)

        self.textbox.config(state=tkinter.DISABLED)
