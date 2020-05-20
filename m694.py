from ap8 import AP8
from math import log10, sqrt


class M694(AP8):
    def phir_calc(self):
        self.phi_r = 100 * self.w / self.d
        self.phi_rr = round(self.phi_r, 2)

    def phib_calc(self):
        self.phi_b = 120 * (self.w / self.d) ** 0.4
        self.phi_br = round(self.phi_b, 2)

    def offaxis_gain(self):
        if 0 <= self.phi < self.phi_m:
            self.g = self.gmax - 2.5 * 10 ** (-3) * (self.dw * self.phi) ** 2
        elif self.phi_m <= self.phi < self.phi_r:
            self.g = self.g1
        elif self.phi_r <= self.phi < self.phi_b:
            self.g = 52 - 10 * log10(self.dw) - 25 * log10(self.phi)
        elif self.phi_b <= self.phi <= 180:
            self.g = 0
        else:
            self.g = '\u03C6 > 180 !'
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        return [self.gr]

    def test(self):
        pass
