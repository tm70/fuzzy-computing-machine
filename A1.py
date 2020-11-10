from gurobipy import *

PurchaseCost = 163

# Transport Costs
CDRDtoFSD = [82, 68, 84, 106, 110]
FSDtoDDP = [
    [120, 176, 154, 60, 71, 72, 57, 139, 55, 33],
    [97, 153, 130, 42, 56, 50, 44, 115, 50, 31],
    [53, 43, 47, 112, 122, 92, 129, 54, 146, 142],
    [71, 30, 51, 135, 144, 115, 152, 65, 169, 167],
    [142, 201, 177, 75, 81, 91, 65, 160, 56, 39]]

# Scenario Data
AvailableFSD = [
    [1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [1, 0, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [0, 1, 0, 1, 1],
    [1, 1, 0, 1, 1]]
ScenarioProb = [0.07, 0.08, 0.14, 0.17, 0.27, 0.27]

F = range(len(CDRDtoFSD))
D = range(len(FSDtoDDP[0]))
S = range(len(ScenarioProb))

Demands = [101, 266, 135, 272, 104, 252, 261, 107, 144, 168]

m = Model("DRDS")

# Xf[x] : transport from CDRD to FSD x
Xf = {}
for x in F:
    Xf[x] = m.addVar()
# Xd[(x,y,s)] : transport from FSD x to DDP y in scenario s
Xd = {}
for x in F:
    for y in D:
        for s in S:
            Xd[(x,y,s)] = m.addVar()

m.setObjective(quicksum(ScenarioProb[s]*Xd[(x,y,s)]*FSDtoDDP[x][y]
                    for s in S for x in F for y in D) + 
                quicksum(Xf[x]*(PurchaseCost + CDRDtoFSD[x]) for x in F), GRB.MINIMIZE)

for d in D:
    for s in S:
        # Const 1, demand
        m.addConstr(quicksum(Xd[(f,d,s)]*AvailableFSD[s][f] for f in F) >= Demands[d])
        # Const 4, max delivery from a single FSD
        for f in F:
            m.addConstr(Xd[(f,d,s)] <= 0.5*Demands[d])
for f in F:
    # Const 2, inventory
    for s in S:
        m.addConstr(quicksum(Xd[(f,d,s)] for d in D) <= Xf[f])
    # Const 3, max capacity
    m.addConstr(Xf[f] <= 900)
for s in S:
    # Const 5, in any scenario, remaining FSDs must be able to meet demand
    m.addConstr(quicksum(Xf[f]*AvailableFSD[s][f] for f in F) >=
                quicksum(Demands[d] for d in D))

m.optimize()

# amount transfered to each FSD
print([Xf[x].x for x in F])
# amount transfered from each FSD to each DDP in each scenario
for s in S:
    print("Scenario", s)
    for f in F:
        print([Xd[(f,d,s)].x for d in D])
print("Total Costs", m.objVal)