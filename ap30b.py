from ap3097 import AP3097
from ap8 import AP8
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class AP30B(AP3097):
    def output_widgets(self):
        AP8.output_widgets(self)
        self.root.label_phir.destroy()
        self.root.entry_phir.destroy()
        self.root.label_phib.destroy()
        self.root.entry_phib.destroy()

    def set_outputs(self, event):
        try:
            AP8.set_outputs(self, event)
        except:
            pass

    def add_params(self):
        self.a_p = AP8.add_params(self)
        self.gmax = 10 * log10(self.eta * (pi*self.dw) ** 2)
        self.gmaxr = round(self.gmax, 2)
        self.g1 = - 1 + 15 * log10(self.dw)
        self.g1r = round(self.g1, 2)
        self.phi_m = (20 * self.w / self.d) * sqrt(self.gmax - self.g1)
        self.phi_mr = round(self.phi_m, 2)
        self.a_p[2:] = [self.gmaxr, self.g1r, self.phi_mr]
        return self.a_p

    def offaxis_gain(self):
        self.g = AP8.offaxis_gain(self)[0]
        if self.phi_m <= self.phi <= 19.95:
            self.g = min(self.g1, 29 - 25 * log10(self.phi))
        elif 19.95 < self.phi <= 180:
            self.g = max(min(- 3.5, 32 - 25 * log10(self.phi)), -10)
        self.m_p = super(AP8, self).offaxis_gain()
        return self.m_p

    def test(self):
        assert self.calculate([0, 13, 2.7, 0.7]) == \
               [49.76, 23.06, 117.08, 49.76, 30.03, 0.76]
        assert self.calculate([0.3, 13, 2.7, 0.7])[0] == 46.68
        assert self.calculate([0.8, 13, 2.7, 0.7])[0] == 30.03
        assert self.calculate([10, 13, 2.7, 0.7])[0] == 4
        assert self.calculate([20, 13, 2.7, 0.7])[0] == -3.5
        assert self.calculate([40, 13, 2.7, 0.7])[0] == -8.05
        assert self.calculate([100, 13, 2.7, 0.7])[0] == -10
        assert self.calculate([200, 13, 2.7, 0.7])[0] == '\u03C6 > 180 !'

