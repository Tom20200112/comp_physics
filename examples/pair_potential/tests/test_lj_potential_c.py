import os
import unittest

import numpy as np
import sys
sys.path.append('/Users/tomzhang/Documents/计算物理/examples')

from local_optimisation import bfgs
from pair_potential import lj_energy_c, lj_gradient_c


class TestLJPotentialC(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.pos = np.loadtxt(f'{current_dir}/_lj13.txt')
        self.energy = -44.32680141

    def test_lj_energy_c(self):
        self.assertAlmostEqual(lj_energy_c(self.pos.flatten()), self.energy)

    def test_lj_gradient_c(self):
        f, df = lj_energy_c, lj_gradient_c
        pos = self.pos.flatten() + np.random.randn(39) * 1e-3
        pos = bfgs(f, df, pos, xtol=1e-8, gtol=1e-5)
        np.testing.assert_array_almost_equal(df(pos), 0.0, decimal=5)
