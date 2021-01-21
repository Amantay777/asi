from tkinter import *
from math import log10, cos, radians


class CN:
    def __init__(self, root):
        self.root = root
        self.uplinkWidgets()
        self.downlinkWidgets()
        self.totalWidgets()

    def uplinkWidgets(self):
        self.uplink = ttk.LabelFrame(self.root, text='Линия вверх', labelanchor="n")
        self.uplink.grid(column=0, row=0, padx=5, pady=5, sticky='N')
        self.upInputs()
        self.upCalc()
        self.upOutputs()

    def upInputs(self):
        self.frame_inputs = ttk.LabelFrame(self.uplink, text='Входные данные:',
                                      labelanchor="n")
        self.frame_inputs.grid(column=0, row=0, padx=5, pady=5)
        iLabels = ['Мощность передатчика ЗС, Вт', 'Ширина полосы, МГц',
                   'Диаметр антенны ЗС, м',
                   'КУ антенны спутника в направлении ЗС, дБ',
                   'Шумовая температура спутника, K',
                   'Частота, МГц', 'Долгота спутника, \u00b0 в.д.',
                   'Долгота ЗС, \u00b0 в.д.',
                   'Широта ЗС, \u00b0 с.ш.']
        values = ['2','1','1.2','30','600','14250','58.5','77','50']
        self.upIEntries = []
        for i in range(9):
            label = ttk.Label(self.frame_inputs, text=iLabels[i])
            label.grid(column = 0, row = i, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_inputs, width=10)
            self.upIEntries.append(entry)
            self.upIEntries[i].grid(column=1, row=i, sticky=W)
            self.upIEntries[i].insert(0, values[i])

    def upCalc(self):
        button_calculate = ttk.Button(self.uplink, text='Рассчитать')
        button_calculate.grid(column=0, row=1)
        button_calculate.bind('<Button-1>', self.upProcess)

    def upOutputs(self):
        self.frame_outputs = ttk.LabelFrame(self.uplink, text='Рассчитанные параметры:',
                           labelanchor="n")
        self.frame_outputs.grid(column=0, row=2, padx=5, pady=5)
        oLabels = ['Отношение несущая/шум на линии вверх, дБ',
                   'КУ антенны ЗС, дБ', 'Расстояние между спутником и ЗС, км',
                   'Потери в свободном пространстве, дБ']
        self.upOEntries = []
        for i in range(4):
            label = ttk.Label(self.frame_outputs, text=oLabels[i])
            label.grid(column = 0, row = i, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_outputs, width=10)
            self.upOEntries.append(entry)
            self.upOEntries[i].grid(column=1, row=i, sticky=W)

    def upProcess(self, event):
        self.p1 = float(self.upIEntries[0].get())
        self.b = float(self.upIEntries[1].get())
        diam = float(self.upIEntries[2].get())
        self.g2 = float(self.upIEntries[3].get())
        self.ts = float(self.upIEntries[4].get())
        self.freq = float(self.upIEntries[5].get())
        self.satLong = float(self.upIEntries[6].get())
        esLong = float(self.upIEntries[7].get())
        esLat = float(self.upIEntries[8].get())

        dw = diam * self.freq * 10**6 / 299792458
        self.g1 = 20 * log10(dw) + 7.7
        self.dist = 42644 * (1 - 0.2954 * cos(radians(esLat)) *
                             cos(radians(abs(esLong - self.satLong)))) ** 0.5
        self.ls = 32.4 + 20 * log10(self.freq) + 20 * log10(self.dist)
        self.cnUp = 10*log10(self.p1) - 10*log10(self.b*10**6) + self.g1 + self.g2 - \
                  10*log10(1.38*10**-23) - 10*log10(self.ts) - self.ls

        cnr = round(self.cnUp, 2)
        g1r = round(self.g1, 2)
        distr = round(self.dist)
        lsr = round(self.ls, 2)

        self.upOEntries[0].delete(0, END)
        self.upOEntries[0].insert(0, cnr)
        self.upOEntries[1].delete(0, END)
        self.upOEntries[1].insert(0, g1r)
        self.upOEntries[2].delete(0, END)
        self.upOEntries[2].insert(0, distr)
        self.upOEntries[3].delete(0, END)
        self.upOEntries[3].insert(0, lsr)

    def downlinkWidgets(self):
        self.downlink = ttk.LabelFrame(self.root, text='Линия вниз', labelanchor="n")
        self.downlink.grid(column=1, row=0, padx=5, pady=5, sticky='N')
        self.downInputs()
        self.downCalc()
        self.downOutputs()

    def downInputs(self):
        self.frame_inputs = ttk.LabelFrame(self.downlink, text='Входные данные:',
                                    labelanchor="n")
        self.frame_inputs.grid(column=0, row=0, padx=5, pady=5)
        iLabels = ['ЭИИМ несущей спутника, дБВт', 'Ширина полосы, МГц',
                   'Диаметр антенны ЗС, м', 'Шумовая температура ЗС, K',
                   'Частота, МГц', 'Долгота спутника, \u00b0 в.д.',
                   'Долгота ЗС, \u00b0 в.д.', 'Широта ЗС, \u00b0 с.ш.']
        values = ['51.14', '1', '1.2', '200', '11200', '58.5', '77', '50']
        self.eirpValues = ['130', '30', '51.14']
        self.downIEntries = []
        for i in range(8):
            label = ttk.Label(self.frame_inputs, text=iLabels[i])
            label.grid(column=0, row=i, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_inputs, width=10)
            self.downIEntries.append(entry)
            self.downIEntries[i].grid(column=1, row=i, sticky=W)
            self.downIEntries[i].insert(0, values[i])

        eirpButton = ttk.Button(self.frame_inputs, text='Рассчитать')
        eirpButton.grid(column=2, row=0, sticky=W, padx=5)
        eirpButton.bind('<Button-1>', self.eirpWindow)

    def eirpWindow(self, event):  # eirp calculation window
        eirpwin = Toplevel(self.root)
        eirpwin.title('ЭИИМ')
        eirpwin.geometry('370x70-570+100')
        self.eirpEntries = []
        eirpLabels = ['Мощность передатчика на несущую спутника, Вт',
                      'КУ антенны спутника в направлении ЗС, дБi',
                      'ЭИИМ несущей спутника, дБВт']
        for i in range(3):
            label = ttk.Label(eirpwin, text=eirpLabels[i])
            label.grid(column=0, row=i, sticky=E, padx=5)
            entry = Entry(eirpwin, width=10)
            self.eirpEntries.append(entry)
            self.eirpEntries[i].grid(column=1, row=i, sticky=W)
            self.eirpEntries[i].insert(0, self.eirpValues[i])
        self.eirpEntries[0].bind('<KeyRelease>', self.eirpProcess)
        self.eirpEntries[1].bind('<KeyRelease>', self.eirpProcess)
        self.eirpEntries[2].config({'bg':'Yellow'})

    def eirpProcess(self, event):
        try:
            p1 = float(self.eirpEntries[0].get())
            g1 = float(self.eirpEntries[1].get())
            eirp = 10 * log10(p1) + g1
            self.eirpr = round(eirp, 2)

            self.eirpEntries[2].delete(0, END)
            self.eirpEntries[2].insert(0, self.eirpr)

            self.downIEntries[0].delete(0, END)
            self.downIEntries[0].insert(0, self.eirpr)

            self.eirpValues[0] = str(p1 if p1 % 1 else int(p1))
            self.eirpValues[1] = str(g1 if g1 % 1 else int(g1))
            self.eirpValues[2] = self.eirpr

        except:
            pass

    def downCalc(self):
        button_calculate = ttk.Button(self.downlink, text='Рассчитать')
        button_calculate.grid(column=0, row=1)
        button_calculate.bind('<Button-1>', self.downProcess)

    def downOutputs(self):
        self.frame_outputs = ttk.LabelFrame(self.downlink, text='Рассчитанные параметры:',
                           labelanchor="n")
        self.frame_outputs.grid(column=0, row=2, padx=5, pady=5)
        oLabels = ['Отношение несущая/шум на линии вниз, дБ',
                   'КУ антенны ЗС, дБi', 'Расстояние между спутником и ЗС, км',
                   'Потери в свободном пространстве, дБ']
        self.downOEntries = []
        for i in range(4):
            label = ttk.Label(self.frame_outputs, text=oLabels[i])
            label.grid(column = 0, row = i, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_outputs, width=10)
            self.downOEntries.append(entry)
            self.downOEntries[i].grid(column=1, row=i, sticky=W)

    def downProcess(self, event):
        self.eirp = float(self.downIEntries[0].get())
        self.b = float(self.downIEntries[1].get())
        self.diam = float(self.downIEntries[2].get())
        self.te = float(self.downIEntries[3].get())
        self.freq = float(self.downIEntries[4].get())
        satLong = float(self.downIEntries[5].get())
        self.esLong = float(self.downIEntries[6].get())
        self.esLat = float(self.downIEntries[7].get())

        dw = self.diam * self.freq * 10**6 / 299792458
        self.g2 = 20 * log10(dw) + 7.7
        dist = 42644 * (1 - 0.2954 * cos(radians(self.esLat)) *
                             cos(radians(abs(self.esLong - satLong)))) ** 0.5
        self.ls = 32.4 + 20 * log10(self.freq) + 20 * log10(dist)
        self.cnDown = self.eirp - 10*log10(self.b*10**6) + self.g2 - \
                  10*log10(1.38*10**-23) - 10*log10(self.te) - self.ls

        cnr = round(self.cnDown, 2)
        g2r = round(self.g2, 2)
        distr = round(dist)
        lsr = round(self.ls, 2)

        self.downOEntries[0].delete(0, END)
        self.downOEntries[0].insert(0, cnr)
        self.downOEntries[1].delete(0, END)
        self.downOEntries[1].insert(0, g2r)
        self.downOEntries[2].delete(0, END)
        self.downOEntries[2].insert(0, distr)
        self.downOEntries[3].delete(0, END)
        self.downOEntries[3].insert(0, lsr)

    def totalWidgets(self):
        self.total = ttk.LabelFrame(self.root, text='Суммарно (вверх+вниз)', labelanchor="n")
        self.total.grid(column=2, row=0, padx=5, pady=5, sticky='N')

        s = ttk.Style()
        s.configure('CNTR.TButton', anchor=CENTER)
        self.button_calculate = \
            ttk.Button(self.total, text='Рассчитать суммарное C/N',
                       style='CNTR.TButton')
        self.button_calculate.grid(column=0, row=0,columnspan = 2)
        self.button_calculate.bind('<Button-1>', self.totalProcess)

        self.CNTEntry = ttk.Entry(self.total, width=10)
        self.CNTEntry.grid(column=1, row=1, sticky=W)

        desc = 'Суммарное C/N, дБ'
        label = ttk.Label(self.total, text=desc)
        label.grid(column=0, row=1, sticky=E, padx=5)

    def totalProcess(self, event):
        self.cnTotal = -10 * log10(10 ** (-self.cnUp / 10) + 10 ** (-self.cnDown / 10 ))
        cnTotalr = round(self.cnTotal, 2)

        self.CNTEntry.delete(0, END)
        self.CNTEntry.insert(0, cnTotalr)
