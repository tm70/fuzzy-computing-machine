# indexed from 1 for easier reading in later code
Species = [0, 0,3,8,9,11,18]
Values = [0, 9,14,18,32,39,47]
Sizes = [0, 3,5,7,9,11,13]
MaxLoad = 215

# a[i][w] = maximum value obtained using the first i species with w weight left
a = {}
for w in range(MaxLoad + 1):
    a[(0,w)] = (0,None)
for i in range(len(Species)):
    a[(i,0)] = (0,None)

for i in range(1, len(Species)):
    for w in range(1, MaxLoad + 1):
        if Sizes[i] > w:
            a[(i,w)] = (a[(i-1,w)][0],(i-1,w))
        else:
            if a[(i-1,w)][0] > a[(i,w-Sizes[i])][0] + Values[i]:
                a[(i,w)] = (a[(i-1,w)][0],(i-1,w))
            else:
                a[(i,w)] = (a[(i,w-Sizes[i])][0] + Values[i], (i,w-Sizes[i]))
            #a[(i,w)] = max(a[(i-1,w)], a[(i,w-Sizes[i])] + Values[i])

print(a[(len(Species) - 1,MaxLoad)])

count = {}
for s in Species:
    count[s] = 0
ind = (len(Species) - 1,MaxLoad)
while ind != None:
    #print(a[ind])
    # the solution has +1 of the species in the case that
    # the previous optimal soln for (i,j) is (i,j-Sizes[i])
    if a[ind][1] != None and a[ind][1][0] == ind[0]:
        count[Species[a[ind][1][0]]] = count[Species[a[ind][1][0]]] + 1
    ind = a[ind][1]

print(count)