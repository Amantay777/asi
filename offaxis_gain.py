# -----------------------------------------------------------------------------
# Name:        off-axis_gain
# Purpose:
#
# Author:      -
#
# Created:     15.04.2020
# Copyright:   (c) - 2020
# Licence:     <your licence>
# -----------------------------------------------------------------------------
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title('Расчет внеосевого коэффициента усиления антенны')
        #   Frame for input data
        self.frame_inputs = ttk.LabelFrame(self, text='Входные данные:',
                                           labelanchor="n")
        self.frame_inputs.grid(column=0, row=0, padx=5, pady=5)
        #   Button for calling calculations
        self.button_calculate = ttk.Button(self, text='Рассчитать')
        self.button_calculate.grid(column=0, row=1)
        #   Frame for calculated parameters
        self.frame_outputs = ttk.LabelFrame(self,
                                            text='Рассчитанные параметры:',
                                            labelanchor="n")
        self.frame_outputs.grid(column=0, row=2, padx=5, pady=5)
        Rec(self)


class Rec:
    def __init__(self, root):
        self.root = root
        self.input_widgets()
        self.root.button_calculate.bind('<Button-1>', self.set_outputs)
        self.output_widgets()

    def input_widgets(self):
        #   Label for recommendations combobox
        self.root.label_rec = ttk.Label(self.root.frame_inputs,
                                        text='Рекомендация')
        self.root.label_rec.grid(column=0, row=0, sticky=E, padx=5)
        #   Combobox for recommendations
        self.root.rec = StringVar()
        self.root.combobox_rec = ttk.Combobox(self.root.frame_inputs,
                                              width=20,
                                              textvariable=self.root.rec)
        self.root.combobox_rec['values'] = ('AP30-97', 'AP30B', 'AP7',
                                            'AP8', 'S.465-6', 'S.580-6')
        self.root.combobox_rec.grid(column=1, row=0, sticky=W)
        self.root.combobox_rec.bind("<<ComboboxSelected>>", self.check_rec)

        #   Register entry check function
        self.vcmd = self.root.register(self.check_entry)
        #   Register eta entry check function
        self.eta_vcmd = self.root.register(self.check_eta_entry)

        #   Label for off-axis angle entry
        self.root.label_offaxis_angle = ttk.Label(self.root.frame_inputs,
                                                  text=('Внеосевой угол'
                                                        '(\u03C6), \u00b0'))
        self.root.label_offaxis_angle.grid(column=0, row=1, sticky=E, padx=5)
        #   Entry for off-axis angle
        self.root.offaxis_angle = StringVar()
        self.root.entry_offaxis_angle = ttk.Entry(self.root.frame_inputs,
                                                  width=10,
                                                  textvariable=self.root.
                                                  offaxis_angle,
                                                  validate='key',
                                                  validatecommand=(self.vcmd,
                                                                   '%P'))
        self.root.entry_offaxis_angle.grid(column=1, row=1, sticky=W)
        self.root.entry_offaxis_angle.insert(0, '0')

        #   Label for frequency entry
        self.root.label_frequency = ttk.Label(self.root.frame_inputs,
                                              text='Частота (f), ГГц')
        self.root.label_frequency.grid(column=0, row=2, sticky=E, padx=5)
        #   Entry for frequency
        self.root.frequency = StringVar()
        self.root.entry_frequency = ttk.Entry(self.root.frame_inputs,
                                              width=10,
                                              textvariable=self.root.frequency,
                                              validate='all',
                                              validatecommand=(self.vcmd,
                                                               '%P'))
        self.root.entry_frequency.grid(column=1, row=2, sticky=W)
        self.root.entry_frequency.insert(0, '14')

        #   Label for diameter entry
        self.root.label_diameter = ttk.Label(self.root.frame_inputs,
                                             text='Диаметр антенны (D), м')
        self.root.label_diameter.grid(column=0, row=3, sticky=E, padx=5)
        #   Entry for diameter
        self.root.diameter = StringVar()
        self.root.entry_diameter = ttk.Entry(self.root.frame_inputs,
                                             width=10,
                                             textvariable=self.root.diameter,
                                             validate='all',
                                             validatecommand=(self.vcmd, '%P'))
        self.root.entry_diameter.grid(column=1, row=3, sticky=W)
        self.root.entry_diameter.insert(0, '2')

    def output_widgets(self):
        #   Frame for main outputs
        self.root.frame_main_out = ttk.Frame(self.root.frame_outputs)
        self.root.frame_main_out.grid(column=0, row=0)

        #   Label for co-polarisation off-axis gain entry
        self.root.label_offaxis_gain = ttk.Label(self.root.frame_main_out,
                                                 text=('Ко-пол. внеосевой коэф'
                                                       'фициент усиления (G), '
                                                       'дБ'))
        self.root.label_offaxis_gain.grid(column=0, row=0, sticky=E, padx=5,
                                          pady=(0, 10))
        #   Entry for co-polarisation off-axis gain
        self.root.entry_offaxis_gain = ttk.Entry(self.root.frame_main_out,
                                                 width=10)
        self.root.entry_offaxis_gain.grid(column=1, row=0, sticky=W,
                                          pady=(0, 10))

        #   Frame for additional outputs
        self.root.frame_add_out = ttk.Frame(self.root.frame_outputs)
        self.root.frame_add_out.grid(column=0, row=1)

        #   Label for wavelength entry
        self.root.label_wavelength = ttk.Label(self.root.frame_add_out,
                                               text=('Длина волны (\u03BB), '
                                                     'мм'))
        self.root.label_wavelength.grid(column=0, row=0, sticky=E,
                                        padx=5)
        #   Entry for wavelength
        self.root.entry_wavelength = ttk.Entry(self.root.frame_add_out,
                                               width=10)
        self.root.entry_wavelength.grid(column=1, row=0, sticky=W)

        #   Label for D/λ entry
        self.root.label_dw = ttk.Label(self.root.frame_add_out,
                                       text='Отношение D/\u03BB')
        self.root.label_dw.grid(column=0, row=1, sticky=E, padx=5)
        #   Entry for D/λ
        self.root.entry_dw = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_dw.grid(column=1, row=1, sticky=W)

    def check_rec(self, event):
        self.clean_previous()
        rec = self.root.rec.get()
        offaxis_angle = self.root.offaxis_angle.get()
        frequency = self.root.frequency.get()
        diameter = self.root.diameter.get()
        if rec == 'AP8':
            AP8(self.root)
        elif rec == 'AP7':
            AP7(self.root)
        elif rec == 'AP30-97':
            AP30_97(self.root)
            self.root.frequency.set(12.1)
            self.root.diameter.set(0.6)
            self.root.eta.set(0.65)
        elif rec == 'AP30B':
            AP30B(self.root)
            self.root.frequency.set(13)
            self.root.diameter.set(2.7)
            self.root.eta.set(0.7)
        elif rec == 'S.465-6':
            S465(self.root)
        elif rec == 'S.580-6':
            S580(self.root)
        self.root.rec.set(rec)
        self.root.offaxis_angle.set(offaxis_angle)
        if rec not in ['AP30-97', 'AP30B']:
            self.root.frequency.set(frequency)
            self.root.diameter.set(diameter)

    def clean_previous(self):
        for widget in self.root.frame_inputs.grid_slaves():
            if int(widget.grid_info()["row"]) > 3:
                widget.destroy()
        for widget in self.root.frame_main_out.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        for widget in self.root.frame_main_out.grid_slaves(column=1):
            widget.delete(0, END)
        for widget in self.root.frame_add_out.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.destroy()
        for widget in self.root.frame_add_out.grid_slaves(column=1):
            widget.delete(0, END)

    def check_entry(self, P):
        try:
            if P == "" or float(P) >= 0:
                return True
            return False
        except ValueError:
            return False

    def check_eta_entry(self, P):
        try:
            if P == "0." or 0.5 <= float(P) <= 0.7:
                return True
            return False
        except ValueError:
            return False

    def get_inputs(self):
        self.offaxis_angle = float(self.root.offaxis_angle.get())
        self.frequency = float(self.root.frequency.get())
        self.diameter = float(self.root.diameter.get())
        self.inputs = [self.offaxis_angle, self.frequency, self.diameter]

    def set_outputs(self, event):
        self.get_inputs()
        self.outputs = self.Equations(self.inputs).outputs
        #   Set off-axis gain
        self.root.entry_offaxis_gain.delete(0, END)
        self.root.entry_offaxis_gain.insert(0, self.outputs[0])
        #   Set wavelength
        self.root.entry_wavelength.delete(0, END)
        self.root.entry_wavelength.insert(0, self.outputs[1])
        #   Set D/λ
        self.root.entry_dw.delete(0, END)
        self.root.entry_dw.insert(0, self.outputs[2])

    class Equations:

        def __init__(self, inputs):
            self.s_l = 299792458  # speed of light, m/s
            # off-axis angle (°), frequency (GHz), antenna diameter (m)
            self.phi, self.f, self.d = inputs[:3]
            self.g = ''
            self.add_params()
            self.offaxis_gain()
            self.outputs = [self.gr, self.wr, self.dwr]

        #   Additional parameter equations
        def add_params(self):
            # длина волны, м
            self.w = self.s_l / (self.f * 10 ** 9) if self.f > 0 else 'f = 0 !'
            # длина волны, мм
            self.wr = (round(10 ** 3 * self.w, 2) if type(self.w) == float
                       else self.w)
            # отношение диаметра антенны к длине волны
            if self.d > 0 and self.f > 0:
                self.dw = self.d / self.w
            elif self.d == 0:
                self.dw = 'd = 0 !'
            else:
                self.dw = 'f = 0 !'
            self.dwr = round(self.dw, 2) if type(self.dw) == float else self.dw

        #   Off-axis gain equations
        def offaxis_gain(self):
            self.gr = round(self.g, 2) if type(self.g) == float else self.g


