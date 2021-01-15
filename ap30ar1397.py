from ap30ar13 import AP30AR13
from math import log10
from asi import Rec


class AP30AR1397(AP30AR13):
    def offaxis_gain(self):
        super().offaxis_gain()
        if 0.32 < self.phi <= 0.54:
            self.g = self.gmax - 5.7 - 53.2 * self.phi ** 2
        elif 0.54 < self.phi <= 36.31:
            self.g = self.gmax - 28 - 25 * log10(self.phi)
        elif 36.31 < self.phi <= 180:
            self.g = self.gmax - 67
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        if self.phi <= 180:
            self.gx = self.gmax - 35
        if self.gx > self.g:
            self.gx = self.g
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p

    def ref_info(self, txt):
        txt = 'Эталонная диаграмма направленности антенны передающей земной ' \
              'станции для Районов 1 и 3 (ВКР-97).'
        Rec.ref_info(self, txt)