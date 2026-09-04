class Dialogue:
    def __init__(self, lines):
        self.lines = lines
        self.current_line = 0
        self.active = False

    def start(self):
        self.active = True
        self.current_line = 0

    def next_line(self):
        if not self.active:
            return

        self.current_line += 1

        if self.current_line >= len(self.lines):
            self.active = False

    def get_current_line(self):
        if not self.active:
            return ""

        return self.lines[self.current_line]