class AP8(Rec):
    def output_widgets(self):
        super().output_widgets()

        #   Label for Gmax entry
        self.root.label_gmax = ttk.Label(self.root.frame_add_out,
                                         text=('Макс. коэффициент усиления '
                                               '(Gmax), дБ'))
        self.root.label_gmax.grid(column=0, row=2, sticky=E, padx=5)
        #   Entry for Gmax
        self.root.entry_gmax = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_gmax.grid(column=1, row=2, sticky=W)

        #   Label for G1 entry
        self.root.label_g1 = ttk.Label(self.root.frame_add_out,
                                       text=('Усиление 1-й бок. лепестка (G1),'
                                             ' дБ'))
        self.root.label_g1.grid(column=0, row=3, sticky=E, padx=5)
        #   Entry for G1
        self.root.entry_g1 = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_g1.grid(column=1, row=3, sticky=W)

        #   Label for φm
        self.root.label_phim = ttk.Label(self.root.frame_add_out,
                                         text=('Внеосевой угол начала G1 '
                                               '(\u03C6m), \u00b0'))
        self.root.label_phim.grid(column=0, row=4, sticky=E, padx=5)
        #   Entry for φm
        self.root.entry_phim = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phim.grid(column=1, row=4, sticky=W)

        #   Label for φr
        self.root.label_phir = ttk.Label(self.root.frame_add_out,
                                         text=('Внеосевой угол конца G1 '
                                               '(\u03C6r), \u00b0'))
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
        self.root.entry_gmax.insert(0, self.outputs[3])
        #   Set G1
        self.root.entry_g1.delete(0, END)
        self.root.entry_g1.insert(0, self.outputs[4])
        #   Set φm
        self.root.entry_phim.delete(0, END)
        self.root.entry_phim.insert(0, self.outputs[5])
        #   Set φr
        self.root.entry_phir.delete(0, END)
        self.root.entry_phir.insert(0, self.outputs[6])
        #   Set φb
        self.root.entry_phib.delete(0, END)
        self.root.entry_phib.insert(0, self.outputs[7])

    class Equations(Rec.Equations):
        def __init__(self, inputs):
            super().__init__(inputs)
            self.outputs += [self.gmaxr, self.g1r, self.phi_mr, self.phi_rr,
                             self.phi_br]

        def add_params(self):
            super().add_params()
            self.gmax = 20 * log10(self.dw) + 7.7
            self.gmaxr = round(self.gmax, 2)
            self.g1 = 2 + 15 * log10(self.dw)
            self.g1r = round(self.g1, 2)
            self.phi_m = (20 * self.w / self.d) * sqrt(self.gmax - self.g1)
            self.phi_mr = round(self.phi_m, 2)
            if self.dw >= 100:
                self.phi_r = 15.85 * self.dw ** (-0.6)
            else:
                self.phi_r = 100 * self.w / self.d
            self.phi_rr = round(self.phi_r, 2)
            self.phi_br = self.phi_b = 48

        def offaxis_gain(self):
            if self.phi == 0:
                self.g = self.gmax
            elif 0 < self.phi < self.phi_m:
                self.g = self.gmax - 2.5 * 10**(-3) * (self.dw * self.phi)**2
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
            super().offaxis_gain()


