from pyomo.environ import ConcreteModel, Var, Objective, Constraint, NonNegativeReals, minimize, SolverFactory
import matplotlib.pyplot as plt

# Data / Parameters
load = [99,93, 88, 87, 87, 88, 109, 127, 140, 142, 142, 140, 140, 140, 137, 139, 146, 148, 148, 142, 134, 123, 108, 93] #demanded in kWh pour chaque heure
lf_pv = [0.00E+00, 0.00E+00, 0.00E+00, 0.00E+00, 9.80E-04, 2.47E-02, 9.51E-02, 1.50E-01, 2.29E-01, 2.98E-01, 3.52E-01, 4.15E-01, 4.58E-01, 3.73E-01, 2.60E-01, 2.19E-01, 1.99E-01, 8.80E-02, 7.03E-02, 3.90E-02, 9.92E-03, 1.39E-06, 0.00E+00, 0.00E+00] #load factor of the PV for each hour, between 0 and 1
timestep = len(load) #number of hours
c_pv = 2500 #€/kW   cost for power
c_batt = 1000 #€/kWh    cost for size
eff_batt_in = 0.95  #efficiency of the battery
eff_batt_out = 0.95 #efficiency of the battery
chargetime = 4  # hours to charge fully the battery -> link between power and energy
#goal : minimize the cost of the system


# Model
model = ConcreteModel()

# Define model variables
model.P_pv_inst = Var(domain=NonNegativeReals)
model.SOC_max = Var(domain=NonNegativeReals)
model.P_pv_prod = Var(range(timestep), domain=NonNegativeReals)
model.P_batt_in = Var(range(timestep), domain=NonNegativeReals)
model.P_batt_out = Var(range(timestep), domain=NonNegativeReals)
model.SOC_time = Var(range(timestep), domain=NonNegativeReals)

print(model.P_batt_in)

# Define the constraints
def P_pv_production_rule(model, t):
    return model.P_pv_prod[t] == model.P_pv_inst * lf_pv[t]
model.P_pv_production_constraint = Constraint(range(timestep), rule=P_pv_production_rule)

def battery_soc_rule(model, t):
    if t == 0:
        return model.SOC_time[t] == model.SOC_max
    return model.SOC_time[t] == model.SOC_time[t-1] + eff_batt_in*model.P_batt_in[t-1]*1 - (1/eff_batt_out)*model.P_batt_out[t-1]*1
model.battery_soc_constraint = Constraint(range(timestep), rule=battery_soc_rule)

def battery_capacity_rule(model, t):
    return model.SOC_time[t] <= model.SOC_max
model.battery_capacity_constraint = Constraint(range(timestep), rule=battery_capacity_rule)

def load_balance_rule(model, t):
    return load[t] == model.P_pv_prod[t] + model.P_batt_out[t] - model.P_batt_in[t]
model.load_balance_constraint = Constraint(range(timestep), rule=load_balance_rule)

def charge_in_max_rule(model, t):
    return model.P_batt_in[t] <= model.SOC_max/chargetime
model.charge_in_max_constraint = Constraint(range(timestep), rule=charge_in_max_rule)

def charge_out_max_rule(model, t):
    return model.P_batt_out[t] <= model.SOC_max/chargetime
model.charge_out_max_constraint = Constraint(range(timestep), rule=charge_out_max_rule)


# Define the objective function
def objective_rule(model):
    return c_pv*model.P_pv_inst + c_batt*model.SOC_max
model.objective = Objective(rule=objective_rule, sense=minimize)

# Solve the model
solver = SolverFactory('gurobi')
solver.solve(model)

results = solver.solve(model)
print(f"Optimal PV size: {model.P_pv_inst():.2f} kW")
print(f"Optimal battery capacity: {model.SOC_max():.2f} kWh")


plt.figure(figsize=(10, 6))
plt.plot(load, label='Load (kWh)')
plt.plot([model.P_pv_prod[t]() for t in range(timestep)], label='PV Production (kWh)')
plt.plot([model.SOC_time[t]() for t in range(timestep)], label='Battery SOC_time (kWh)')
plt.xlabel('Time (hours)')
plt.ylabel('Energy (kWh)')
plt.legend()
plt.title('Energy Management')
plt.show()