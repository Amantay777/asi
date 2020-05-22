from offaxis_gain import Rec
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class AP8(Rec):
    def output_widgets(self):
        super().output_widgets()
        #   Label for Gmax entry
        self.root.label_gmax = \
            ttk.Label(self.root.frame_add_out,
                      text='Макс. коэффициент усиления (Gmax), дБ')
        self.root.label_gmax.grid(column=0, row=2, sticky=E, padx=5)
        #   Entry for Gmax
        self.root.entry_gmax = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_gmax.grid(column=1, row=2, sticky=W)

        #   Label for G1 entry
        self.root.label_g1 =\
            ttk.Label(self.root.frame_add_out,
                      text='Усиление 1-й бок. лепестка (G1), дБ')
        self.root.label_g1.grid(column=0, row=3, sticky=E, padx=5)
        #   Entry for G1
        self.root.entry_g1 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_g1.grid(column=1, row=3, sticky=W)

        #   Label for φm
        self.root.label_phim =\
            ttk.Label(self.root.frame_add_out,
                      text='Внеосевой угол начала G1 (\u03C6m), \u00b0')
        self.root.label_phim.grid(column=0, row=4, sticky=E, padx=5)
        #   Entry for φm
        self.root.entry_phim = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phim.grid(column=1, row=4, sticky=W)

        #   Label for φr
        self.root.label_phir = \
            ttk.Label(self.root.frame_add_out,
                      text='Внеосевой угол конца G1 (\u03C6r), \u00b0')
        self.root.label_phir.grid(column=0, row=5, sticky=E, padx=5)
        #   Entry for φr
        self.root.entry_phir = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phir.grid(column=1, row=5, sticky=W)

        #   Label for φb
        self.root.label_phib = ttk.Label(self.root.frame_add_out,
                                         text='Внеосевой угол \u03C6b, \u00b0')
        self.root.label_phib.grid(column=0, row=6, sticky=E, padx=5)
        #   Entry for φb
        self.root.entry_phib = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phib.grid(column=1, row=6, sticky=W)

    def set_outputs(self, event):
        super().set_outputs(event)
        #   Set Gmax
        self.root.entry_gmax.delete(0, END)
        self.root.entry_gmax.insert(0, self.gmaxr)
        #   Set G1
        self.root.entry_g1.delete(0, END)
        self.root.entry_g1.insert(0, self.g1r)
        #   Set φm
        self.root.entry_phim.delete(0, END)
        self.root.entry_phim.insert(0, self.phi_mr)
        #   Set φr
        self.root.entry_phir.delete(0, END)
        self.root.entry_phir.insert(0, self.phi_rr)
        #   Set φb
        self.root.entry_phib.delete(0, END)
        self.root.entry_phib.insert(0, self.phi_br)

    def add_params(self):
        self.a_p = super().add_params()
        self.gmax_calc()
        self.g1_calc()
        self.phim_calc()
        self.phib_calc()
        self.phir_calc()
        self.a_p += [self.gmaxr, self.g1r, self.phi_mr, self.phi_rr,
                     self.phi_br]
        return self.a_p

    def gmax_calc(self):
        self.gmax = 20 * log10(self.dw) + 7.7
        self.gmaxr = round(self.gmax, 2)

    def g1_calc(self):
        self.g1 = 2 + 15 * log10(self.dw)
        self.g1r = round(self.g1, 2)

    def phir_calc(self):
        if self.dw >= 100:
            self.phi_r = 15.85 * self.dw ** (-0.6)
        else:
            self.phi_r = 100 * self.w / self.d
        self.phi_rr = round(self.phi_r, 2)

    def phib_calc(self):
        self.phi_br = self.phi_b = 48

    def phim_calc(self):
        self.phi_m = (20 * self.w / self.d) * sqrt(self.gmax - self.g1)
        self.phi_mr = round(self.phi_m, 2)

    def offaxis_gain(self):
        if self.phi == 0:
            self.g = self.gmax
        elif 0 < self.phi < self.phi_m:
            self.g = self.gmax - 2.5 * 10 ** (-3) * (self.dw * self.phi) ** 2
        elif self.phi_m <= self.phi < self.phi_r:
            self.g = self.g1
        elif self.phi > 180:
            self.g = '\u03C6 > 180 !'
        else:
            if self.dw >= 100:
                if self.phi_r <= self.phi < self.phi_b:
                    self.g = 32 - 25 * log10(self.phi)
                else:
                    self.g = - 10
            else:
                if self.phi_r <= self.phi < self.phi_b:
                    self.g = (52 - 10*log10(self.dw) - 25*log10(self.phi))
                else:
                    self.g = 10 - 10 * log10(self.dw)
        self.m_p = super().offaxis_gain()
        return self.m_p

    def test(self):
        assert self.calculate([0, 14, 3]) ==\
               [50.63, 21.41, 140.1, 50.63, 34.2, 0.58, 0.82, 48]
        assert self.calculate([0.3, 14, 3])[0] == 46.21
        assert self.calculate([0.7, 14, 3])[0] == 34.2
        assert self.calculate([20, 14, 3])[0] == -0.53
        assert self.calculate([100, 14, 3])[0] == -10
        assert self.calculate([200, 14, 3])[0] == '\u03C6 > 180 !'
        assert self.calculate([0, 14, 1]) == \
               [41.09, 21.41, 46.7, 41.09, 27.04, 1.61, 2.14, 48]
        assert self.calculate([0.8, 14, 1])[0] == 37.6
        assert self.calculate([2, 14, 1])[0] == 27.04
        assert self.calculate([20, 14, 1])[0] == 2.78
        assert self.calculate([100, 14, 1])[0] == -6.69
        assert self.calculate([200, 14, 1])[0] == '\u03C6 > 180 !'