class AP7(AP8):

    class Equations(AP8.Equations):
        def add_params(self):
            super().add_params()
            if self.dw < 35:
                self.gmaxr = self.g1r = self.phi_mr = 'D/\u03BB < 35 !'
                self.phi_rr = self.phi_br = 'D/\u03BB < 35 !'
            else:
                if self.dw >= 100:
                    self.g1 = -1 + 15 * log10(self.dw)
                else:
                    self.g1 = -21 + 25 * log10(self.dw)
                self.g1r = round(self.g1, 2)
                self.phi_m = 20 * (self.w / self.d) * sqrt(self.gmax - self.g1)
                self.phi_mr = round(self.phi_m, 2)
                self.phi_br = self.phi_b = 36

        def offaxis_gain(self):
            if self.dw < 35:
                self.g = 'D/\u03BB < 35 !'
            else:
                super().offaxis_gain()
            if self.phi_r <= self.phi < self.phi_b:
                self.g = 29 - 25 * log10(self.phi)
            elif self.phi_b <= self.phi <= 180:
                self.g = - 10
            super(AP8.Equations, self).offaxis_gain()


class AP30_97(AP8):
    def input_widgets(self):
        super().input_widgets()

        #   Label for eta entry
        self.root.label_eta = ttk.Label(self.root.frame_inputs,
                                        text=('Коэфф. использ. поверхн. '
                                              'антенны (\u03B7)'))
        self.root.label_eta.grid(column=0, row=4, sticky=E, padx=5)
        #   Entry for eta
        self.root.eta = StringVar()
        self.root.entry_eta = ttk.Entry(self.root.frame_inputs, width=10,
                                        textvariable=self.root.eta,
                                        validate='key',
                                        validatecommand=(self.eta_vcmd, '%P'))
        self.root.entry_eta.grid(column=1, row=4, sticky=W)
        self.root.entry_eta.insert(0, '0.65')

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

    def get_inputs(self):
        super().get_inputs()
        self.eta = float(self.root.eta.get())
        self.inputs += [self.eta]

    def set_outputs(self, event):
        super().set_outputs(event)
        #   Set Gx
        self.root.entry_offaxis_gain_x.delete(0, END)
        self.root.entry_offaxis_gain_x.insert(0, self.outputs[8])
        #   Set 0.25*φ0
        self.root.entry_z25phi0.delete(0, END)
        self.root.entry_z25phi0.insert(0, self.outputs[9])
        #   Set 0.44*φ0
        self.root.entry_z44phi0.delete(0, END)
        self.root.entry_z44phi0.insert(0, self.outputs[10])
        #   Set φ0
        self.root.entry_phi0.delete(0, END)
        self.root.entry_phi0.insert(0, self.outputs[11])
        #   Set φ1
        self.root.entry_phi1.delete(0, END)
        self.root.entry_phi1.insert(0, self.outputs[12])
        #   Set φ2
        self.root.entry_phi2.delete(0, END)
        self.root.entry_phi2.insert(0, self.outputs[13])
        #   Set S
        self.root.entry_s.delete(0, END)
        self.root.entry_s.insert(0, self.outputs[14])

    class Equations(AP8.Equations):
        def __init__(self, inputs):
            self.eta = inputs[3]
            super().__init__(inputs)
            self.outputs += [self.gxr, self.z25phi_0r, self.z44phi_0r,
                             self.phi_0r, self.phi_1r, self.phi_2r, self.cr]

        def add_params(self):
            super().add_params()
            self.gmax = 10 * log10(self.eta * (pi*self.dw) ** 2)
            self.gmaxr = round(self.gmax, 2)
            self.phi_r = 95 * self.w / self.d
            self.phi_rr = round(self.phi_r, 2)
            self.g1 = 29 - 25 * log10(self.phi_r)
            self.g1r = round(self.g1, 2)
            self.phi_m = (self.w / self.d) * sqrt((self.gmax - self.g1)/0.0025)
            self.phi_mr = round(self.phi_m, 2)
            self.phi_b = 10 ** (34 / 25)
            self.phi_br = round(self.phi_b, 2)
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
            self.c = 21 - 25 * log10(self.phi_1) - (self.gmax - 17)
            self.cr = round(self.c, 2)

        def offaxis_gain(self):
            super().offaxis_gain()
            # Co-polar. off-axis gain
            if self.phi_r <= self.phi < self.phi_b:
                self.g = 29 - 25 * log10(self.phi)
            elif self.phi_b <= self.phi < 70:
                self.g = - 5
            elif 70 <= self.phi <= 180:
                self.g = 0
            super(AP8.Equations, self).offaxis_gain()
            # Cross-polar. off-axis gain
            if 0 <= self.phi < self.z25phi_0:
                self.gx = self.gmax - 25
            elif self.z25phi_0 <= self.phi < self.z44phi_0:
                self.gx = self.gmax - 25 + 8 * ((self.phi - self.z25phi_0)
                                                / (0.19 * self.phi_0))
            elif self.z44phi_0 <= self.phi < self.phi_0:
                self.gx = self.gmax - 17
            elif self.phi_0 <= self.phi < self.phi_1:
                self.gx = self.gmax - 17 + self.c * ((self.phi - self.phi_0)
                                                     / (self.phi_1
                                                        - self.phi_0))
            elif self.phi_1 <= self.phi < self.phi_2:
                self.gx = 21 - 25 * log10(self.phi)
            elif self.phi_2 <= self.phi < 70:
                self.gx = - 5
            elif 70 <= self.phi <= 180:
                self.gx = 0
            else:
                self.gx = '\u03C6 > 180 !'
            self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx


