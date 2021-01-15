from ap8 import AP8
from asi import Rec
from math import log10, sqrt


class AP7(AP8):
    def add_params(self):
        self.a_p = super().add_params()
        if self.dw < 35:
            self.gmaxr = self.g1r = self.phi_mr = 'D/\u03BB < 35 !'
            self.phi_rr = self.phi_br = 'D/\u03BB < 35 !'
        else:
            if self.dw >= 100:
                self.g1 = -1 + 15 * log10(self.dw)
            else:
                self.g1 = -21 + 25 * log10(self.dw)
            self.g1r = round(self.g1, 2)
            self.phi_m = 20 * (self.w / self.d) * sqrt(self.gmax - self.g1)
            self.phi_mr = round(self.phi_m, 2)
            self.phi_br = self.phi_b = 36
        self.a_p[2:] = [self.gmaxr, self.g1r, self.phi_mr, self.phi_rr,
                     self.phi_br]
        return self.a_p

    def offaxis_gain(self):
        if self.dw < 35:
            self.g = 'D/\u03BB < 35 !'
        else:
            self.g = super().offaxis_gain()[0]
        if self.phi_r <= self.phi < self.phi_b:
            self.g = 29 - 25 * log10(self.phi)
        elif self.phi_b <= self.phi <= 180:
            self.g = - 10
        self.m_p = super(AP8, self).offaxis_gain()
        return self.m_p

    def test(self):
        assert self.calculate([0, 14, 0.6]) == \
               ['D/\u03BB < 35 !', 21.41, 28.02, 'D/\u03BB < 35 !',
                'D/\u03BB < 35 !', 'D/\u03BB < 35 !', 'D/\u03BB < 35 !',
                'D/\u03BB < 35 !']
        assert self.calculate([0, 14, 3]) == [50.63, 21.41, 140.1, 50.63, 31.2,
                                              0.63, 0.82, 36]
        assert self.calculate([0.3, 14, 3])[0] == 46.21
        assert self.calculate([0.7, 14, 3])[0] == 31.2
        assert self.calculate([20, 14, 3])[0] == -3.53
        assert self.calculate([100, 14, 3])[0] == -10
        assert self.calculate([200, 14, 3])[0] == '\u03C6 > 180 !'
        assert self.calculate([0, 14, 1]) == [41.09, 21.41, 46.7, 41.09, 20.73,
                                              1.93, 2.14, 36]
        assert self.calculate([1, 14, 1])[0] == 35.63
        assert self.calculate([2, 14, 1])[0] == 20.73
        assert self.calculate([20, 14, 1])[0] == -3.53
        assert self.calculate([100, 14, 1])[0] == -10
        assert self.calculate([200, 14, 1])[0] == '\u03C6 > 180 !'

    def ref_info(self, txt):
        txt = 'Используется для определения координационной зоны вокруг ' \
              'передающей или приемной земной станции, которая использует ' \
              'спектр в полосах частот между 100 МГц и 105 ГГц совместно с ' \
              'наземными службами радиосвязи или с земными станциями, ' \
              'работающими в противоположном направлении передачи'
        Rec.ref_info(self, txt)