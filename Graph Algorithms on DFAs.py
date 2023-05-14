import queue
import random


class DFA:

    #Initialising DFA
    def __init__(self, size):
        self.size=size
        self.states = []
        self.i_state = 0
        self.f_states = []
        self.trans = {}
        self.time = 0

        #Creating states using numerical format
        for x in range(0,self.size):
            self.states.append(x)

        #Creating final states
        for x in range(0, self.size):
            check = random.randint(0,1)
            if(check==0):
                self.f_states.append(x)
            else:
                continue

        #Creating transitions
        for x in range(0,self.size):
            checkA = random.randint(0,self.size-1)
            checkB = random.randint(0,self.size-1)
            self.trans[x]=[checkA,checkB]

        #Choosing start state
        self.i_state = random.randint(0,self.size-1)

    #Variation of the breadth first search algorithm
    def search(self):

        #Creating a queue and visited list for the BFS
        visit=[]
        queue=[]
        #Cost list is used to find the depth of the dfa
        cost=[]

        #Appending the initial state
        visit.append(self.i_state)
        queue.append(self.i_state)

        while queue:
            s=queue.pop(0)
            #print(s)

            #Check the transitions of the current state
            for next_state in self.trans[s]:
                #If the next state not visited append in queue and visited list
                if next_state not in visit:

                    visit.append(next_state)
                    queue.append(next_state)
                    #Add value s and increment 
                    if(next_state not in cost):
                        cost.append(next_state)

                    temp = cost.index(next_state)
                    cost[temp]=s+1
    
        return cost

    #Finding the maximum depth of the dfa by using the cost list
    def depth(self, cost):

        maxs=0
    
        #Find the largest value in the cost list
        for x in range(0, len(cost)):
            if(maxs<cost[x]):
                temp=x
                #Check if the largest state is a final state, if not use another value
                for y in range(0,len(self.f_states)):
                    if(temp==self.f_states[y]):
                        maxs=cost[x]

        return maxs

    #Later on this was not used since islands can be strongly connected components and it sometimes interfered when building the transitions of M
    def removeNodes(self):

        #Creating a queue and visited list for the BFS
        visit=[]
        queue=[]

        #Appending the initial state
        visit.append(self.i_state)
        queue.append(self.i_state)

        while queue:
            s=queue.pop(0)
            #print(s)

            #Check the transitions of the current state
            for next_state in self.trans[s]:
                #If the next state not visited append in queue and visited list
                if next_state not in visit:

                    visit.append(next_state)
                    queue.append(next_state)
                    #Add value s and increment 
                    
        for x in self.states:
            if(x not in visit):

                self.size-=1
                self.states.remove(x)
                del self.trans[x]

                if(x in self.f_states):
                    self.f_states.remove(x)

    #Using hopcroft minimization 
    def hopcroft(self):

        #self.removeNodes()

        #Seperating states into final and non-final
        final=self.f_states
        non_final=[]
 
        #Adding the non final states into a list
        for x in range(len(self.states)):
            flag=False
            for y in range(len(final)):
                if(self.states[x]==final[y]):
                    flag=True
                    break
                else:
                    continue
            if(flag==False):
                non_final.append(self.states[x])
                flag=True
 
        set1=[final,non_final]
        set2=[]
 
        #Looping until set1 and set2 have the same length meaning that all values have been inputted
        while(len(set1))!=len((set2)):
 
            if(len(set2)!=0):
                set1=set2.copy()
                set2=[]
 
            #Iterating through the set
            for x in set1:
 
                set3=[]#If state transitions lead to the same set, these will be appended here
                set4=[]#If state transitions do not lead to the same set, these will be appended here
 
            #Iterating set elements in set1
                for y in x:
                    if(self.trans[y][0] in x and self.trans[y][1] in x):
                        set3.append(y)
                    else:
                       set4.append(y)
 
                # adding the sets
                if(len(set3)!=0):
                    set2.append(set3)
                if(len(set4) == 1):
                    set2.append(set4)
                    #If the values which point to a different set is larger than 1, we have to check if these values all point to the same state, if not they must also be seperated.
                elif(len(set4) > 1):

                    set5=[]#If state transitions lead to the same set, these will be appended here
                    set6=[]#If state transitions do not lead to the same set, these will be appended here

                    #Saving the transitions of the first value in the list
                    temp=set4[0]

                    a=self.trans[temp][0]
                    b=self.trans[temp][1]

                    tempA=[]
                    tempB=[]

                    #Saving the state which the first value in the list points to
                    for x in set1:
                        if(a in x):
                            tempA = x 
                        if(b in x):
                            tempB = x

                    #Checking if the other elements in the list point to the same list
                    for y in set4:
                        if(self.trans[y][0] in tempA and self.trans[y][1] in tempB):
                            set5.append(y)#sameSet
                        else:
                            set6.append(y)#differentSet

                    if(len(set5)!=0):
                        set2.append(set5)
                    if(len(set6)!=0):
                        set2.append(set6)

        return set2

    #Initialising new DFA
    def DFAM(self,dfaM):


        #Creating temporary variables to store the new data
        statesM= []
        f_statesM = []
        transM = {}
        i_stateM = 0
        saveState={}

        #Looping through the new states set
        for x in dfaM:

            for y in x:
                #Checking for initial state
                if(y==self.i_state):
                    if(len(x)==1):
                        i_stateM = y
                    else:
                        i_stateM = x[0]
                
                #Checking for final states
                for i in range(len(self.f_states)):
                    if(self.f_states[i]==y):
                        if(x in f_statesM): 
                            break
                        else:
                            f_statesM.append(x)
                    else:
                        continue   

                #Adding transitions
                #If state was not combined with another, add to transition dictionary
                if(len(x)==1):
                    transM[y]=[self.trans[y][0],self.trans[y][1]]
                else:
                    #Else input the first number in the list in the dictionary
                    transM[x[0]]=[self.trans[y][0],self.trans[y][1]]
                    if(x[0] in saveState):
                        continue
                    else:
                        #Add the state combination in a list
                        saveState[x[0]]=x 

        #Checking if the state combination list has any values
        for key1 in saveState:
            #Appending values of current list into a temp list
            list1=[]
            for x in saveState[key1]:
                list1.append(x)
                #Checking all values of the transitions if in they are in the temp list
            for key2 in transM:
                #If in temp list change value to key1
                if(transM[key2][0] in list1):
                    transM[key2][0]=key1
                if(transM[key2][1] in list1):
                    transM[key2][1]=key1

        #Changing final states from nested list to list
        flatList1 = [ item for elem in f_statesM for item in elem]
        
        #Adding states
        for key in transM:
            statesM.append(key)

        #Removing final states that are no longer in the DFA
        for x in f_statesM:

            if(x not in statesM):
                f_statesM.remove(x)
        
        #Changing the values of the DFA A to that of M
        self.states = statesM
        self.i_state = i_stateM
        self.f_states = flatList1
        self.trans = transM
        self.size=len(statesM)


    def DFS(self, x, disc, low, stackMem, stack, scc):

        # Initialize discovery time and low value
        disc[x] = self.time
        low[x] = self.time
        #Incrementing the time
        self.time += 1
        #Append the value and add it in stackMem
        stackMem[x] = True
        stack.append(x)

        #Check transitions of state
        for y in self.trans[x]:

            #Not visited
            if(disc[y] == -1):

                self.DFS(y, disc, low, stackMem, stack, scc)

                low[x] = min(low[x], low[y])

            elif (stackMem[y] == True):

                low[x] = min(low[x], disc[y])  

        sccLength=0
        w = -1

        if(low[x] == disc[x]):
            #Printing current SCC
            print("SCC:", end = " ") 
            while w!=x:
                w = stack.pop()
                print(w, end=" ")
                sccLength+=1
                stackMem[w]= False

            print()
            #If scc has more than 1 state add into list
            if(sccLength > 1):
                scc.append(sccLength)


    #Recursively uses the dfs algorithm to find storngly connected components
    def Tarjans(self, ran):
        
        #Stores discovery time of visited states
        disc = [-1]*(ran)
        #Stores the minimum discovery time of state
        low = [-1]*(ran)
        #Used to check if state in stack
        stackMem = [False]*(ran)
        #Stores current connected states
        stack=[]
        #Used to store size of all SCCs
        scc=[]

        #Recursively call the function
        for x in self.states:
            if(disc[x]==-1):
                self.DFS(x, disc, low, stackMem, stack, scc)

        print("Size of largest SCC: ", max(scc))
        print("Size of smallest SCC: ", min(scc))

        
class main:

    #Usint the random class to have a random value between 16 and 64
    ran = random.randint(16,64)

    A = DFA(ran)
    cost = A.search()
    depth = A.depth(cost)

    #Printing the depth and number of states for DFA A
    print("Depth of A: ",  depth)
    print("Number of states in A: ", len(A.states))

    M = A.hopcroft()
    finalM = A.DFAM(M)

    cost1 = A.search()
    depth1 = A.depth(cost1)

    #Printing the depth and number of states for DFA M
    print("Depth of M: ",  depth1)
    print("Number of states in M: ", len(A.states))

    #Finding the strongly connected components in DFA M
    A.Tarjans(ran)
