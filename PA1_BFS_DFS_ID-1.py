"""
@author : Ganesh Nagaraj & Siddharth Jayasanakar
"""
#Graph Input file name is to be changed here. This program assumes the filename would be graph.csv
graphFile='graph.csv'
import sys
from collections import defaultdict

def loadGraph(graphFile):
    """
    load graph function loads a comma separated file as a dictionary of list of dictionaries.
    if there is a veritex a,b and there is an edge e from a to b with unit distance, the graph is represented as
    {a:[{b:1}]}. This program assumes there is only one entry from A to B, generates B to A Distance.
    This expects the input as a,b,1
    """
    graph=defaultdict(list)
    file=open(graphFile,'r')
    for line in file.readlines():
        node=line.rstrip().split(',')
        graph[node[0]].append({node[1]:int(node[2])})
        #Comment the following line if the a->b and b->a has two entries in the CSV.
        graph[node[1]].append({node[0]:int(node[2])})
        
    return graph

def queuePop(queue,popIndex,bd):
    """
    Queue pop function takes a queue, index at which element has to be popped and a boolean bd.
    The boolean bd is used to resolve the location of the pop, if True first element is popped, representing a BFS.
    If bd is false, the queue acts like a stack and initiates a DFS.
    """
    if bd:
        return queue.pop(popIndex)
    else:
        return queue.pop()

def goalCheck(visited,destination):
    """
    goalCheck function takes a list of tuples representing (destination,source) and checks if the goal is reached.
    This function returns a boolen True if goal is reached, False if its not reached.
    """
    visitedList=[k for (k,v) in visited]
    if destination in visitedList:
        return True
    else:
        return False

def resolveDistance(graph,visited):
    """
    resolveDistance function takes the graph (returned by function loadGraph) as input and
    computes the distance of a node from source.
    """
    path=[]
    visitedDict=defaultdict(type(visited[0][0]))
    #Create a dictionary to link the path of the source to destination tree
    for (k,v) in visited:
        visitedDict[k]=v
    currNode=visited[len(visited)-1][0]
    #Back track the dictionary till the source node is reached
    while currNode is not visited[0][0]:
        path.append(currNode)
        currNode=visitedDict[currNode]
    path.append(visited[0][0])
    #Flip the path vector to see the path from source to destination
    path.reverse()
    distance=0
    #For the path, lookup the graph and calculate the distance.
    for index in range(0,len(path)-1):
        for element in graph[path[index]]:
            if list(element.keys())[0]==path[index+1]:
                distance+=element[path[index+1]]
    return (path,distance)

def resolveLevel(graph,visited,source,destination):
    """
    resolveLevel calculates the level of the given node(destination) from source.
    This backtracks the path from destination to source and counts the no.of level and returns the level.
    """
    path=[]
    visitedDict=defaultdict(type(source))
    for (k,v) in visited:
        visitedDict[k]=v
    currNode=destination
    while currNode is not source:
        path.append(currNode)
        currNode=visitedDict[currNode]
    return len(path)

def bfs(source,destination,graph,bd,iterlength=-1):
    """
    This is the main workhorse of the search package. Source and destination needs to be nodes in the graph.
    Boolean bd refers to BFS if True, else DFS.
    iterlength is the deepening level. Default -1 indicates that there is no fix on the DFS length,
    however any positive number enforces an limit on the level of iterative deepening
    """
    levelIncrement=iterlength
    possibleLocs=graph.keys()
    #Check if source and destination is present in the graph.
    if source not in possibleLocs:
        print("Source Not Found in Graph")
    elif destination not in possibleLocs:
        print("Destination Not Found in Graph")
    else:
        #Inorder to track the visited node and the source node, a visit includes a tuple (node,sourcenode)
        #The source of the initial node is zero
        #Eg, if we visit city a from city b then the tuple is (a,b)
        queue=[(source,0)]
        #TempQueue is used to hold entries for iterative deepening
        tempQueue=[]
        #Visited queue acts both as a stack and queue based on the queuePop function.
        #The whole queue visited is passed as an mutable object
        visited=[]
        #Loop while the entire frontier of queue is visited
        while queue:
            currNode=queuePop(queue,0,bd) #Pop a node based on BFS or DFS
            visited.append(currNode) #Add current node to queue
            checkGoal=goalCheck(visited,destination) #Check for Goalstate
            if not checkGoal:
                for element in graph[currNode[0]]:
                    for node in element:
                        #Check if the node is in visited and not in queue (to avoid revisiting)
                        if ((node not in [k for (k,v) in visited]) and (node not in [k for (k,v) in queue])):
                            #Retrieve the level of the node from the source
                            level=resolveLevel(graph,visited,source,currNode[0])
                            #Check if the running instance if BFS/DFS or level reachable within ID
                            if (iterlength < 0) or (level < iterlength) :
                                #If yes append the current node and the source node to the queue
                                queue.append((node,currNode[0]))
                            else:
                                #If no append the current node to temp queue.
                                tempQueue.append((node,currNode[0]))
                                #If queue is empty and goal state not reached,
                                #Copy the tempQueue to Queue
                                #Increase the level to search
                        if len(queue)==0 and len(tempQueue)>0 and iterlength>0:
                            queue=tempQueue[:]
                            tempQueue=[]
                            iterlength+=levelIncrement
                            print("Level Deepened",iterlength)
            else:
                #Return the distance as goal state is reached
                return resolveDistance(graph,visited)
        #Return the goal is not possible
        return("No Possible Goals")

args=sys.argv[1:]
if len(args) <= 2 :
    print("Invalid Input. Syntax : source destination BFS/DFS/ID")
    exit(0)
graph=loadGraph(graphFile)
if args[2]=="BFS" :
    print(bfs(args[0],args[1],graph,True))
elif args[2]=="DFS" :
    print(bfs(args[0],args[1],graph,False))
elif args[2]=="ID":
    depth= int(input("Enter the deepening factor : "))
    print(bfs(args[0],args[1],graph,False,depth)) #Calling ID with one level per search
else:
    print("Invalid Input. Syntax : source destination BFS/DFS/ID")
    exit(0)
