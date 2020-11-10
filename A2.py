from gurobipy import *

PurchaseCost = 163
MaxStore = 900
Fmax = 5
Tmax = 6
TruckCap = 60
MaxTime = 12 * 60

# Transport Costs
CDRDtoFSD = [82, 68, 84, 106, 110, 47, 44, 49, 55]
FSDtoDDP = [
    [120, 176, 154, 60, 71, 72, 57, 139, 55, 33],
    [97, 153, 130, 42, 56, 50, 44, 115, 50, 31],
    [53, 43, 47, 112, 122, 92, 129, 54, 146, 142],
    [71, 30, 51, 135, 144, 115, 152, 65, 169, 167],
    [142, 201, 177, 75, 81, 91, 65, 160, 56, 39],
    [90, 141, 122, 52, 68, 51, 60, 109, 69, 52],
    [68, 119, 99, 46, 62, 37, 59, 87, 73, 61],
    [46, 94, 75, 55, 69, 38, 72, 64, 88, 81],
    [40, 75, 61, 74, 86, 54, 91, 54, 107, 102]]

# Scenario Data
# Having a single scenario with all FSDs available is the same as
# not having scenarios in the model, without having to change it from
# assignment 1
AvailableFSD = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1]]
ScenarioProb = [1]

F = range(len(CDRDtoFSD))
Forig = [0, 1, 2, 3, 4]
D = range(len(FSDtoDDP[0]))
S = range(len(ScenarioProb))

Demands = [101, 266, 135, 272, 104, 252, 261, 107, 144, 168]

m = Model("DRDS")

# Xf[i] : tonnes transported from CDRD to FSD site i
Xf = {}
# Xft[i] : truck trips from CDRD to FSD site i
Xtf = {}
# A[i] : trucks allocated to FSD i
A = {}
# Y[i] : if FSD site i is used
Y = {}
for i in F:
    Xf[i] = m.addVar()
    Xtf[i] = m.addVar(vtype = GRB.INTEGER)
    A[i] = m.addVar(vtype = GRB.INTEGER)
    Y[i] = m.addVar(vtype = GRB.BINARY)
# Xd[(i,j,s)] : transport from FSD site i to DDP j in scenario s
Xd = {}
# Xdt[(i,j,s)] : truck trips from FSD site 1 to DDP j in scenario s
Xtd = {}
for i in F:
    for j in D:
        for s in S:
            Xd[(i,j,s)] = m.addVar()
            Xtd[(i,j,s)] = m.addVar(vtype = GRB.INTEGER)

m.setObjective(quicksum(ScenarioProb[s]*Xtd[(i,j,s)]*TruckCap*FSDtoDDP[i][j]
                    for s in S for i in F for j in D) + 
                quicksum(Xf[i]*PurchaseCost for i in F) +
                quicksum(Xtf[i]*TruckCap*CDRDtoFSD[i] for i in F) +
                quicksum(20000* A[i] for i in F), GRB.MINIMIZE)

# Constr 4, max number of FSDs
m.addConstr(quicksum(Y[i] for i in F) <= Fmax)
# Constr 5, change at most 1 FSD site
m.addConstr(quicksum(Y[i] for i in Forig) >= (Fmax - 1))
for j in D:
    for s in S:
        # Constr 1, demand
        m.addConstr(quicksum(Xd[(i,j,s)]*AvailableFSD[s][i] for i in F) >= Demands[j])
        for i in F:
            # Constr 7, trucks from FSDs to DDPs can carry all goods tranported
            m.addConstr(Xtd[(i,j,s)] * TruckCap >= Xd[(i,j,s)])

for i in F:
    for s in S:
        # Constr 2, inventory
        m.addConstr(quicksum(Xd[(i,j,s)] for j in D) <= Xf[i])
        # Constr 8, max time transporting for each truck
        m.addConstr(quicksum(3 * FSDtoDDP[i][j] * Xtd[(i,j,s)] for j in D) <= MaxTime * A[i])
    # Constr 3, max capacity and FSD must be chosen to be used
    m.addConstr(Xf[i] <= Y[i]*MaxStore)
    # Constr 6, trucks from CDRD to FSDs can carry all goods transported
    m.addConstr(Xtf[i] * TruckCap >= Xf[i])
    # Constr 9, max trucks allocated to FSD
    m.addConstr(A[i] <= Tmax)

m.optimize()

# amount transfered to each FSD
print([Xf[i].x for i in F])
# amount transfered from each FSD to each DDP in each scenario
for s in S:
    print("Scenario", s)
    for i in F:
        print(A[i].x, "Trucks allocated")
        print([Xd[(i,j,s)].x for j in D])
print("Total Costs", m.objVal)