class AP30B(AP30_97):
    def output_widgets(self):
        AP8.output_widgets(self)
        self.root.label_phir.destroy()
        self.root.entry_phir.destroy()
        self.root.label_phib.destroy()
        self.root.entry_phib.destroy()

    def set_outputs(self, event):
        Rec.set_outputs(self, event)
        #   Set Gmax
        self.root.entry_gmax.delete(0, END)
        self.root.entry_gmax.insert(0, self.outputs[3])
        #   Set G1
        self.root.entry_g1.delete(0, END)
        self.root.entry_g1.insert(0, self.outputs[4])
        #   Set φm
        self.root.entry_phim.delete(0, END)
        self.root.entry_phim.insert(0, self.outputs[5])

    class Equations(AP30_97.Equations):
        def __init__(self, inputs):
            self.eta = inputs[3]
            Rec.Equations.__init__(self, inputs)
            self.outputs += [self.gmaxr, self.g1r, self.phi_mr]

        def add_params(self):
            super().add_params()
            self.g1 = - 1 + 15 * log10(self.dw)
            self.g1r = round(self.g1, 2)
            self.phi_m = (20 * self.w / self.d) * sqrt(self.gmax - self.g1)
            self.phi_mr = round(self.phi_m, 2)

        def offaxis_gain(self):
            super().offaxis_gain()
            if self.phi_m <= self.phi <= 19.95:
                self.g = min(self.g1, 29 - 25 * log10(self.phi))
            elif 19.95 < self.phi <= 180:
                self.g = max(min(- 3.5, 32 - 25 * log10(self.phi)), -10)
            self.gr = round(self.g, 2) if type(self.g) == float else self.g


