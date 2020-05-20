from ap3097 import AP3097
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class BO1900(AP3097):
    def offaxis_gain(self):
        if self.dw >= 32:
            super().offaxis_gain()
            if 0 <= self.phi < self.phi_0:
                self.gx = self.gmax - 17
        else:
            [self.gr, self.gxr] = ['D/\u03BB < 32 !', 'D/\u03BB < 32 !']
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p

    def test(self):
        pass
