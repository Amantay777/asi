from asi import Rec
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk
from math import log10, sqrt, pi


class AP3077(Rec):
    def output_widgets(self):
        super().output_widgets()
        self.gmax_widgets()
        self.phi0_widgets()
        self.gx_widgets()

    def gmax_widgets(self):
        #   Label for Gmax entry
        self.root.label_gmax = \
            ttk.Label(self.root.frame_add_out,
                      text='Макс. коэффициент усиления (Gmax), дБ')
        self.root.label_gmax.grid(column=0, row=2, sticky=E, padx=5)
        #   Entry for Gmax
        self.root.entry_gmax = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_gmax.grid(column=1, row=2, sticky=W)

    def phi0_widgets(self):
        #   Label for φ0
        self.root.label_phi0 =\
            ttk.Label(self.root.frame_add_out,
                      text='Ширина луча по уровню -3 дБ (\u03C60), \u00b0')
        self.root.label_phi0.grid(column=0, row=3, sticky=E, padx=5)
        #   Entry for φ0
        self.root.entry_phi0 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phi0.grid(column=1, row=3, sticky=W)

    def gx_widgets(self):
        #   Label for X-polarisation off-axis gain entry
        self.root.label_offaxis_gain_x =\
            ttk.Label(self.root.frame_main_out,
                      text='Кросс-пол. внеосевой коэффициент усиления (Gx),дБ')
        self.root.label_offaxis_gain_x.grid(column=0, row=1, sticky=E,
                                            padx=5, pady=(0, 10))
        #   Entry for X-polarisation off-axis gain
        self.root.entry_offaxis_gain_x =\
            ttk.Entry(self.root.frame_main_out, width=10)
        self.root.entry_offaxis_gain_x.grid(column=1, row=1, sticky=W,
                                            pady=(0, 10))

    def set_outputs(self, event):
        super().set_outputs(event)
        self.set_gmax()
        self.set_phi0()
        self.set_gx()

    def set_gmax(self):
        self.root.entry_gmax.delete(0, END)
        self.root.entry_gmax.insert(0, self.gmaxr)

    def set_phi0(self):
        self.root.entry_phi0.delete(0, END)
        self.root.entry_phi0.insert(0, self.phi_0r)

    def set_gx(self):
        self.root.entry_offaxis_gain_x.delete(0, END)
        self.root.entry_offaxis_gain_x.insert(0, self.gxr)

    def add_params(self):
        self.a_p = super().add_params()
        self.gmax_calc()
        self.phi0_calc()
        self.a_p += [self.gmaxr, self.phi_0r]
        return self.a_p

    def gmax_calc(self):
        self.gmax = 10 * log10(0.7 * (pi * self.dw) ** 2)
        self.gmaxr = round(self.gmax, 2)

    def phi0_calc(self):
        self.phi_0 = (2 * self.w / self.d) * sqrt(3 / 0.0025)
        self.phi_0r = round(self.phi_0, 2)

    def offaxis_gain(self):
        if 0 <= self.phi <= 0.25 * self.phi_0:
            self.g = self.gmax
        elif 0.25 * self.phi_0 < self.phi <= 0.707 * self.phi_0:
            self.g = self.gmax - 12 * (self.phi / self.phi_0) ** 2
        elif 0.707 * self.phi_0 < self.phi <= 1.26 * self.phi_0:
            self.g = self.gmax - 9 - 20 * log10(self.phi / self.phi_0)
        elif 1.26 * self.phi_0 < self.phi <= 9.55 * self.phi_0:
            self.g = self.gmax - 8.5 - 25 * log10(self.phi / self.phi_0)
        elif 9.55 * self.phi_0 < self.phi <= 180:
            self.g = self.gmax - 33
        elif self.phi > 180:
            self.g = '\u03C6 > 180 !'
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        # Cross-polar. off-axis gain
        if 0 <= self.phi <= 0.25 * self.phi_0:
            self.gx = self.gmax - 25
        elif 0.25 * self.phi_0 < self.phi <= 0.44 * self.phi_0:
            self.gx = self.gmax - 30 - \
                      40 * log10(abs((self.phi / self.phi_0) - 1))
        elif 0.44 * self.phi_0 < self.phi <= 1.4 * self.phi_0:
            self.gx = self.gmax - 20
        elif 1.4 * self.phi_0 < self.phi <= 2 * self.phi_0:
            self.gx = self.gmax - 30 - \
                      25 * log10(abs((self.phi / self.phi_0) - 1))
        elif 2 * self.phi_0 < self.phi <= 180:
            self.gx = self.gmax - 30
        elif self.phi > 180:
            self.gx = '\u03C6 > 180 !'
        if self.gx > self.g:
            self.gx = self.g
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p
