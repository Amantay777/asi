from asi import Rec
from math import log10, sqrt, pi
from tkinter import Tk, E, W, StringVar, IntVar, END
from tkinter import ttk


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
        self.root.entry_phimin.insert(0, self.out[3])

    def calculate(self, inputs):
        self.ab = inputs[3]
        # ab = True, if earth station belongs to the network,
        # coordinated after 1993.
        self.tr = inputs[4]
        # tr = True, if emission direction is transmit
        return super().calculate(inputs)

    def add_params(self):
        self.a_p = super().add_params()
        if 2 <= self.f <= 31:
            if self.ab or self.dw > 100:
                if self.tr or self.dw >= 33.3:
                    if self.dw >= 50:
                        self.phi_min = max(1, 100 * self.w / self.d)
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
        self.phi_minr = round(self.phi_min, 2) if type(self.phi_min) ==\
            float else self.phi_min
        self.a_p += [self.phi_minr]
        return self.a_p

    def offaxis_gain(self):
        if 2 <= self.f <= 31:
            if self.phi < self.phi_min:
                self.g = '\u03C6 < \u03C6_min !'
            elif self.phi > 180:
                self.g = '\u03C6 > 180 !'
            else:
                if self.ab or self.dw > 100:
                    if self.phi_min <= self.phi < 48:
                        self.g = 32 - 25 * log10(self.phi)
                    else:
                        self.g = -10
                else:
                    if self.phi_min <= self.phi < 48:
                        self.g = 52 - 10 * (log10(self.dw)) -\
                                 (25 * log10(self.phi))
                    else:
                        self.g = 10 - 10 * log10(self.dw)
        elif self.f < 2:
            self.g = 'f < 2 ГГц !'
        else:
            self.g = 'f > 31 ГГц !'
        self.m_p = super().offaxis_gain()
        return self.m_p

    def test(self):
        assert self.calculate([1, 14, 1, True, True]) ==\
               ['\u03C6 < \u03C6_min !', 21.41, 46.7, 2]
        assert self.calculate([3, 14, 1, True, True])[0] == 20.07
        assert self.calculate([50, 14, 1, True, True])[0] == -10
        assert self.calculate([200, 14, 1, True, True])[0] == '\u03C6 > 180 !'
        assert self.calculate([1, 14, 3, True, True]) == [32, 21.41, 140.1, 1]
        assert self.calculate([1, 14, 1, False, True]) ==\
               ['\u03C6 < \u03C6_min !', 21.41, 46.7, 2.14]
        assert self.calculate([3, 14, 1, False, True])[0] == 23.38
        assert self.calculate([50, 14, 1, False, True])[0] == -6.69
        assert self.calculate([200, 14, 1, False, True])[0] == '\u03C6 > 180 !'
        assert self.calculate([1, 14, 3, False, True]) == [32, 21.41, 140.1, 1]
        assert self.calculate([1, 3.4, 1, True, False]) ==\
               ['\u03C6 < \u03C6_min !', 88.17, 11.34, 2.5]
        assert self.calculate([1, 3.4, 3, True, False]) ==\
               ['\u03C6 < \u03C6_min !', 88.17, 34.02, 2.44]

    def ref_info(self, txt):
        txt = 'Эталонная диаграмма направленности антенн земных станций ' \
              'фиксированной спутниковой службы для использования при ' \
              'координации и оценке помех в диапазоне частот от 2 до 31 ГГц'
        super().ref_info(txt)