class S465(Rec):
    def input_widgets(self):
        super().input_widgets()

        self.root.label_date = ttk.Label(self.root.frame_inputs,
                                         text='Дата заявления сети: ')
        self.root.label_date.grid(column=0, row=4, sticky=E, padx=5)

        self.root.date_frame = ttk.Frame(self.root.frame_inputs)
        self.root.date_frame.grid(column=1, row=4)

        self.root.after_before = IntVar()
        self.root.radio_after = ttk.Radiobutton(self.root.date_frame,
                                                text='После 1993 г.',
                                                value=1,
                                                variable=self.root.
                                                after_before)
        self.root.radio_after.grid(column=0, row=0)
        self.root.radio_after.invoke()

        self.root.radio_before = ttk.Radiobutton(self.root.date_frame,
                                                 text='До 1993 г.', value=0,
                                                 variable=self.root.
                                                 after_before)
        self.root.radio_before.grid(column=1, row=0)

        self.root.label_tx_rx = ttk.Label(self.root.frame_inputs,
                                          text='Направление излучения')
        self.root.label_tx_rx.grid(column=0, row=5, sticky=E, padx=5)

        self.root.frame_tx_rx = ttk.Frame(self.root.frame_inputs)
        self.root.frame_tx_rx.grid(column=1, row=5)

        self.root.tx_rx = IntVar()
        self.root.radio_tx = ttk.Radiobutton(self.root.frame_tx_rx,
                                             text='Передача', value=1,
                                             variable=self.root.tx_rx)
        self.root.radio_tx.grid(column=0, row=0)
        self.root.radio_tx.invoke()

        self.root.radio_rx = ttk.Radiobutton(self.root.frame_tx_rx,
                                             text='Прием', value=0,
                                             variable=self.root.tx_rx)
        self.root.radio_rx.grid(column=1, row=0)

    def output_widgets(self):
        self.root.label_phimin = ttk.Label(self.root.frame_add_out,
                                           text=('Минимальный внеосевой '
                                                 'угол (\u03C6min), \u00b0'))
        self.root.label_phimin.grid(column=0, row=2, sticky=E, padx=5)

        self.root.entry_phimin = ttk.Entry(self.root.frame_add_out, width=10)
        self.root.entry_phimin.grid(column=1, row=2, sticky=W)

    def get_inputs(self):
        super().get_inputs()
        self.after_before = self.root.after_before.get()
        self.tx_rx = self.root.tx_rx.get()
        self.inputs += [self.after_before, self.tx_rx]

    def set_outputs(self, event):
        super().set_outputs(event)
        #   Set φmin
        self.root.entry_phimin.delete(0, END)
        self.root.entry_phimin.insert(0, self.outputs[3])

    class Equations(Rec.Equations):
        def __init__(self, inputs):
            self.ab = inputs[3]
            # ab = True, если земная станция принадлежит сети,
            # координируемой после 1993 г.
            self.tr = inputs[4]
        # tr = True, если направление излучения - передача
            super().__init__(inputs)
            self.outputs += [self.phi_minr]

        def add_params(self):
            super().add_params()

            if 2 <= self.f <= 31:
                if (self.ab or self.dw > 100):
                    if (self.tr or self.dw >= 33.3):
                        if self.dw >= 50:
                            self.phi_min = max(1, 100 * self.w / self.d)
                        # минимальный внеосевой угол, градусов
                        else:
                            self.phi_min = max(2, 114 * (self.dw) ** (- 1.09))
                    else:
                        self.phi_min = 2.5
                else:
                    self.phi_min = 100 * self.w / self.d
            elif self.f < 2:
                self.phi_min = 'f < 2 ГГц !'
            else:
                self.phi_min = 'f > 31 ГГц !'
            self.phi_minr = round(self.phi_min, 2) if (type(self.phi_min)
                                                       == float) else (
                                                           self.phi_min)

        def offaxis_gain(self):
            if 2 <= self.f <= 31:
                if self.phi < self.phi_min:
                    self.g = '\u03C6 < \u03C6_min !'
                # внеосевой коэффициент усиления антенны, дБ
                elif self.phi > 180:
                    self.g = '\u03C6 > 180 !'
                else:
                    if (self.ab or self.dw > 100):
                        if self.phi_min <= self.phi < 48:
                            self.g = 32 - 25 * log10(self.phi)
                        else:
                            self.g = -10
                    else:
                        if self.phi_min <= self.phi < 48:
                            self.g = 52 - 10 * (
                                log10(self.dw)) - (
                                    25 * log10(self.phi))
                        else:
                            self.g = 10 - 10 * log10(self.dw)
            elif self.f < 2:
                self.g = 'f < 2 ГГц !'
            else:
                self.g = 'f > 31 ГГц !'
            super().offaxis_gain()


