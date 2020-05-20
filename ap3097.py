from aperr002v01 import APERR002V01
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class AP3097(APERR002V01):
    def input_widgets(self):
        super().input_widgets()
        self.root.entry_eta.insert(0, '0.65')
        self.root.label_coeffa.destroy()
        self.root.coeffa_frame.destroy()

    def output_widgets(self):
        super().output_widgets()
        #   Label for X-polarisation off-axis gain entry
        self.root.label_offaxis_gain_x = ttk.Label(self.root.frame_main_out,
                                                   text=('Кросс-пол. внеосевой'
                                                         ' коэффициент усилени'
                                                         'я (Gx), дБ'))
        self.root.label_offaxis_gain_x.grid(column=0, row=1, sticky=E,
                                            padx=5, pady=(0, 10))
        #   Entry for X-polarisation off-axis gain
        self.root.entry_offaxis_gain_x = ttk.Entry(self.root.frame_main_out,
                                                   width=10)
        self.root.entry_offaxis_gain_x.grid(column=1, row=1, sticky=W,
                                            pady=(0, 10))

        #   Label for 0.25*φ0
        self.root.label_z25phi0 = ttk.Label(self.root.frame_add_out,
                                            text=('Внеосевой угол 0.25*\u03C60'
                                                  ', \u00b0'))
        self.root.label_z25phi0.grid(column=0, row=7, sticky=E, padx=5)
        #   Entry for 0.25*φ0
        self.root.entry_z25phi0 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_z25phi0.grid(column=1, row=7, sticky=W)

        #   Label for 0.44*φ0
        self.root.label_z44phi0 = ttk.Label(self.root.frame_add_out,
                                            text=('Внеосевой угол 0.44*\u03C60'
                                                  ', \u00b0'))
        self.root.label_z44phi0.grid(column=0, row=8, sticky=E, padx=5)
        #   Entry for 0.44*φ0
        self.root.entry_z44phi0 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_z44phi0.grid(column=1, row=8, sticky=W)

        #   Label for φ0
        self.root.label_phi0 = ttk.Label(self.root.frame_add_out,
                                         text=('Внеосевой угол \u03C60, '
                                               '\u00b0'))
        self.root.label_phi0.grid(column=0, row=9, sticky=E, padx=5)
        #   Entry for φ0
        self.root.entry_phi0 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phi0.grid(column=1, row=9, sticky=W)

        #   Label for φ1
        self.root.label_phi1 = ttk.Label(self.root.frame_add_out,
                                         text=('Внеосевой угол \u03C61, '
                                               '\u00b0'))
        self.root.label_phi1.grid(column=0, row=10, sticky=E, padx=5)
        #   Entry for φ1
        self.root.entry_phi1 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phi1.grid(column=1, row=10, sticky=W)

        #   Label for φ2
        self.root.label_phi2 = ttk.Label(self.root.frame_add_out,
                                         text=('Внеосевой угол \u03C62, '
                                               '\u00b0'))
        self.root.label_phi2.grid(column=0, row=11, sticky=E, padx=5)
        #   Entry for φ2
        self.root.entry_phi2 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phi2.grid(column=1, row=11, sticky=W)

        #   Label for S
        self.root.label_s = ttk.Label(self.root.frame_add_out,
                                      text='Коэффициент C, дБ')
        self.root.label_s.grid(column=0, row=12, sticky=E, padx=5)
        #   Entry for S
        self.root.entry_s = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_s.grid(column=1, row=12, sticky=W)

    def set_outputs(self, event):
        super().set_outputs(event)
        #   Set Gx
        self.root.entry_offaxis_gain_x.delete(0, END)
        self.root.entry_offaxis_gain_x.insert(0, self.gxr)
        #   Set 0.25*φ0
        self.root.entry_z25phi0.delete(0, END)
        self.root.entry_z25phi0.insert(0, self.z25phi_0r)
        #   Set 0.44*φ0
        self.root.entry_z44phi0.delete(0, END)
        self.root.entry_z44phi0.insert(0, self.z44phi_0r)
        #   Set φ0
        self.root.entry_phi0.delete(0, END)
        self.root.entry_phi0.insert(0, self.phi_0r)
        #   Set φ1
        self.root.entry_phi1.delete(0, END)
        self.root.entry_phi1.insert(0, self.phi_1r)
        #   Set φ2
        self.root.entry_phi2.delete(0, END)
        self.root.entry_phi2.insert(0, self.phi_2r)
        #   Set S
        self.root.entry_s.delete(0, END)
        self.root.entry_s.insert(0, self.sr)

    def calculate(self, inputs):
        self.eta = inputs[3]
        return super().calculate(inputs)

    def add_params(self):
        super().add_params()
        self.phir_calc()
        self.g1_calc()
        self.phim_calc()
        self.phib_calc()
        self.xap_calc()
        self.a_p[3:] = [self.g1r, self.phi_mr, self.phi_rr, self.phi_br]
        self.a_p += [self.z25phi_0r, self.z44phi_0r, self.phi_0r,
                     self.phi_1r, self.phi_2r, self.sr]
        return self.a_p

    def phir_calc(self):
        self.phi_r = 95 * self.w / self.d
        self.phi_rr = round(self.phi_r, 2)

    def g1_calc(self):
        self.g1 = 29 - 25 * log10(self.phi_r)
        self.g1r = round(self.g1, 2)

    def phib_calc(self):
        self.phi_b = 10 ** (34 / 25)
        self.phi_br = round(self.phi_b, 2)

    def xap_calc(self):
        self.phi_0 = (2 * self.w / self.d) * sqrt(3 / 0.0025)
        self.phi_0r = round(self.phi_0, 2)
        self.z25phi_0 = 0.25 * self.phi_0
        self.z25phi_0r = round(self.z25phi_0, 2)
        self.z44phi_0 = 0.44 * self.phi_0
        self.z44phi_0r = round(self.z44phi_0, 2)
        self.phi_1 = (self.phi_0 / 2) * sqrt(10.1875)
        self.phi_1r = round(self.phi_1, 2)
        self.phi_2 = 10 ** (26 / 25)
        self.phi_2r = round(self.phi_2, 2)
        self.s = 21 - 25 * log10(self.phi_1) - (self.gmax - 17)
        self.sr = round(self.s, 2)

    def offaxis_gain(self):
        self.g = super().offaxis_gain()[0]
        # Co-polar. off-axis gain
        if self.phi_r <= self.phi < self.phi_b:
            self.g = 29 - 25 * log10(self.phi)
        elif self.phi_b <= self.phi < 70:
            self.g = - 5
        elif 70 <= self.phi <= 180:
            self.g = 0
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        # Cross-polar. off-axis gain
        if 0 <= self.phi < self.z25phi_0:
            self.gx = self.gmax - 25
        elif self.z25phi_0 <= self.phi < self.z44phi_0:
            self.gx = self.gmax - 25 + 8 * ((self.phi - self.z25phi_0)
                                            / (0.19 * self.phi_0))
        elif self.z44phi_0 <= self.phi < self.phi_0:
            self.gx = self.gmax - 17
        elif self.phi_0 <= self.phi < self.phi_1:
            self.gx = self.gmax - 17 + self.s * ((self.phi - self.phi_0) /
                                                 (self.phi_1 - self.phi_0))
        elif self.phi_1 <= self.phi < self.phi_2:
            self.gx = 21 - 25 * log10(self.phi)
        elif self.phi_2 <= self.phi < 70:
            self.gx = - 5
        elif 70 <= self.phi <= 180:
            self.gx = 0
        else:
            self.gx = '\u03C6 > 180 !'
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p

    def test(self):
        assert self.calculate([0, 12.1, 0.6, 0.65]) == \
               [35.75, 10.75, 24.78, 24.22, 35.75, 14.16, 3.84, 3.92, 22.91,
                0.72, 1.26, 2.86, 4.57, 10.96, -14.24]
        assert self.calculate([0.3, 12.1, 0.6, 0.65])[:2] == [35.62, 10.75]
        assert self.calculate([1, 12.1, 0.6, 0.65])[:2] == [34.29, 14.95]
        assert self.calculate([2, 12.1, 0.6, 0.65])[:2] == [29.89, 18.75]
        assert self.calculate([3.9, 12.1, 0.6, 0.65])[:2] == [14.16, 10.07]
        assert self.calculate([4, 12.1, 0.6, 0.65])[:2] == [13.95, 9.24]
        assert self.calculate([8, 12.1, 0.6, 0.65])[:2] == [6.42, -1.58]
        assert self.calculate([50, 12.1, 0.6, 0.65])[:2] == [-5, -5]
        assert self.calculate([100, 12.1, 0.6, 0.65])[:2] == [0, 0]
        assert self.calculate([200, 12.1, 0.6, 0.65])[:2] == ['\u03C6 > 180 !',
                                                              '\u03C6 > 180 !']

