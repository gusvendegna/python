# Written by August Vendegna


import networkx as nx
import sys
#import time
#import matplotlib.pyplot as pp


inputFile = open(sys.argv[1])


firstLine = inputFile.readline().split(' ')
numVillages = int(firstLine[0])
numTransitLines = int(firstLine[1])
startVillage = (firstLine[2], firstLine[2], None, None)
endVillage = (firstLine[3][:-1], firstLine[3][:-1], None, None)  # remove the newline
# FIRST LINE DONE
# array for storing maze data
edgeArray = set()
edgeDict = {}
G = nx.DiGraph() # must be directional in this implementation!!


#t0 = time.time()


edgeArray.add(endVillage) # must be here for some reason?
edgeArray.add(startVillage) # must be here for some reason?
G.add_node(startVillage)
G.add_node(endVillage)


# make edges based on which first two is not different and if there is a correct one




edgeDict[startVillage[0]] = []
edgeDict[startVillage[0]].append(startVillage)
edgeDict[endVillage[0]] = []
edgeDict[endVillage[0]].append(endVillage)




with inputFile:
    while True:
        curLine = inputFile.readline()
        if not curLine:
            break
        curLine = curLine.split(' ')


        # we want both directions!!
        curEdge = (curLine[0], curLine[1], curLine[2], curLine[3].strip())
        altEdge = (curLine[1], curLine[0], curLine[2], curLine[3].strip())
        edgeArray.add(curEdge)
        edgeArray.add(altEdge)
        if startVillage[0] == curEdge[0]:
            G.add_edge(startVillage, curEdge, weight=sum(ord(i) for i in curEdge[1]))
        elif startVillage[0] == altEdge[0]:
            G.add_edge(startVillage, altEdge, weight=sum(ord(i) for i in curEdge[1]))  
   
        if endVillage[0] == curEdge[1]:
            G.add_edge(curEdge, endVillage, weight=sum(ord(i) for i in curEdge[1]))
        elif endVillage[0] == altEdge[0]:
            G.add_edge(altEdge, endVillage, weight=sum(ord(i) for i in curEdge[1]))




        if curEdge[0] not in edgeDict:
            edgeDict[curEdge[0]] = []
        edgeDict[curEdge[0]].append(curEdge)


        if altEdge[0] not in edgeDict:
            edgeDict[altEdge[0]] = []
        edgeDict[altEdge[0]].append(altEdge)
       
 
#print("added all")
# all edges loaded into edgeArray - which is actually a set now but 'eff em'




for curEdge in edgeArray:
    altEdge = (curEdge[1], curEdge[0], curEdge[2], curEdge[3])
    if curEdge[1] not in edgeDict:
        continue
    for compEdge in edgeDict[curEdge[1]]:
        #print(compEdge)
        edgeCost = ord(curEdge[1][0])
        if compEdge == altEdge or compEdge == curEdge:
            continue
        if compEdge == endVillage:
            if curEdge[1] == compEdge[0]:
                G.add_edge(curEdge, compEdge, weight=edgeCost)
                continue
        if (curEdge[2] == compEdge[2] or curEdge[3] == compEdge[3]) and curEdge[1] == compEdge[0]:
            G.add_edge(curEdge, compEdge, weight=edgeCost)


#print("done adding edges")
# for i in G.neighbors(('DD', 'Bm', 'R', 'H')):
#     print(i)
failed = False
     


allPaths = nx.all_shortest_paths(G, startVillage, endVillage, method='dijkstra', weight = 'weight')


if nx.has_path(G, startVillage, endVillage) == False:
    failed = True
    print('NO PATH')
if failed == False:
    paths = []
    for path in allPaths:
        output = ''
        for i in range(len(path)-1):
            output += path[i][1]
            if i < len(path)-2:
                output+= ' '
        paths.append(output)
    print(sorted(paths)[0])




#print(time.time()-t0
