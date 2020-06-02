from ap3077 import AP3077
from math import log10
from tkinter import END


class AP30AR13(AP3077):
    def phi0_widgets(self):
        pass

    def set_outputs(self, event):
        try:
            super().set_outputs(event)
        except:
            pass
        #   Set Gx
        self.root.entry_offaxis_gain_x.delete(0, END)
        self.root.entry_offaxis_gain_x.insert(0, self.gxr)

    def offaxis_gain(self):
        super().offaxis_gain()
        if 0 <= self.phi <= 0.1:
            self.g = self.gmax
        elif 0.1 < self.phi <= 0.32:
            self.g = self.gmax - 21 - 20 * log10(self.phi)
        elif 0.32 < self.phi <= 0.44:
            self.g = self.gmax - 5.7 - 53.2 * self.phi ** 2
        elif 0.44 < self.phi <= 48:
            self.g = self.gmax - 25 - 25 * log10(self.phi)
        elif 48 < self.phi <= 180:
            self.g = self.gmax - 67
        elif self.phi > 180:
            self.g = '\u03C6 > 180 !'
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        if self.phi <= 180:
            self.gx = self.gmax - 30
        else:
            self.gx = '\u03C6 > 180 !'
        if self.gx > self.g:
            self.gx = self.g
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p
