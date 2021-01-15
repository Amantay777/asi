from ap3097 import AP3097
from asi import Rec


class BO1900(AP3097):
    def offaxis_gain(self):
        if self.dw >= 32:
            super().offaxis_gain()
            if 0 <= self.phi < self.phi_0:
                self.gx = self.gmax - 17
        else:
            [self.g, self.gx] = ['D/\u03BB < 32 !', 'D/\u03BB < 32 !']
        self.gr = round(self.g, 2) if type(self.g) == float else self.g
        self.gxr = round(self.gx, 2) if type(self.gx) == float else self.gx
        self.m_p = [self.gr, self.gxr]
        return self.m_p

    def test(self):
        pass

    def ref_info(self, txt):
        txt = 'Эталонная диаграмма направленности антенны приемной земной ' \
              'станции для радиовещательной спутниковой службы в полосе ' \
              '21.4-22 ГГц в Районах 1 и 3.'
        Rec.ref_info(self, txt)