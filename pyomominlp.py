from pyomo.environ import *
import numpy as np
import random

################# problem definition #################
#   min sum ((a_i * x_i^2 + b_i * x_i) * m_i) 
#   s.t. a_i ** 2 - 1 >= 0
#   a_i in {-1, 1}
#   b_i in R
#
######################################################

# desired intervals

# We will divide [0,1] in P sections. Then, midpoints for each section will be calculated

p = 2 # P
interval = np.arange(p, dtype=np.float)
midpoint = np.arange(p, dtype=np.float)

# split [0,1] in P parts

delta = 1 / p

# setting intervals and midpoints

interval[0] = delta
midpoint[0] = delta * 0.5


for i in range(1,p):
  interval[i] = interval[i-1] + delta
  midpoint[i] = midpoint[i-1] + delta


model = ConcreteModel()

def initA (model, i) :
  if i > p:
    return Set.End
  return i

def initB (model, i) :
  if i > p:
    return Set.End
  return random.randrange(-999999, 999999)

# variables
model.I = range(p)
model.A = range(p) 
model.B = range(p)
model.a = Var(model.A, within=Integers, bounds=(-1,1))
model.b = Var(model.B, domain=Reals)

def obj_expression(model):
    return sum((model.a[i] * (midpoint[i] ** 2) + model.b[i] * midpoint[i]) * interval[i] for i in range(p))

model.OBJ = Objective(rule=obj_expression)

def ax_constraint_rule(model,i):
    # return the expression for the constraint for i
    return model.a[i] ** 2 - 1  >= 0

# the next line creates one constraint for each member of the set model.I
model.AxbConstraint = Constraint(model.I, rule=ax_constraint_rule)

# In case you need extra information from BARON
# uncomment the following lines and run normally (python pymonminlp.py)

#opt = SolverFactory('baron', executable='YOUR/PATH/TO/BARON')
#result = opt.solve(model, tee=True)