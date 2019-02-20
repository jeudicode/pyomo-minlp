# abstract1.py
from __future__ import division
from pyomo.environ import *
import numpy as np
import random


# desired intervals
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