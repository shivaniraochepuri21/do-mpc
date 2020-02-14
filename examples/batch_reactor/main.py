#
#   This file is part of do-mpc
#
#   do-mpc: An environment for the easy, modular and efficient implementation of
#        robust nonlinear model predictive control
#
#   Copyright (c) 2014-2019 Sergio Lucia, Alexandru Tatulea-Codrean
#                        TU Dortmund. All rights reserved
#
#   do-mpc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#
#   do-mpc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with do-mpc.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
from casadi import *
from casadi.tools import *
import pdb
import sys
sys.path.append('../../')
import do_mpc
import scipy.io as sio
import matplotlib.pyplot as plt


from template_model import template_model
from template_optimizer import template_optimizer
from template_simulator import template_simulator

X_s_0 = 1.0 # This is the initial concentration inside the tank [mol/l]
S_s_0 = 0.5 # This is the controlled variable [mol/l]
P_s_0 = 0.0 #[C]
V_s_0 = 120.0 #[C]
x0 = np.array([X_s_0, S_s_0, P_s_0, V_s_0]).reshape(-1,1)

model = template_model()
optimizer = template_optimizer(model)
simulator = template_simulator(model)
estimator = do_mpc.estimator.state_feedback(model)

optimizer._x0 = x0
simulator._x0 = x0
estimator._x0 = x0

configuration = do_mpc.configuration(simulator, optimizer, estimator)

for k in range(150):
    configuration.make_step_optimizer()
    configuration.make_step_simulator()
    configuration.make_step_estimator()

_x = simulator.data._x
_u = simulator.data._u
_t = simulator.data._time

for i in range(_x.shape[1]):
    plt.figure()
    plt.plot(_t, _x[:,i])

for i in range(_u.shape[1]):
    plt.figure()
    plt.plot(_t[0:-1], _u[:,i])