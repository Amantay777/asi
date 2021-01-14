from tkinter import ttk, E, W, END
from math import log10, cos, radians
from cn import CN


class CI(CN):
    def upInputs(self):
        CN.upInputs(self)
        iLabels = ['p1\', Вт', 'B\', МГц', 'g1\'(\u03D5), дБ', 'g2\'(\u03D5), дБ',
                   'ESLn\', \u00b0 в.д.', 'ESLt\', \u00b0 с.ш.']
        iDescs = ['Мощность передатчика ЗС, создающей помехи',
                  'Ширина полосы помехи', 'Внеосевой КУ антенны ЗС, создающей помехи',
                  'КУ антенны спутника в напр. ЗС, созд. помехи',
                  'Долгота ЗС, создающей помехи', 'Широта ЗС, создающей помехи']
        values = ['2', '1', '25', '30', '47', '40']
        for i in range(6):
            label = ttk.Label(self.frame_inputs, text=iLabels[i])
            label.grid(column=0, row=i+9, sticky=E, padx=5)
            desc = ttk.Label(self.frame_inputs, text=iDescs[i])
            desc.grid(column=2, row=i+9, sticky=W, padx=5)
            entry = ttk.Entry(self.frame_inputs, width=10)
            self.upIEntries.append(entry)
            self.upIEntries[i+9].grid(column=1, row=i+9, sticky=W)
            self.upIEntries[i+9].insert(0, values[i])

    def upOutputs(self):
        CN.upOutputs(self)
        oLabels = ['d\', км', 'ls\', дБ', 'C/Iup, дБ', 'I/Nup, дБ', 'C/(N+I)up, дБ']
        oDescs = ['Расстояние между спутником и ЗС, создающей помехи',
                  'Потери помехи в свободном пространстве',
                  'Отношение несущая/помеха на линии вверх',
                  'Отношение помеха/шум на линии вверх',
                  'Отношение несущая/(шум+помеха) на линии вверх']
        for i in range(5):
            label = ttk.Label(self.frame_outputs, text=oLabels[i])
            label.grid(column=0, row=i+4, sticky=E, padx=5)
            desc = ttk.Label(self.frame_outputs, text=oDescs[i])
            desc.grid(column=2, row=i+4, sticky=W, padx=5)
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
        iLabels = ['p1\', Вт', 'B\', МГц', 'g1\'(\u03D5), дБ',
                   'g2\'(\u03D5), дБ', 'OL\', \u00b0 в.д.']
        iDescs = ['Мощность передатчика спутника, создающего помехи',
                  'Ширина полосы помехи',
                  'КУ антенны спутника, создающего помехи, в направлении ЗС',
                  'Внеосевой КУ антенны ЗС в напр. спутника, созд. помехи',
                  'Долгота спутника, создающего помехи']
        values = ['130', '1', '30', '25', '60']
        for i in range(5):
            label = ttk.Label(self.frame_inputs, text=iLabels[i])
            label.grid(column=0, row=i+9, sticky=E, padx=5)
            desc = ttk.Label(self.frame_inputs, text=iDescs[i])
            desc.grid(column=2, row=i+9, sticky=W, padx=5)
            entry = ttk.Entry(self.frame_inputs, width=10)
            self.downIEntries.append(entry)
            self.downIEntries[i+9].grid(column=1, row=i+9, sticky=W)
            self.downIEntries[i+9].insert(0, values[i])

    def downOutputs(self):
        CN.downOutputs(self)
        oLabels = ['d\', км', 'ls\', дБ', 'C/Idown, дБ', 'I/Ndown, дБ', 'C/(N+I)down, дБ']
        oDescs = ['Расстояние между спутником, создающим помехи, и ЗС',
                  'Потери помехи в свободном пространстве',
                  'Отношение несущая/помеха на линии вниз',
                  'Отношение помеха/шум на линии вниз',
                  'Отношение несущая/(шум+помеха) на линии вниз']
        for i in range(5):
            label = ttk.Label(self.frame_outputs, text=oLabels[i])
            label.grid(column=0, row=i+4, sticky=E, padx=5)
            desc = ttk.Label(self.frame_outputs, text=oDescs[i])
            desc.grid(column=2, row=i+4, sticky=W, padx=5)
            entry = ttk.Entry(self.frame_outputs, width=10)
            self.downOEntries.append(entry)
            self.downOEntries[i+4].grid(column=1, row=i+4, sticky=W)

    def downProcess(self, event):
        CN.downProcess(self, event)
        p1i = float(self.downIEntries[9].get())
        bi = float(self.downIEntries[10].get())
        g1i = float(self.downIEntries[11].get())
        g2i = float(self.downIEntries[12].get())
        satLongi = float(self.downIEntries[13].get())

        disti = 42644 * (1 - 0.2954 * cos(radians(self.esLat)) *
                              cos(radians(abs(self.esLong - satLongi)))) ** 0.5
        lsi = 32.4 + 20 * log10(self.freq) + 20 * log10(disti)
        C = 10 * log10(self.p1) - 10 * log10(self.b * 10 ** 6) + self.g1 + self.g2 - self.ls
        I = 10 * log10(p1i) - 10 * log10(bi * 10 ** 6) + g1i + g2i - lsi
        N =  10 * log10(1.38 * 10 ** -23) + 10 * log10(self.te)
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
        self.CITEntry.grid(column=0, row=2, sticky=W)

        desc1 = 'Рассчитать суммарные C/N и C/I'
        desc2 = 'Суммарное C/I, дБ'
        self.button_calculate.config(text=desc1)

        label = ttk.Label(self.total, text=desc2)
        label.grid(column=1, row=2, sticky=W)

    def totalProcess(self, event):
        CN.totalProcess(self, event)

        self.ciTotal = -10 * log10(10 ** (-self.CIUp / 10) + 10 ** (-self.CIDown / 10 ))
        ciTotalr = round(self.ciTotal, 2)

        self.CITEntry.delete(0, END)
        self.CITEntry.insert(0, ciTotalr)
