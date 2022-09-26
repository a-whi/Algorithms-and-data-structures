"""
Assignment 2

Created by: Alexander Whitfield
Student ID: 32541767

"""
import heapq

class RoadGraph:
    def __init__(self, roads, cafes):
        """
        This function is used to initialise the graph data structure. In this function I initialise 'cafes' and 'roads'. I take the input 
        'roads' and find the highest loccation in the list and create an adjacency list as long as the highest location found. In the 
        adjacenct list each index is a location and has a list of locations you can get to from the index location and time that it will 
        take to get there. I used an adjacency list because it is better suited for the inputs the program will be recieving and is more 
        effienct than if I were to use an adjacency matrix. 

         - Input:
                roads: A list of roads represented as a list of tuples (u, v, w). 
                       'u' is the starting point, 'v' is the end point and 'w' is the time taken to travel from location u to location v

                cafes:  A list of coffee locations represented as a list of tuples (location, waiting_time)

         - Output:
                There is no output for this function as it is just used to initalise the graph data structure. 

        Time complexity: O(V+E)
        Aux space complexity: O(V+E)

        """
        # Initialising roads and cafes
        # O(1) to create
        self.roads = roads
        self.cafes = cafes
        self.cafes_locations = []

        for i in range(len(self.cafes)):
            self.cafes_locations.append(self.cafes[i][0]) 

        # Sorting roads and cafes into adjeceny list
        # Firstly I need to find the maximum node given in roads
        max = 0

        for i in range(len(roads)):     # O(E) looping through all road inputs to find the highest location value
            if roads[i][1] > max:
                max = roads[i][1]
            elif roads[i][0] > max:
                max = roads[i][0]

        
        # A list of lists to represent an adjacency list
        # 'adj_list' will be used as the graph in future functions
        self.adj_list = [[]] * (max+1)      # O(1) to create
        # 'transp_adjlist' will be used as a transposed graph in future functions
        self.transp_adjlist = [[]] * (max + 1)
 
        # Allocate blank lists for the two adjacency lists so it can hold values later
        for i in range(max):        # O(V) 
            self.adj_list[i] = []
            self.transp_adjlist[i] = []

        # Adds edges to the adjacency list
        for i in range(len(roads)):     # O(E)
            self.adj_list[roads[i][0]].append((roads[i][1],roads[i][2]))
            self.transp_adjlist[roads[i][1]].append((roads[i][0],roads[i][2]))


    def routing(self, start, end):
        """
         High level description about the functiona and the approach you have undertaken.

        - Input:
            start: The starting location on the graph
            end: The location we are trying to get to

        - Output:
            . The shortest route in the form of a list of integers going from the start point to the end by passing a cafe to get a coffee.
            . If no such route exists from the start location to one of the cafes and proceeding next to the end location is possible, 
            then the function will return None.


        Time complexity: O(Elog(V))
        Aux space complexity: O(V+E)

        """
        # Just checks to see if there are any cafes in the inputs. If not then it will return None in cafe then the can't be a route
        if self.cafes == []:
            return None

        # Create a final list which will hold the paths and distances
        final_list = []

        # Dijkstra's Algorithm O(Elog(V))
        # Performs the operation needed to find the optimal route
        self.Dijkstras(self.adj_list, start)

        # This will hold the predecessor array in it from the first time we run Dijkstra's algorithm
        # It is used later to find the shortest path 
        predarr_1 = []
        
        # This loops through and adds all values in the predecessor array to a new array
        for i in range(len(self.pred_arr)):
            predarr_1.append(self.pred_arr[i])

        # This appends all the cafe locations into a list called 'cafe_location_distance'
        for i in range(len(self.cafes)):
            cafe_location_distance = []
            #find cafe node
            cafe_location_distance.append(self.cafes[i][0])
    
            # Next we add the wait times to get a coffee and the distances to get from the start to the coffee shop
            cafe_location_distance.append(self.dist_arr[self.cafes[i][0]] + self.cafes[i][1])
            # Finally both are stored in 'final_list' in the form (location, total time)
            final_list.append(cafe_location_distance)
            # This gives us total distance from start to cafes
            
        # Now we change the starting point to the end point and work backwards to the cafes.
        # Dijkstra's Algorithm O(Elog(V))
        # Performs the operation needed to find the optimal route
        self.Dijkstras(self.transp_adjlist, end)

        # This will hold the predecessor array for the second time we run Dijkstras in it.
        # It is used later to find the shortest path from end point to cafe.
        predarr_2 = []

        # This loops through and adds all values in the predecessor array to a new array
        for i in range(len(self.pred_arr)):
            predarr_2.append(self.pred_arr[i])

        for i in range(len(self.cafes)):
            # Adds the distances from end point to the cafes
            final_list[i][1] += self.dist_arr[self.cafes[i][0]]

        # find min
        min = float('inf')
        node = 0
        # This loops through and find the shortest wait time
        for i in range(len(final_list)):

            if final_list[i][1] < min:
                min = final_list[i][1]
                # This also updates the locations so we know which cafe it is
                node = final_list[i][0]

        current = node  
        # This just checks to make sure that the node is in the cafe list.
        # If not then there is no route with a cafe stop, so it will return none.
        if current not in self.cafes_locations:
            return None
        # Empty array to store the route
        shortestpath = []

        while current != start:
            shortestpath.append(current)
            #if current in cafe_locations:
                #x = 1
            current = predarr_1[current]

        shortestpath.append(start)

        # reverse shortest path
        shortestpath = shortestpath[::-1]  

        # If the end point has a cafe at it and its the shortest time it will immediately return the route 
        if node == end:
            return shortestpath

        else:
            # Loops again but this time from the cafe to the end point
            current = node    
            current = predarr_2[current]
            while current != end:
                shortestpath.append(current)
                current = predarr_2[current]

            shortestpath.append(end)

            # Finally returns the shortest path
            return shortestpath

    def Dijkstras(self, graph, starting_point):
        """
        This function is my Dijkstras alorithm. An algorithm that allows you to find the shortest path between any two locations on a 
        graph.
        For this function I first initialised 3 lists: queue_arr, pred_arr & dist_arr. These are all need for the algorithm to work.
        The queue holds a queue for all locations in the graph. The predecessor array stores the route to get to each location and the
        distance array stores the distances between all locations. 
        After initialising the arrays I set the distances in the distance array to infinity so no matter what is given in the input it 
        will always be changed to the shortest distance. 
        Then useing heapq I added the queue_arr as well as the starting location to the heap. and began looping through the locations in 
        the graph. As I found the shortest path to each location I'd update the distance array and the predecessor array as well as pop
        and push different locations on and off the heap. 

        - Input:
            graph: Either the adjacency list for the normal graph or the transp_adjlist for the flipped graph.

            starting_point: The location that the algorithm starts at

        - Output:
            self.dist_arr: This is an array that holds all distances from the starting point to all locations

            self.pred_arr: This is an array that hold the routes taken to get to the locations


        Time complexity: O(Elog(V))
        Aux space complexity: O(V+E)

        """

        # Setting up a queue
        queue_arr = []  # O(1)

        # Setting up the predecessor array this records the path
        self.pred_arr = [0] * len(graph)    # O(1)

        # Setting up the distance array this will record the distances to all locations
        self.dist_arr = [0] * (len(graph))  # O(1)

        # Setting up all distnces as infinity at the start
        for i in range(len(graph)): # O(V)
            self.dist_arr[i] = float('inf')

        # The starting point will have a distance of 0 though
        self.dist_arr[starting_point] = 0

        # Using heapq as we are allowed to import it. It is an implementation of the heap queue algorithm,
        # basically means that I dont have to set up my own heap queue. I can just use one that is already made.
        # Add the queue_arr as well as the starting location to the heap.
        heapq.heappush(queue_arr, [0, starting_point])  # O(logV)

        # This is the loop that goes through the queue_arr and find the other locations that are connected
        # Go from start to all cafes then record the path and distance 
        # This loop will break when the queue is empty
        while len(queue_arr) > 0:   #O(log(V))

            # node_dist & curr_node are the top item in the heap and are poped off
            node_dist, curr_node = heapq.heappop(queue_arr) # O(logV)

            # Loops through all locations that are connected to graph[curr_node]
            for edges in graph[curr_node]:  #O(E)

                total_dist = node_dist + edges[1]

                # If the total distance (distance from all previous nodes + current node weight) is smaller than the value in
                # the dist_arr index pred_arr & dist_arr will be changed and the queue_arr as well as the [total_dist & location] are
                # pushed onto the heap
                if total_dist < self.dist_arr[edges[0]]:

                    self.pred_arr[edges[0]] = curr_node
                    self.dist_arr[edges[0]] = total_dist
                    heapq.heappush(queue_arr, [total_dist, edges[0]])   # O(logV)

        return self.dist_arr, self.pred_arr


