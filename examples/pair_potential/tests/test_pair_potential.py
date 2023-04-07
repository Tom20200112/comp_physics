import os
import unittest

import numpy as np

from pair_potential.lj_potential import lennard_jones_potential
from pair_potential.pair_potential import pair_potential


class TestPairPotential(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.pos = np.loadtxt(f'{current_dir}/_lj13.txt')
        self.energy = -44.326801

    def test_pair_potential(self):
        v = pair_potential(self.pos, potential=lennard_jones_potential, args=(1.0, 1.0))
        self.assertAlmostEqual(v, self.energy, places=6)
