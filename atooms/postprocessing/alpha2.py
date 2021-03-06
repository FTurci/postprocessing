# This file is part of atooms
# Copyright 2010-2018, Daniele Coslovich

"""Non-Gaussian parameter."""

import numpy

from .helpers import linear_grid
from .correlation import Correlation, gcf_offset
from .helpers import adjust_skip, setup_t_grid

__all__ = ['NonGaussianParameter']


def non_gaussian_parameter(x, y):
    if x is y:
        return 0.0
    dx2 = (x-y)**2
    dr2 = numpy.sum(dx2) / float(x.shape[0])
    dr4 = numpy.sum(numpy.sum(dx2, axis=1)**2) / float(x.shape[0])
    return 3*dr4 / (5*dr2**2) - 1


class NonGaussianParameter(Correlation):

    """Non-Gaussian parameter."""

    def __init__(self, trajectory, tgrid=None, norigins=50, nsamples=30):
        Correlation.__init__(self, trajectory, tgrid, 'alpha_2(t)', 'alpha2',
                             "non-Gaussian parameter", ['pos-unf'])
        if self.grid is None:
            self.grid = linear_grid(0.0, trajectory.total_time * 0.75, nsamples)
        self._discrete_tgrid = setup_t_grid(trajectory, self.grid)
        self.skip = adjust_skip(trajectory, norigins)

    def _compute(self):
        f = non_gaussian_parameter
        self.grid, self.value = gcf_offset(f, self._discrete_tgrid, self.skip,
                                           self.trajectory.steps, self._pos_unf)
        self.grid = [ti * self.trajectory.timestep for ti in self.grid]

    def analyze(self):
        try:
            from .helpers import ifabsmm
            self.results['t_star'], self.results['a2_star'] = ifabsmm(self.grid, self.value)[1]
        except:
            pass