def optimalRoute(downhillScores, start, finish):
    """
    This is my optimalRoute function which returns a list of nodes going from the start point to the end point while scoring
    the maximum score. 
    For the function to do this first we find the max node in the downhillScores. This lets use create the arrays we need to the
    correct lengths. 
    After that we append the values from the downhillScores into an adjacency list. 
    Because this is a directed acyclic graph we need to do a topological sort on the nodes to order them from highest to lowest. 
    After that we go through the sorted topological list finding the largest scores between the nodes and updating an array which
    stores the data. 
    Then once we have found the score between the nodes we can append the nodes going from the starting point to the end point with
    the largest scores. 

    - Input:
        downhillScores: A list of tuples containing: the start point of the downhill segment, the
                        end point of the downhill segment and the score that can be achieved by going 
                        down it.
        start: The point which we are starting at 
        finish: The end point

    - Output:
        .The route from start to finish that will result in the most points 


    Time complexity: O(D+P)
    Aux space complexity: O(D)

    """
    #Finding the max node in downhillScores
    max = 0
    for i in range(len(downhillScores)):    #O(D)
        if downhillScores[i][0] > max:
            max = downhillScores[i][0]
        elif downhillScores[i][1] > max:
            max = downhillScores[i][1]
        
    # A list of lists to represent an adjacency list
    adj_list = [[]] * (max+1)   #O(1)

    # I also create an array which just has only nodes as for my topological sort function I could only manage to get 
    # it to work with just the nodes and no weights
    just_nodes = [[]] * (max+1) #O(1)

 
    # allocate memory for the adjacency list & just_nodes
    for i in range(max):    #O(D)
        adj_list[i] = []
        just_nodes[i] = []


    # add edges to the graph 
    for i in range(len(downhillScores)):
        adj_list[downhillScores[i][0]].append((downhillScores[i][1],downhillScores[i][2]))
        just_nodes[downhillScores[i][0]].append((downhillScores[i][1]))

    # Call top_sort to do a topological sort
    top_list = top_sort(just_nodes) #O(D+P)

    # Now we have the topilogical sorted list we reverse the list as we are starting from the bottom working up 
    # to the start
    top_list = top_list[::-1]   #O(D) cause we are reversing the list

    # Setting up the distance array this will record the distances to all locations
    dist_arr = [0] * (len(adj_list))  # O(1)

    # Setting up all distnces as infinity at the start
    for i in range(len(adj_list)):  #O(D)
        dist_arr[i] = float('-inf')

    # The starting point will have a distance of 0 though
    dist_arr[start] = 0
    
    dist_arr = [0] * (len(adj_list))  # O(1)
    pred = [[]] * (len(adj_list))
    final_list = []

    # Setting up all distnces as -infinity at the start
    for i in range(len(adj_list)):
        dist_arr[i] = float('-inf')

    # The starting point will have a distance of 0 though
    #dist_arr[start] = 0
    dist_arr[top_list[-1]] = 0

    while len(top_list) > 0:    #O(D)
        
        # Take the last value in top_list
        # We are starting from the last node and working back to the starting point
        vert = top_list.pop()

        # Now we loop through the values in the adj_list index
        for i in range(len(adj_list[vert])):    #O(P)
            
            total_weight = dist_arr[adj_list[vert][i][0]] + adj_list[vert][i][1]

            #If the total_weight is larger than the value in the distance array. Then the 
            # distance array will be changed to the total_weight
            # Also the predecessor array gets up dated so later we can find the path.
            if dist_arr[vert] < total_weight:   #O(1)
                dist_arr[vert] = total_weight
                pred[vert] = adj_list[vert][i][0]

        #Since we are looping backwards if the vertex that we pop off from the top_list is the 
        # start then we don't need to loop any more and it can break
        if vert == start:
            break 

    # This is a check that makes sure we can get from the end point to the start point
    # If not then the function will just return None
    if dist_arr[start] == float('-inf'):
        return None

    # Now we must find the path from the start to the finish
    current = start
    # So we loop till the current equals the finish
    while current != finish:    #O(D)
        # We just append the current into a list which is returned at the end
        final_list.append(current)  #O(1)
        # This is another test to make sure that there is a viable path
        if pred[current] == []: #O(1)
            return None
        current = pred[current] #O(1)

    # Append the finish vale to the list as the loop breaks before it is added
    final_list.append(finish) #O(1)

    # Return a list of nodes going from start to finish while getting the maximum points available
    return final_list