class S580(S465):
    def input_widgets(self):
        super().input_widgets()
        self.root.label_tx_rx.destroy()
        self.root.frame_tx_rx.destroy()

    def get_inputs(self):
        super(S465, self).get_inputs()
        self.after_before = self.root.after_before.get()
        self.inputs += [self.after_before]

    class Equations(Rec.Equations):
        def __init__(self, inputs):
            self.inputs = inputs
            self.ab = inputs[3]
            # ab = True, если земная станция принадлежит сети,
            # координируемой после 1993 г.
            super().__init__(inputs)
            self.outputs += [self.phi_minr]

        def add_params(self):
            super().add_params()
            if self.dw >= 50:
                # минимальный внеосевой угол, градусов
                self.phi_min = max(1, 100 * self.w / self.d)
            else:
                self.phi_min = ''
            self.phi_minr = round(self.phi_min, 2) if (type(self.phi_min)
                                                       == float) else (
                                                           self.phi_min)

        def offaxis_gain(self):
            if self.dw >= 50:
                if self.phi < self.phi_min:
                    self.g = AP7.Equations(self.inputs).g
                # внеосевой коэффициент усиления антенны, дБ
                elif self.phi_min <= self.phi <= 20:
                    self.g = 29 - 25 * log10(self.phi)
                    # elif (20 < self.phi <= 26.3):
                    # self.g = -3.5
                else:
                    self.g = S465.Equations(self.inputs + [True]).g
            else:
                self.g = 'D/\u03BB < 50 !'
            super().offaxis_gain()


