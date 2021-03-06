from itertools import combinations

Sites = range(9)
Species = [
    {0,13,15},
    {0,3,8,9,11,18},
    {1,3,13,17},
    {10,12,16,19},
    {0,8},
    {1,5,14,17},
    {2,6,7,18},
    {1,2,4,13},
    {14,18}
    ]
Adjacent = [
    [4],
    [2,5],
    [1,3,6],
    [2,7],
    [0],
    [1,6],
    [2,5,7,8],
    [3,6],
    [6]
    ]
BaseLossProb = 0.2
IncLossProb = 0.05

#Order = [1,7,6,5,3,2,0,8,4]

# The state is a 9-tuple where each element is
# -1 = lost, 0 = fragile, 1 = restored
# GenerateOutcomes returns a list of tuples with a probability
# in position 0 and a state as a tuple in position 1
def GenerateOutcomes(State, LossProb):
    ans = []
    tempSites = [j for j in Sites if State[j]==0]
    n = len(tempSites)
    for i in range(n+1):
        for tlist in combinations(tempSites, i):
            p = 1.0
            slist = list(State)
            for j in range(n):
                if tempSites[j] in tlist:
                    p *= LossProb[tempSites[j]]
                    slist[tempSites[j]] = -1
                else:
                    p *= 1-LossProb[tempSites[j]]
            ans.append((p, tuple(slist)))
    return ans

# vals[state] = (p,a) where
# p = probability of saving all important species from this state
# a = optimal action to save all important species
vals = {}

def V(state, lossprob):
    if vals.get(state) != None:
        return vals.get(state)
    
    # end case: all sites lost or restored
    if 0 not in state:
        saved = set()
        for s in Sites:
            if state[s] == 1:
                saved = saved|Species[s]
        vals[state] = (len(saved),-1)
        return (len(saved),-1)
    
    mv = 0
    ac = -1
    for s in Sites:
        if state[s] != 0:
            continue
        
        newstate = [i for i in state]
        newstate[s] = 1
        newstate = tuple(newstate)
    
        # calculate value
        v = 0
        nextstates = GenerateOutcomes(newstate, lossprob)
        for st in nextstates:
            newlossprob = getLossProb(st[1])
            v += st[0] * V(st[1],newlossprob)[0]
        
        if (mv <= v):
            mv = v
            ac = s
    
    vals[state] = (mv, ac)
    return (mv,ac)

def getLossProb(state):
    lossprob = [BaseLossProb for j in Sites]
    for i in Sites:
        if state[i] == -1:
            for j in Adjacent[i]:
                lossprob[j] = lossprob[j] + IncLossProb
    return lossprob

print(V((0,0,0,0,0,0,0,0,0),[BaseLossProb for j in Sites]))
'''
print(V((0,0,0,1,0,0,0,0,0),[BaseLossProb for j in Sites]))
print(V((0,1,0,1,0,0,0,0,0),[BaseLossProb for j in Sites]))
print(V((0,-1,0,1,0,0,0,0,0),[BaseLossProb for j in Sites]))
print(V((0,1,0,1,0,0,1,0,0),[BaseLossProb for j in Sites]))
print(V((0,-1,0,1,0,0,-1,0,0),[BaseLossProb for j in Sites]))
'''
    
for s in GenerateOutcomes((0,0,0,1,0,0,0,0,0),[BaseLossProb for j in Sites]):
    if s[1][1] != -1:
        continue
    #if vals[s[1]][1] != 6:
    #    print("---", s[1])
    print(vals[s[1]])