def top_sort(real_nodes):
    """
    This function is used with a depth first search function to order the nodes in the graph. Topological sort
    sorts the nodes in a graph in decending order going from parent to child. 
    This function starts by creating an array which marks all the nodes as false since they have not been visited yet. 
    Then we run a for loop which goes through the len(real_nodes). If the the index of the visited array is marked False
    then the function calls DFS and DFS goes through the rest of the visited array marking the nodes as visited and then appending
    the node to a list named 'top_list'.

    - Input:
        real_nodes: This is just the adjacency list, but with only nodes and no weights. 

    - Output:
        top_list: A sorted list of vertices in decending order of where they are on the graph 
                  (The vertex that is highest on the graph will come first)

    Time complexity: O(D+P)
    Aux space complexity: O(D)

    """
    # Create a list that is the length of the input.
    # Mark all values in the list as false as they havent been visited yet.
    visited = [False] * len(real_nodes) #O(1)

    # A list to store the order  
    top_list = []   #O(1)

    # This for loop goes through the real_nodes list
    for i in range(0, len(real_nodes)): #O(D)

        # If the index in real_nodes is marked as False in the visited array
        # IT will call DFS
        if not visited[i]:  #O(P)
            dfs(i, real_nodes, top_list, visited) #O(D)

    # Finally returns the top_list back to the optimalRoute function
    return top_list


def dfs(node, real_nodes, top_list, visited):
    """
    This is my depth first search function. DFS is used in topological sort as it ensures that the parent node
    will be stored before the child node is stored, thus returning a list in decending order from parent to children.

    - Input:
        node: The for loop iteration from the top_sort function
        real_nodes: This is just the adjacency list, but with only nodes and no weights. 
        top_list: A list of vertices in decending order of where they are on the graph 
        visited: An array of values marks either true or false depending if they have been visited yet

    - Output:
        top_list: A sorted list of vertices in decending order of where they are on the graph 
                  (The vertex that is highest on the graph will come first)

    Time complexity: O(D)
    Aux space complexity: O(D)

    """
    # Mark as visited
    visited[node] = True
   
    # Traverse for all its children
    for i in range(0,len(real_nodes[node])): 
   
        # If it has not been visited it will call DFS again 
        # This will loop recursively until all values in the visited array are marked as True. 
        if not visited[real_nodes[node][i]]:
            dfs(real_nodes[node][i], real_nodes, top_list, visited)
 
    # Finally append the node to a list to store its position
    top_list.append(node)