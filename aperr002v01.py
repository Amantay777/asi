from ap8 import AP8
from asi import Rec
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


class APERR002V01(AP8):
    def input_widgets(self):
        super().input_widgets()
        #   Label for eta entry
        self.root.label_eta = \
            ttk.Label(self.root.frame_inputs,
                      text='Коэфф. использ. поверхн. антенны (\u03B7)')
        self.root.label_eta.grid(column=0, row=4, sticky=E, padx=5)
        #   Entry for eta
        self.root.eta = StringVar()
        self.root.entry_eta = \
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.eta, validate='key',
                      validatecommand=(self.eta_vcmd, '%P'))
        self.root.entry_eta.grid(column=1, row=4, sticky=W)
        self.root.entry_eta.insert(0, '0.7')

        self.root.label_coeffa = \
            ttk.Label(self.root.frame_inputs, text='Коэффициент A')
        self.root.label_coeffa.grid(column=0, row=5, sticky=E, padx=5)

        self.root.coeffa_frame = ttk.Frame(self.root.frame_inputs)
        self.root.coeffa_frame.grid(column=1, row=5)

        self.root.coeffa = IntVar()
        self.root.radio_29 = \
            ttk.Radiobutton(self.root.coeffa_frame, text='29', value=29,
                            variable=self.root.coeffa)
        self.root.radio_29.grid(column=0, row=0)
        self.root.radio_29.invoke()

        self.root.radio_32 = \
            ttk.Radiobutton(self.root.coeffa_frame, text='32', value=32,
                            variable=self.root.coeffa)
        self.root.radio_32.grid(column=1, row=0)

    def get_inputs(self):
        super().get_inputs()
        self.eta = float(self.root.eta.get())
        self.coeffa = int(self.root.coeffa.get())
        self.inputs += [self.eta, self.coeffa]

    def add_params(self):
        super().add_params()
        self.gmax_calc()
        self.phib_calc()
        self.g1_calc()
        self.a_p[2:4] = [self.gmaxr, self.g1r]
        self.a_p[6] = self.phi_br
        return self.a_p

    def gmax_calc(self):
        self.gmax = 10 * log10(self.eta * (pi*self.dw) ** 2)
        self.gmaxr = round(self.gmax, 2)

    def phib_calc(self):
        self.phi_b = 10 ** ((self.coeffa + 10) / 25)
        self.phi_br = round(self.phi_b, 2)

    def g1_calc(self):
        self.g1 = 15 * log10(self.dw) - 30 + self.coeffa
        self.g1r = round(self.g1, 2)

    def test(self):
        pass

    def ref_info(self, txt):
        txt = 'Диаграмма направленности антенны земной станции Приложения 30B, ' \
              'применимая для D/lambda > 100. Используется для определения ' \
              'требований по координации и оценки помех в Плане ФСС.'
        Rec.ref_info(self, txt)
