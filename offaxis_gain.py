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
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class Root(Tk):
    def __init__(self):
        super().__init__()
        Rec(self)


class Rec:
    def __init__(self, root):
        self.root = root
        self.root.title('Расчет внеосевого коэффициента усиления антенны')
        self.input_widgets()
        self.btn_calc()
        self.output_widgets()
        self.test()

    def input_widgets(self):
        #   Frame for input data
        self.root.frame_inputs = ttk.LabelFrame(self.root,
                                                text='Входные данные:',
                                                labelanchor="n")
        self.root.frame_inputs.grid(column=0, row=0, padx=5, pady=5)
        #   Label for recommendations combobox
        self.root.label_rec = ttk.Label(self.root.frame_inputs,
                                        text='Рекомендация')
        self.root.label_rec.grid(column=0, row=0, sticky=E, padx=5)
        #   Combobox for recommendations
        self.root.rec = StringVar()
        self.root.combobox_rec = ttk.Combobox(self.root.frame_inputs,
                                              width=20,
                                              textvariable=self.root.rec)
        self.root.combobox_rec['values'] = \
            ('AP30-97', 'AP30B', 'AP7', 'AP8', 'APERR002V01', 'BO.1213',
             'BO.1900', 'S.1855', 'S.465-6', 'S.580-6')
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
        self.root.entry_offaxis_angle =\
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.offaxis_angle, validate='key',
                      validatecommand=(self.vcmd, '%P'))
        self.root.entry_offaxis_angle.grid(column=1, row=1, sticky=W)
        self.root.entry_offaxis_angle.insert(0, '0')

        #   Label for frequency entry
        self.root.label_frequency = ttk.Label(self.root.frame_inputs,
                                              text='Частота (f), ГГц')
        self.root.label_frequency.grid(column=0, row=2, sticky=E, padx=5)
        #   Entry for frequency
        self.root.frequency = StringVar()
        self.root.entry_frequency =\
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.frequency, validate='all',
                      validatecommand=(self.vcmd, '%P'))
        self.root.entry_frequency.grid(column=1, row=2, sticky=W)
        self.root.entry_frequency.insert(0, '14')

        #   Label for diameter entry
        self.root.label_diameter = ttk.Label(self.root.frame_inputs,
                                             text='Диаметр антенны (D), м')
        self.root.label_diameter.grid(column=0, row=3, sticky=E, padx=5)
        #   Entry for diameter
        self.root.diameter = StringVar()
        self.root.entry_diameter =\
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.diameter, validate='all',
                      validatecommand=(self.vcmd, '%P'))
        self.root.entry_diameter.grid(column=1, row=3, sticky=W)
        self.root.entry_diameter.insert(0, '2')

    def btn_calc(self):
        #   Button for calling calculations
        self.root.button_calculate = ttk.Button(self.root, text='Рассчитать')
        self.root.button_calculate.grid(column=0, row=1)
        self.root.button_calculate.bind('<Button-1>', self.set_outputs)

    def output_widgets(self):
        #   Frame for calculated outputs
        self.root.frame_outputs = ttk.LabelFrame(self.root,
                                                 text='Рассчитанные параметры:'
                                                 , labelanchor="n")
        self.root.frame_outputs.grid(column=0, row=2, padx=5, pady=5)
        #   Frame for main outputs
        self.root.frame_main_out = ttk.Frame(self.root.frame_outputs)
        self.root.frame_main_out.grid(column=0, row=0)

        #   Label for co-polarisation off-axis gain entry
        self.root.label_offaxis_gain = \
            ttk.Label(self.root.frame_main_out,
                      text='Ко-пол. внеосевой коэффициент усиления (G), дБ')
        self.root.label_offaxis_gain.grid(column=0, row=0, sticky=E, padx=5,
                                          pady=(0, 10))
        #   Entry for co-polarisation off-axis gain
        self.root.entry_offaxis_gain = \
            ttk.Entry(self.root.frame_main_out, width=10)
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
            from ap8 import AP8
            AP8(self.root)
        elif rec == 'AP7':
            from ap7 import AP7
            AP7(self.root)
        elif rec == 'AP30-97':
            from ap3097 import AP3097
            AP3097(self.root)
            self.root.frequency.set(12.1)
            self.root.diameter.set(0.6)
            self.root.eta.set(0.65)
        elif rec == 'BO.1213':
            from bo1213 import BO1213
            BO1213(self.root)
            self.root.frequency.set(11.7)
            self.root.diameter.set(0.6)
            self.root.eta.set(0.65)
        elif rec == 'BO.1900':
            from bo1900 import BO1900
            BO1900(self.root)
        elif rec == 'AP30B':
            from ap30b import AP30B
            AP30B(self.root)
            self.root.frequency.set(13)
            self.root.diameter.set(2.7)
            self.root.eta.set(0.7)
        elif rec == 'APERR002V01':
            from aperr002v01 import APERR002V01
            APERR002V01(self.root)
            self.root.frequency.set(13)
            self.root.diameter.set(2.7)
            # self.root.eta.set(0.7)
        elif rec == 'S.1855':
            from s1855 import S1855
            S1855(self.root)
        elif rec == 'S.465-6':
            from s465 import S465
            S465(self.root)
        elif rec == 'S.580-6':
            from s580 import S580
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
        self.phi = float(self.root.offaxis_angle.get())
        self.f = float(self.root.frequency.get())
        self.d = float(self.root.diameter.get())
        self.inputs = [self.phi, self.f, self.d]

    def set_outputs(self, event):
        self.get_inputs()
        self.calculate(self.inputs)
        #   Set off-axis gain
        self.root.entry_offaxis_gain.delete(0, END)
        self.root.entry_offaxis_gain.insert(0, self.gr)
        #   Set wavelength
        self.root.entry_wavelength.delete(0, END)
        self.root.entry_wavelength.insert(0, self.wr)
        #   Set D/λ
        self.root.entry_dw.delete(0, END)
        self.root.entry_dw.insert(0, self.dwr)

    def calculate(self, inputs):
        self.s_l = 299792458  # speed of light, m/s
        # off-axis angle (°), frequency (GHz), antenna diameter (m)
        self.phi, self.f, self.d = inputs[:3]
        self.g = ''
        self.a_p = self.add_params()
        self.m_p = self.offaxis_gain()
        self.out = self.m_p + self.a_p
        return self.out

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
        return [self.wr, self.dwr]

        #   Off-axis gain equations
    def offaxis_gain(self):
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        return [self.gr]

    def test(self):
        pass


if __name__ == '__main__':
    Root().mainloop()
