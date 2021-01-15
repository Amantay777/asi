from ap3097 import AP3097
from asi import Rec


class BO1213(AP3097):
    def add_params(self):
        self.a_p = super().add_params()
        if self.dw < 11:
            self.gmaxr = self.g1r = self.phi_mr = self.phi_rr = 'D/\u03BB < 11 !'
            self.phi_br = self.z25phi_0r = self.z44phi_0r = 'D/\u03BB < 11 !'
            self.phi_0r = self.phi_1r = self.phi_2r = self.sr = 'D/\u03BB < 11 !'
        return self.a_p

    def offaxis_gain(self):
        self.m_p = super().offaxis_gain()
        if self.dw < 11:
            [self.gr, self.gxr] = ['D/\u03BB < 11 !', 'D/\u03BB < 11 !']
        return self.m_p

    def ref_info(self, txt):
        txt = 'Эталонная диаграмма направленности приемной антенны земной ' \
              'станции для радиовещательной спутниковой службы в полосе ' \
              'частот 11,7−12,75 ГГц'
        Rec.ref_info(self, txt)