class TestEquations:
    def __init__(self):
        self.AP30_97()
        self.AP30B()
        self.AP7()
        self.AP8()
        self.S465()
        self.S580()

    def AP30_97(self):
        assert AP30_97.Equations([0, 12.1, 0.6, 0.65
                                  ]).outputs == [35.75, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 10.75, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([0.3, 12.1, 0.6, 0.65
                                  ]).outputs == [35.62, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 10.75, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([1, 12.1, 0.6, 0.65
                                  ]).outputs == [34.29, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 14.95, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([2, 12.1, 0.6, 0.65
                                  ]).outputs == [29.89, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 18.75, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([4, 12.1, 0.6, 0.65
                                  ]).outputs == [13.95, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 9.24, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([8, 12.1, 0.6, 0.65
                                  ]).outputs == [6.42, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 -1.58, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([50, 12.1, 0.6, 0.65
                                  ]).outputs == [-5, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 -5, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([100, 12.1, 0.6, 0.65
                                  ]).outputs == [0, 24.78, 24.22, 35.75,
                                                 14.16, 3.84, 3.92, 22.91,
                                                 0, 0.72, 1.26, 2.86, 4.57,
                                                 10.96, -14.24]
        assert AP30_97.Equations([200, 12.1, 0.6, 0.65
                                  ]).outputs == ['\u03C6 > 180 !', 24.78,
                                                 24.22, 35.75, 14.16, 3.84,
                                                 3.92, 22.91, '\u03C6 > 180 !',
                                                 0.72, 1.26, 2.86, 4.57, 10.96,
                                                 -14.24]

    def AP30B(self):
        assert AP30B.Equations([0, 13, 2.7, 0.7
                                ]).outputs == [49.76, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([0.3, 13, 2.7, 0.7
                                ]).outputs == [46.68, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([0.8, 13, 2.7, 0.7
                                ]).outputs == [30.03, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([10, 13, 2.7, 0.7
                                ]).outputs == [4.0, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([20, 13, 2.7, 0.7
                                ]).outputs == [-3.5, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([40, 13, 2.7, 0.7
                                ]).outputs == [-8.05, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([100, 13, 2.7, 0.7
                                ]).outputs == [-10, 23.06, 117.08, 49.76,
                                               30.03, 0.76]
        assert AP30B.Equations([200, 13, 2.7, 0.7
                                ]).outputs == ['\u03C6 > 180 !', 23.06, 117.08,
                                               49.76, 30.03, 0.76]

    def AP7(self):
        assert AP7.Equations([0, 14, 0.6]).outputs == ['D/\u03BB < 35 !',
                                                       21.41, 28.02,
                                                       'D/\u03BB < 35 !',
                                                       'D/\u03BB < 35 !',
                                                       'D/\u03BB < 35 !',
                                                       'D/\u03BB < 35 !',
                                                       'D/\u03BB < 35 !']
        assert AP7.Equations([0, 14, 3]).outputs == [50.63, 21.41, 140.1,
                                                     50.63, 31.2, 0.63, 0.82,
                                                     36]
        assert AP7.Equations([0.3, 14, 3]).outputs == [46.21, 21.41, 140.1,
                                                       50.63, 31.2, 0.63, 0.82,
                                                       36]
        assert AP7.Equations([0.7, 14, 3]).outputs == [31.2, 21.41, 140.1,
                                                       50.63, 31.2, 0.63, 0.82,
                                                       36]
        assert AP7.Equations([20, 14, 3]).outputs == [-3.53, 21.41, 140.1,
                                                      50.63, 31.2, 0.63, 0.82,
                                                      36]
        assert AP7.Equations([100, 14, 3]).outputs == [-10, 21.41, 140.1,
                                                       50.63, 31.2, 0.63, 0.82,
                                                       36]
        assert AP7.Equations([200, 14, 3]).outputs == ['\u03C6 > 180 !', 21.41,
                                                       140.1, 50.63, 31.2,
                                                       0.63, 0.82, 36]
        assert AP7.Equations([0, 14, 1]).outputs == [41.09, 21.41, 46.7, 41.09,
                                                     20.73, 1.93, 2.14, 36]
        assert AP7.Equations([1, 14, 1]).outputs == [35.63, 21.41, 46.7, 41.09,
                                                     20.73, 1.93, 2.14, 36]
        assert AP7.Equations([2, 14, 1]).outputs == [20.73, 21.41, 46.7, 41.09,
                                                     20.73, 1.93, 2.14, 36]
        assert AP7.Equations([20, 14, 1]).outputs == [-3.53, 21.41, 46.7,
                                                      41.09, 20.73, 1.93, 2.14,
                                                      36]
        assert AP7.Equations([100, 14, 1]).outputs == [-10, 21.41, 46.7, 41.09,
                                                       20.73, 1.93, 2.14, 36]
        assert AP7.Equations([200, 14, 1]).outputs == ['\u03C6 > 180 !', 21.41,
                                                       46.7, 41.09, 20.73,
                                                       1.93, 2.14, 36]

    def AP8(self):
        assert AP8.Equations([0, 14, 3]).outputs == [50.63, 21.41, 140.1,
                                                     50.63, 34.2, 0.58, 0.82,
                                                     48]
        assert AP8.Equations([0.3, 14, 3]).outputs == [46.21, 21.41, 140.1,
                                                       50.63, 34.2, 0.58, 0.82,
                                                       48]
        assert AP8.Equations([0.7, 14, 3]).outputs == [34.2, 21.41, 140.1,
                                                       50.63, 34.2, 0.58, 0.82,
                                                       48]
        assert AP8.Equations([20, 14, 3]).outputs == [-0.53, 21.41, 140.1,
                                                      50.63, 34.2, 0.58, 0.82,
                                                      48]
        assert AP8.Equations([100, 14, 3]).outputs == [-10, 21.41, 140.1,
                                                       50.63, 34.2, 0.58, 0.82,
                                                       48]
        assert AP8.Equations([200, 14, 3]).outputs == ['\u03C6 > 180 !', 21.41,
                                                       140.1, 50.63, 34.2,
                                                       0.58, 0.82, 48]
        assert AP8.Equations([0, 14, 1]).outputs == [41.09, 21.41, 46.7,
                                                     41.09, 27.04, 1.61, 2.14,
                                                     48]
        assert AP8.Equations([0.8, 14, 1]).outputs == [37.6, 21.41, 46.7,
                                                       41.09, 27.04, 1.61,
                                                       2.14, 48]
        assert AP8.Equations([2, 14, 1]).outputs == [27.04, 21.41, 46.7,
                                                     41.09, 27.04, 1.61, 2.14,
                                                     48]
        assert AP8.Equations([20, 14, 1]).outputs == [2.78, 21.41, 46.7,
                                                      41.09, 27.04, 1.61, 2.14,
                                                      48]
        assert AP8.Equations([100, 14, 1]).outputs == [-6.69, 21.41, 46.7,
                                                       41.09, 27.04, 1.61,
                                                       2.14, 48]
        assert AP8.Equations([200, 14, 1]).outputs == ['\u03C6 > 180 !',
                                                       21.41, 46.7, 41.09,
                                                       27.04, 1.61, 2.14, 48]

    def S465(self):
        assert S465.Equations([1, 14, 1, True, True
                               ]).outputs == ['\u03C6 < \u03C6_min !',
                                              21.41, 46.7, 2]
        assert S465.Equations([3, 14, 1, True, True
                               ]).outputs == [20.07, 21.41, 46.7, 2]
        assert S465.Equations([49, 14, 1, True, True
                               ]).outputs == [-10, 21.41, 46.7, 2]
        assert S465.Equations([181, 14, 1, True, True
                               ]).outputs == ['\u03C6 > 180 !', 21.41, 46.7, 2]
        assert S465.Equations([1, 14, 3, True, True
                               ]).outputs == [32, 21.41, 140.1, 1]
        assert S465.Equations([3, 14, 3, True, True
                               ]).outputs == [20.07, 21.41, 140.1, 1]
        assert S465.Equations([49, 14, 3, True, True
                               ]).outputs == [-10, 21.41, 140.1, 1]
        assert S465.Equations([181, 14, 3, True, True
                               ]).outputs == ['\u03C6 > 180 !',
                                              21.41, 140.1, 1]

        assert S465.Equations([1, 14, 1, False, True
                               ]).outputs == ['\u03C6 < \u03C6_min !',
                                              21.41, 46.7, 2.14]
        assert S465.Equations([3, 14, 1, False, True
                               ]).outputs == [23.38, 21.41, 46.7, 2.14]
        assert S465.Equations([49, 14, 1, False, True
                               ]).outputs == [-6.69, 21.41, 46.7, 2.14]
        assert S465.Equations([181, 14, 1, False, True
                               ]).outputs == ['\u03C6 > 180 !', 21.41, 46.7,
                                              2.14]
        assert S465.Equations([1, 14, 3, False, True
                               ]).outputs == [32, 21.41, 140.1, 1]
        assert S465.Equations([3, 14, 3, False, True
                               ]).outputs == [20.07, 21.41, 140.1, 1]
        assert S465.Equations([49, 14, 3, False, True
                               ]).outputs == [-10, 21.41, 140.1, 1]
        assert S465.Equations([181, 14, 3, False, True
                               ]).outputs == ['\u03C6 > 180 !', 21.41, 140.1,
                                              1]

        assert S465.Equations([1, 3.4, 1, True, False
                               ]).outputs == ['\u03C6 < \u03C6_min !', 88.17,
                                              11.34, 2.5]
        assert S465.Equations([3, 3.4, 1, True, False
                               ]).outputs == [20.07, 88.17, 11.34, 2.5]
        assert S465.Equations([49, 3.4, 1, True, False
                               ]).outputs == [-10, 88.17, 11.34, 2.5]
        assert S465.Equations([181, 3.4, 1, True, False
                               ]).outputs == ['\u03C6 > 180 !', 88.17, 11.34,
                                              2.5]
        assert S465.Equations([1, 3.4, 3, True, False
                               ]).outputs == ['\u03C6 < \u03C6_min !', 88.17,
                                              34.02, 2.44]
        assert S465.Equations([3, 3.4, 3, True, False
                               ]).outputs == [20.07, 88.17, 34.02, 2.44]
        assert S465.Equations([49, 3.4, 3, True, False
                               ]).outputs == [-10, 88.17, 34.02, 2.44]
        assert S465.Equations([181, 3.4, 3, True, False
                               ]).outputs == ['\u03C6 > 180 !', 88.17, 34.02,
                                              2.44]

    def S580(self):
        assert S580.Equations([1, 14, 1, True
                               ]).outputs == ['D/\u03BB < 50 !', 21.41, 46.7,
                                              '']
        assert S580.Equations([1, 14, 1.1, True
                               ]).outputs == [35.32, 21.41, 51.37, 1.95]
        assert S580.Equations([3, 14, 1.1, True
                               ]).outputs == [17.07, 21.41, 51.37, 1.95]
        assert S580.Equations([21, 14, 1.1, True
                               ]).outputs == [-1.06, 21.41, 51.37, 1.95]
        assert S580.Equations([27, 14, 1.1, True
                               ]).outputs == [-3.78, 21.41, 51.37, 1.95]
        assert S580.Equations([49, 14, 1.1, True
                               ]).outputs == [-10, 21.41, 51.37, 1.95]
        assert S580.Equations([181, 14, 1.1, True
                               ]).outputs == ['\u03C6 > 180 !', 21.41, 51.37,
                                              1.95]


TestEquations()
Root().mainloop()
