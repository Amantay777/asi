from tkinter import ttk, E, W, END
from math import log10, cos, radians
from cn import CN


class CI(CN):
    def upInputs(self):
        CN.upInputs(self)
        iLabels = ['Мощность передатчика ЗС, создающей помехи, Вт',
                   'Ширина полосы помехи, МГц',
                   'Внеосевой КУ антенны ЗС, создающей помехи, дБ',
                   'КУ антенны спутника в напр. ЗС, созд. помехи, дБ',
                   'Долгота ЗС, создающей помехи, \u00b0 в.д.',
                   'Широта ЗС, создающей помехи, \u00b0 с.ш.']
        values = ['2', '1', '25', '30', '47', '40']
        for i in range(6):
            label = ttk.Label(self.frame_inputs, text=iLabels[i])
            label.grid(column=0, row=i+9, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_inputs, width=10)
            self.upIEntries.append(entry)
            self.upIEntries[i+9].grid(column=1, row=i+9, sticky=W)
            self.upIEntries[i+9].insert(0, values[i])

    def upOutputs(self):
        CN.upOutputs(self)
        oLabels = ['Расстояние между спутником и ЗС, создающей помехи, км',
                   'Потери помехи в свободном пространстве, дБ',
                   'Отношение несущая/помеха на линии вверх, дБ',
                   'Отношение помеха/шум на линии вверх, дБ',
                   'Отношение несущая/(шум+помеха) на линии вверх, дБ']
        for i in range(5):
            label = ttk.Label(self.frame_outputs, text=oLabels[i])
            label.grid(column=0, row=i+4, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_outputs, width=10)
            self.upOEntries.append(entry)
            self.upOEntries[i+4].grid(column=1, row=i+4, sticky=W)

    def upProcess(self, event):
        CN.upProcess(self, event)
        p1i = float(self.upIEntries[9].get())
        bi = float(self.upIEntries[10].get())
        g1i = float(self.upIEntries[11].get())
        g2i = float(self.upIEntries[12].get())
        esLongi = float(self.upIEntries[13].get())
        esLati = float(self.upIEntries[14].get())

        disti = 42644 * (1 - 0.2954 * cos(radians(esLati)) *
                              cos(radians(abs(esLongi - self.satLong)))) ** 0.5
        lsi = 32.4 + 20 * log10(self.freq) + 20 * log10(disti)
        C = 10 * log10(self.p1) - 10 * log10(self.b * 10 ** 6) + self.g1 + self.g2 - self.ls
        I = 10 * log10(p1i) - 10 * log10(bi * 10 ** 6) + g1i + g2i - lsi
        N =  10*log10(1.38*10**-23) + 10*log10(self.ts)
        NpI = 10*log10(10**(N/10) + 10**(I/10))
        self.CIUp = C - I
        self.INUp = I - N
        self.CNIUp = C - NpI

        cir = round(self.CIUp, 2)
        distir = round(disti)
        lsir = round(lsi, 2)
        inr = round(self.INUp, 2)
        cnir = round(self.CNIUp, 2)
        outputs = [distir,lsir,cir,inr,cnir]
        for i in range(4,9):
            self.upOEntries[i].delete(0, END)
            self.upOEntries[i].insert(0,outputs[i-4])

    def downInputs(self):
        CN.downInputs(self)
        iLabels = ['Мощность передатчика спутника, создающего помехи, Вт',
                   'КУ антенны спутника, создающего помехи, в направлении ЗС, дБ',
                   'Ширина полосы помехи, МГц',
                   'Внеосевой КУ антенны ЗС в напр. спутника, созд. помехи, дБ',
                   'Долгота спутника, создающего помехи, \u00b0 в.д.']
        values = ['130', '30', '1', '25', '60']
        for i in range(5):
            label = ttk.Label(self.frame_inputs, text=iLabels[i])
            label.grid(column=0, row=i+8, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_inputs, width=10)
            self.downIEntries.append(entry)
            self.downIEntries[i+8].grid(column=1, row=i+8, sticky=W)
            self.downIEntries[i+8].insert(0, values[i])

    def downOutputs(self):
        CN.downOutputs(self)
        oLabels = ['Расстояние между спутником, создающим помехи, и ЗС, км',
                   'Потери помехи в свободном пространстве, дБ',
                   'Отношение несущая/помеха на линии вниз, дБ',
                   'Отношение помеха/шум на линии вниз, дБ',
                   'Отношение несущая/(шум+помеха) на линии вниз, дБ']
        for i in range(5):
            label = ttk.Label(self.frame_outputs, text=oLabels[i])
            label.grid(column=0, row=i+4, sticky=E, padx=5)
            entry = ttk.Entry(self.frame_outputs, width=10)
            self.downOEntries.append(entry)
            self.downOEntries[i+4].grid(column=1, row=i+4, sticky=W)

    def downProcess(self, event):
        CN.downProcess(self, event)
        p1i = float(self.downIEntries[8].get())
        g1i = float(self.downIEntries[9].get())
        bi = float(self.downIEntries[10].get())
        g2i = float(self.downIEntries[11].get())
        satLongi = float(self.downIEntries[12].get())

        disti = 42644 * (1 - 0.2954 * cos(radians(self.esLat)) *
                              cos(radians(abs(self.esLong - satLongi)))) ** 0.5
        lsi = 32.4 + 20 * log10(self.freq) + 20 * log10(disti)
        C = self.eirp - 10 * log10(self.b * 10 ** 6) + self.g2 - self.ls
        I = 10 * log10(p1i) + g1i - 10 * log10(bi * 10 ** 6) + g2i - lsi
        N = 10 * log10(1.38 * 10 ** -23) + 10 * log10(self.te)
        NpI = 10*log10(10**(N/10) + 10**(I/10))
        self.CIDown = C - I
        self.INDown = I - N
        self.CNIDown = C - NpI

        cir = round(self.CIDown, 2)
        distir = round(disti)
        lsir = round(lsi, 2)
        inr = round(self.INDown, 2)
        cnir = round(self.CNIDown, 2)

        outputs = [distir, lsir, cir, inr, cnir]
        for i in range(4, 9):
            self.downOEntries[i].delete(0, END)
            self.downOEntries[i].insert(0, outputs[i - 4])

    def totalWidgets(self):
        CN.totalWidgets(self)

        self.CITEntry = ttk.Entry(self.total, width=10)
        self.CITEntry.grid(column=1, row=2, sticky=W)

        self.INTEntry = ttk.Entry(self.total, width=10)
        self.INTEntry.grid(column=1, row=3, sticky=W)

        self.CNITEntry = ttk.Entry(self.total, width=10)
        self.CNITEntry.grid(column=1, row=4, sticky=W)

        desc1 = 'Рассчитать суммарные \n C/N, C/I, I/N и C/N+I'
        self.button_calculate.config(text=desc1)

        desc2 = 'Суммарное C/I, дБ'
        label = ttk.Label(self.total, text=desc2)
        label.grid(column=0, row=2, sticky=E, padx=5)

        desc3 = 'Суммарное I/N, дБ'
        label = ttk.Label(self.total, text=desc3)
        label.grid(column=0, row=3, sticky=E, padx=5)

        desc4 = 'Суммарное C/N+I, дБ'
        label = ttk.Label(self.total, text=desc4)
        label.grid(column=0, row=4, sticky=E, padx=5)

    def totalProcess(self, event):
        CN.totalProcess(self, event)

        self.ciTotal = -10 * log10(10 ** (-self.CIUp / 10) + 10 ** (-self.CIDown / 10 ))
        ciTotalr = round(self.ciTotal, 2)

        self.inTotal = -10 * log10(
            10 ** (-self.INUp / 10) + 10 ** (-self.INDown / 10))
        inTotalr = round(self.inTotal, 2)

        self.cniTotal = -10 * log10(
            10 ** (-self.CNIUp / 10) + 10 ** (-self.CNIDown / 10))
        cniTotalr = round(self.cniTotal, 2)

        self.CITEntry.delete(0, END)
        self.CITEntry.insert(0, ciTotalr)

        self.INTEntry.delete(0, END)
        self.INTEntry.insert(0, inTotalr)

        self.CNITEntry.delete(0, END)
        self.CNITEntry.insert(0, cniTotalr)
