import unittest
import Portfolio
import single_period_optimization


class TestAbsFunction(unittest.TestCase):

    p1 = new Portfolio()
    phi_trade = p1.phi_trade()
    phi_hold = p1.phi_hold()
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = p1.get_weights()


    def high_gamma(self):

        spo = single_period_optimization(r_t, w_t, 5.0, phi_trade, phi_hold)
        self.assertEqual(Portfolio.single_period_optimization(r_t, w_t, 5.0, phi_trade, phi_hold), spo)

    def low_gamma(self):

        spo = single_period_optimization(r_t, w_t, 0.1, phi_trade, phi_hold)
        self.assertEqual(Portfolio.single_period_optimization(r_t, w_t, 0.1, phi_trade, phi_hold), spo)
    
    def med_gamma(self):

        spo = single_period_optimization(r_t, w_t, 1.0, phi_trade, phi_hold)
        self.assertEqual(Portfolio.single_period_optimization(r_t, w_t, 1.0, phi_trade, phi_hold), spo)
    
