from tkinter import Tk, E, W, StringVar, END
from tkinter import ttk
from math import log10


class SD:
    def __init__(self, root):
        self.root = root
        self.input_widgets()
        self.btn_calc()
        self.output_widgets()

    def input_widgets(self):
        #   Frame for input data
        self.root.frame_inputs = \
            ttk.LabelFrame(self.root, text='Входные данные:', labelanchor="n")
        self.root.frame_inputs.grid(column=0, row=0, padx=5, pady=5)
        self.eirp_widgets()
        self.bandwidth_widgets()

    def eirp_widgets(self):
        #   Label for EIRP entry
        self.root.label_eirp = ttk.Label(self.root.frame_inputs,
                                            text='ЭИИМ, дБВт')
        self.root.label_eirp.grid(column=0, row=2, sticky=E, padx=5)
        #   Entry for EIRP
        self.root.eirp = StringVar()
        self.root.entry_eirp = \
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.eirp, validate='all')
        # , validatecommand=(Rec.vcmd, '%P'))
        self.root.entry_eirp.grid(column=1, row=2, sticky=W)
        self.root.entry_eirp.insert(0, '56')

    def bandwidth_widgets(self):
        #   Label for bandwidth entry
        self.root.label_bandwidth = ttk.Label(self.root.frame_inputs,
                                            text='Ширина полосы, МГц')
        self.root.label_bandwidth.grid(column=0, row=3, sticky=E, padx=5)
        #   Entry for bandwidth
        self.root.bandwidth = StringVar()
        self.root.entry_bandwidth = \
            ttk.Entry(self.root.frame_inputs, width=10,
                      textvariable=self.root.bandwidth, validate='all')
        # , validatecommand=(Rec.vcmd, '%P'))
        self.root.entry_bandwidth.grid(column=1, row=3, sticky=W)
        self.root.entry_bandwidth.insert(0, '54')

    def btn_calc(self):
        #   Button for calling calculations
        self.root.button_calculate = ttk.Button(self.root, text='Рассчитать')
        self.root.button_calculate.grid(column=0, row=1)
        self.root.button_calculate.bind('<Button-1>', self.set_outputs)

    def output_widgets(self):
        #   Frame for calculated outputs
        self.root.frame_outputs = \
            ttk.LabelFrame(self.root, text='Рассчитанные параметры:',
                           labelanchor="n")
        self.root.frame_outputs.grid(column=0, row=2, padx=5, pady=5)
        self.sd_widgets()

    def sd_widgets(self):
        #   Label for SD entry
        self.root.label_sd = \
            ttk.Label(self.root.frame_outputs,
                      text='СП ЭИИМ, дБВт/Гц')
        self.root.label_sd.grid(column=0, row=0, sticky=E, padx=5,
                                  pady=(0, 10))
        #   Entry for SD
        self.root.entry_sd = \
            ttk.Entry(self.root.frame_outputs, width=10)
        self.root.entry_sd.grid(column=1, row=0, sticky=W,
                                  pady=(0, 10))

    def get_inputs(self):
        self.eirp = float(self.root.eirp.get())
        self.bandwidth = float(self.root.bandwidth.get())
        self.inputs = [self.eirp, self.bandwidth]

    def set_outputs(self, event):
        self.get_inputs()
        self.calculate(self.inputs)
        self.set_sd()

    def calculate(self, inputs):
        self.eirp, self.bandwidth = inputs[:2]
        self.sd = self.eirp - 10 * log10(self.bandwidth*10**6)
        self.sdr = round(self.sd, 2)
        return self.sdr

    def set_sd(self):
        #   Set sd
        self.root.entry_sd.delete(0, END)
        self.root.entry_sd.insert(0, self.sdr)

