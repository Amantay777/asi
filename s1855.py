from aperr002v01 import APERR002V01
from ap8 import AP8
from math import log10, sqrt, sin, cos
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class S1855(APERR002V01):
    def input_widgets(self):
        super().input_widgets()
        self.root.label_coeffa.destroy()
        self.root.coeffa_frame.destroy()
        #   Label for Dgso entry
        self.root.label_dgso =\
            ttk.Label(self.root.frame_inputs, text='Параметр Dgso, м')
        self.root.label_dgso.grid(column=0, row=5, sticky=E, padx=5)
        #   Entry for Dgso
        self.root.d_gso = StringVar()
        self.root.entry_dgso =\
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.d_gso, validate='all',
                      validatecommand=(self.vcmd, '%P'))
        self.root.entry_dgso.grid(column=1, row=5, sticky=W)
        self.root.entry_dgso.insert(0, '2.1')
        #   Label for theta entry
        self.root.label_theta =\
            ttk.Label(self.root.frame_inputs, text='Параметр \u03B8, \u00b0')
        self.root.label_theta.grid(column=0, row=6, sticky=E, padx=5)
        #   Entry for theta
        self.root.theta = StringVar()
        self.root.entry_theta =\
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.theta, validate='all',
                      validatecommand=(self.vcmd, '%P'))
        self.root.entry_theta.grid(column=1, row=6, sticky=W)
        self.root.entry_theta.insert(0, '0')

    def output_widgets(self):
        super().output_widgets()
        self.k_widgets()
        self.dtheta_widgets()
        self.phi1_widgets()
        self.phimin_widgets()

    def k_widgets(self):
        #   Label for K entry
        self.root.label_k = \
            ttk.Label(self.root.frame_add_out, text='Параметр K')
        self.root.label_k.grid(column=0, row=7, sticky=E, padx=5)
        #   Entry for K
        self.root.entry_k = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_k.grid(column=1, row=7, sticky=W)

    def dtheta_widgets(self):
        #   Label for Dtheta entry
        self.root.label_dtheta = \
            ttk.Label(self.root.frame_add_out, text='Параметр Dtheta')
        self.root.label_dtheta.grid(column=0, row=8, sticky=E, padx=5)
        #   Entry for Dtheta
        self.root.entry_dtheta = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_dtheta.grid(column=1, row=8, sticky=W)

    def phi1_widgets(self):
        #   Label for φ1
        self.root.label_phi1 = ttk.Label(self.root.frame_add_out,
                                         text='Внеосевой угол \u03C61, \u00b0')
        self.root.label_phi1.grid(column=0, row=9, sticky=E, padx=5)
        #   Entry for φ1
        self.root.entry_phi1 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phi1.grid(column=1, row=9, sticky=W)

    def phimin_widgets(self):
        #   Label for φmin
        self.root.label_phimin = \
            ttk.Label(self.root.frame_add_out,
                      text='Внеосевой угол \u03C6min, \u00b0')
        self.root.label_phimin.grid(column=0, row=10, sticky=E, padx=5)
        #   Entry for φmin
        self.root.entry_phimin = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phimin.grid(column=1, row=10, sticky=W)

    def get_inputs(self):
        AP8.get_inputs(self)
        self.eta = float(self.root.eta.get())
        self.d_eq = self.d
        self.d_gso = float(self.root.d_gso.get())
        self.theta = float(self.root.theta.get())

    def set_outputs(self, event):
        super().set_outputs(event)
        #   Set K
        self.root.entry_k.delete(0, END)
        self.root.entry_k.insert(0, self.kr)
        #   Set Dtheta
        self.root.entry_dtheta.delete(0, END)
        self.root.entry_dtheta.insert(0, self.d_thetar)
        #   Set φ1
        self.root.entry_phi1.delete(0, END)
        self.root.entry_phi1.insert(0, self.phi_1r)
        #   Set φmin
        self.root.entry_phimin.delete(0, END)
        self.root.entry_phimin.insert(0, self.phi_minr)

    def add_params(self):
        self.coeffa = 0
        super().add_params()
        self.k_calc()
        self.dtheta_calc()
        self.phir2_calc()
        self.phi1_calc()
        self.phimin_calc()
        self.g12_calc()
        self.phim2_calc()
        self.phib_calc()
        self.a_p[3:] = [self.g1r, self.phi_mr, self.phi_rr, self.phi_br,
                        self.kr, self.d_thetar, self.phi_1r, self.phi_minr]
        return self.a_p

    def k_calc(self):
        self.k = (self.d_gso/self.d_eq) ** 2
        self.kr = round(self.k, 2)

    def dtheta_calc(self):
        self.d_theta = (self.d_gso / self.k) / \
                       sqrt(sin(self.theta) ** 2 + (1 / self.k) ** 2 *
                            cos(self.theta) ** 2)
        self.d_thetar = round(self.d_theta, 2)

    def phir2_calc(self):
        self.phi_r = 15.85 * (self.d_theta / self.w) ** (-0.6)
        self.phi_rr = round(self.phi_r, 2)

    def phi1_calc(self):
        self.phi_1 = 0.9 * 114 * (self.d_theta / self.w) ** (-1.09)
        self.phi_1r = round(self.phi_1, 2)

    def phimin_calc(self):
        self.phi_min = max(self.phi_r, 118 * (self.d_theta / self.w) ** (-1.06))
        self.phi_minr = round(self.phi_min, 2)

    def g12_calc(self):
        self.g1 = 29 - 25 * log10(self.phi_r) + 3 * sin(self.theta) ** 2
        self.g1r = round(self.g1, 2)

    def phim2_calc(self):
        self.d = self.d_theta
        super().phim_calc()

    def phib_calc(self):
        if self.dw >= 46.8:
            self.phi_b = 10 ** (42 / 25)
        else:
            self.phi_b = 10 ** (37 / 25)
        self.phi_br = round(self.phi_b, 2)

    def offaxis_gain(self):
        [gmax, d, w, p] = [self.gmax, self.d_theta, self.w, self.phi]
        t = self.theta
        if self.phi_m < self.phi_r:
            if 0 <= p < self.phi_m:
                g = gmax - 2.5 * 10 ** (-3) * ((d / w) * p) ** 2
            elif self.phi_m <= p <= self.phi_r:
                g = self.g1
            elif self.phi_r < p < self.phi_min:
                g = min(self.g1, 29 + 3 * sin(t) ** 2 - 25 * log10(p))
        elif self.phi_m >= self.phi_r:
            if 0 <= p < self.phi_1:
                g = gmax - 2.5 * 10 ** (-3) * ((d / w) * p) ** 2
            elif self.phi_1 <= p < self.phi_min:
                g = max(gmax - 2.5 * 10 ** (-3) * ((d / w) * p) ** 2,
                             29 + 3 * sin(t) ** 2 - 25 * log10(p))
        if self.phi_min <= p <= 7:
            g = 29 + 3 * sin(t) ** 2 - 25 * log10(p)
        elif 7 < p <= 9.2:
            g = 7.9 + 3 * sin(t) ** 2 * ((9.2 - p) / 2.2)
        elif 9.2 < p <= self.phi_b:
            g = 32 - 25 * log10(p)
        if (self.d_eq / w) >= 46.8:
            if self.phi_b < p <= 180:
                g = - 10
        elif 15 <= (self.d_eq / w) < 46.8:
            if self.phi_b < p <= 70:
                g = - 5
            elif 70 < p <= 180:
                g = 0
        if p > 180:
            g = '\u03C6 > 180 !'
        self.g = g
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        return [self.gr]
