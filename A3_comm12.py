from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

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

lostProb = 0.2

Order = [1,7,6,5,3,2,0,8,4]

# t = month (start from 1 to guarentee site 1 is restored)
# s = set of destroyed sites
def V(t,s):
    #print(t,s)
    # end case: all sites restored or lost
    if (t + len(s) >= len(Order)):
        saved = set()
        for site in Order:
            if site not in s:
                saved = saved|Species[site]
        return len(saved)
    
    # what is the next fragile site
    i = 0
    for f in range(t):
        while Order[i] in s:
            i += 1
        i += 1
    #print(i)
    
    # what are the remaining fragile states
    remaining = Order[i:]
    for site in s:
        if site in remaining:
            remaining.remove(site)
    
    # calculate value
    v = 0
    for rs in powerset(remaining):
        destroyed = set()|s
        destroyed.update(rs)
        prob = ((1-lostProb)**(len(remaining)-len(rs)))*(lostProb**len(rs))
        #print(rs)
        #print(destroyed)
        #print(prob)
        v += prob*V(t+1,destroyed)
    
    return v

print(V(1,set()))