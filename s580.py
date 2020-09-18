from s465 import S465
from asi import Rec
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class S580(S465):
    def input_widgets(self):
        super().input_widgets()
        self.root.label_tx_rx.destroy()
        self.root.frame_tx_rx.destroy()

    def get_inputs(self):
        super(S465, self).get_inputs()
        self.after_before = self.root.after_before.get()
        self.inputs += [self.after_before, True]

    def calculate(self, inputs):
        self.ab = inputs[3]
        self.tr = True
        return Rec.calculate(self, inputs)

    def add_params(self):
        self.a_p = super().add_params()
        if self.dw >= 50:
            self.phi_min = max(1, 100 * self.w / self.d)
        else:
            self.phi_min = ''
        self.phi_minr = round(self.phi_min, 2) if type(self.phi_min) ==\
            float else self.phi_min
        self.a_p[2] = self.phi_minr
        return self.a_p

    def offaxis_gain(self):
        if self.dw >= 50:
            if self.phi < self.phi_min:
                self.gmax = 20 * log10(self.dw) + 7.7
                self.g = self.gmax - 2.5 * 10 ** (-3) *\
                    (self.dw * self.phi) ** 2
            elif self.phi_min <= self.phi <= 20:
                self.g = 29 - 25 * log10(self.phi)
                # elif (20 < self.phi <= 26.3):
                # self.g = -3.5
            elif (self.ab or self.dw > 100) and 20 < self.phi < 48:
                self.g = 32 - 25 * log10(self.phi)
            elif 20 < self.phi < 48:
                self.g = 52 - 10 * log10(self.dw) - 25 * log10(self.phi)
            elif (self.ab or self.dw > 100) and 48 <= self.phi <= 180:
                self.g = -10
            elif 48 <= self.phi <= 180:
                self.g = 10 - 10 * log10(self.dw)
            else:
                self.g = '\u03C6 > 180 !'
        else:
            self.g = 'D/\u03BB < 50 !'
        self.m_p = super(S465, self).offaxis_gain()
        return self.m_p

    def test(self):
        assert self.calculate([1, 14, 1, True]) == \
               ['D/\u03BB < 50 !', 21.41, 46.7, '']
        assert self.calculate([1, 14, 1.1, True]) ==\
               [35.32, 21.41, 51.37, 1.95]
        assert self.calculate([3, 14, 1.1, True])[0] == 17.07
        assert self.calculate([21, 14, 1.1, True])[0] == -1.06
        assert self.calculate([27, 14, 1.1, True])[0] == -3.78
        assert self.calculate([49, 14, 1.1, True])[0] == -10
        assert self.calculate([181, 14, 1.1, True])[0] == '\u03C6 > 180 !'
