from pyomo.environ import ConcreteModel, Var, Objective, Constraint, NonNegativeReals, minimize, SolverFactory
import matplotlib.pyplot as plt

# Data / Parameters
load = [99,93, 88, 87, 87, 88, 109, 127, 140, 142, 142, 140, 140, 140, 137, 139, 146, 148, 148, 142, 134, 123, 108, 93]
lf_pv = [0.00E+00, 0.00E+00, 0.00E+00, 0.00E+00, 9.80E-04, 2.47E-02, 9.51E-02, 1.50E-01, 2.29E-01, 2.98E-01, 3.52E-01, 4.15E-01, 4.58E-01, 3.73E-01, 2.60E-01, 2.19E-01, 1.99E-01, 8.80E-02, 7.03E-02, 3.90E-02, 9.92E-03, 1.39E-06, 0.00E+00, 0.00E+00]
timestep = len(load)
c_pv = 2500
c_batt = 1000
eff_batt_in = 0.95
eff_batt_out = 0.95
chargetime = 4  # hours to charge fully the battery

# Model
model = ConcreteModel()

# Define model variables
##########################################
############ CODE TO ADD HERE ############
##########################################

# Define the constraints
##########################################
############ CODE TO ADD HERE ############
##########################################

# Define the objective functions
##########################################
############ CODE TO ADD HERE ############
##########################################


# Specify the path towards your solver (gurobi) file
solver = SolverFactory(gurobi)
solver.solve(model)

# Results - Print the optimal PV size and optimal battery capacity
##########################################
############ CODE TO ADD HERE ############
##########################################


# Plotting - Generate a graph showing the evolution of (i) the load, 
# (ii) the PV production and, (iii) the soc of the battery
##########################################
############ CODE TO ADD HERE ############
##########################################