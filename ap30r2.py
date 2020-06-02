from ap3077 import AP3077
from math import log10


class AP30R2(AP3077):
    def offaxis_gain(self):
        super().offaxis_gain()
        if 0.25 < self.phi / self.phi_0 <= 1.13:
            self.g = self.gmax - 12 * (self.phi / self.phi_0) ** 2
        elif 1.13 < self.phi / self.phi_0 <= 14.7:
            self.g = self.gmax - 14 - 25 * log10(self.phi / self.phi_0)
        elif 14.7 < self.phi / self.phi_0 <= 35:
            self.g = self.gmax - 43.2
        elif 35 < self.phi / self.phi_0 <= 45.1:
            self.g = self.gmax - 85.2 + 27.2 * log10(self.phi / self.phi_0)
        elif 45.1 < self.phi / self.phi_0 <= 70:
            self.g = self.gmax - 40.2
        elif 70 < self.phi / self.phi_0 <= 80:
            self.g = self.gmax + 55.2 - 51.7 * log10(self.phi / self.phi_0)
        elif 80 * self.phi_0 < self.phi <= 180:
            self.g = self.gmax - 43.2
        elif self.phi > 180:
            self.g = '\u03C6 > 180 !'
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        if 0.44 < self.phi / self.phi_0 <= 1.28:
            self.gx = self.gmax - 20
        elif 1.28 < self.phi / self.phi_0 <= 3.22:
            self.gx = self.gmax - 17.3 - \
                      25 * log10(abs(self.phi / self.phi_0))
        elif 3.22 * self.phi_0 < self.phi <= 180:
            self.gx = self.gmax - 30
        elif self.phi > 180:
            self.gx = '\u03C6 > 180 !'
        if self.gx > self.g:
            self.gx = self.g
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p
