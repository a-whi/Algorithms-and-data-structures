"""
Assignment 3

Created by: Alexander Whitfield
Student ID: 32541767

"""
import math

# PART 1
class edge:
    def __init__(self, start, end, cap):
        """
        This function is used to create the edges in the adjacency list. This class stores the start, end, capacity, flow and the 
        residual flow (reverse flow).

         - Input:
                start: The starting point of the node
                end: Which node the node goes to
                cap: The capacity of flow that is allowed between the two points. Most are set to 1 except for a few excaptions

         - Output:
                There is no output. It just stores everything that relates to the edge.

        Time complexity: O(1)
        Aux space complexity: O(1)

        """
        self.start = start
        self.end = end
        self.cap = cap
        # I set these as 0 at the start as later when I run the Ford Fulkerson algorithm they change
        self.flow = 0
        self.reverse = 0

def allocate(availability):
    """
    This is my allocate function. This function creates the adjacency list and then calls other functions to find which
    flatmate does what meal.
    At the start of this function we find what the minimum & maximum of meals that need to be satisfied as well as the 
    number of available restaurant orders we can do.
    Then we create the adjacency list for this and set capacities for the edges as minimum values. 
    Then I call the Ford Fulkerson function which finds the max flow through the graph with the minimum number of meals
    set as the capacity. After that I change the capacity from the source to the flatmates to the maximum number of meals
    that they can make. Then I run Ford Fulkerson again.

    If the max flows from each run doesn't equal the number of meals required, then there is no solution available. 
    If they are equal then we run the distribute_meals function which finds who does what meal.
    Finally we return a list with that says who does breakfast and who does the dinner meals. 

    - Input:
        availability: 

    - Output:
        final_list: A list containing two sublits. The first being the allocation of the breakfast meals. The second being the 
                    allocation of the dinner meals. (breakfast,dinner)
        None: Will be returned if an allocation that satisfy all constraints does not exist

    Time complexity: O(n^2)
    Aux space complexity: O(n^2)

    """
    num_days = len(availability)    # Lets the function know how many days there are
    meals = 2 * num_days    # The max amount of meals

    # This will be the total number of nodes in the adjacency list. 
    total = 7 + meals + (5 * num_days) + 1  # must be 1 extra to account for the source starting at 0

    # Now I calculate the constraints
    rest_max = math.ceil(0.1 * num_days)   # The max amount of restaurant meals that cna be ordered
    person_min = math.floor(0.36 * num_days)   # The min amount of meals each person must do
    person_max = math.ceil(0.44 * num_days)    # The max amount of meals each person can do

    # Initialise the adjacency list
    adj_list = []

# This whole section is for the adjacency list O(N)^2
##### Quick break down of the structure #####
# Node 0 = source
# Node -1 = sink
# Node 1 - 5 is for each flatmate
# Nod 6 is the restaurant
# Each person is connected to their own set of all days in availability (Nodes 7 to 7+(5*number of days))
# Each day for that person connects to a node which that meal is related to (Nodes 7+(5*number of days) to 1-length of adj_list)
# Each meal is connected to the sink

    # Creates the adjacency list
    for i in range(total):
        adj_list.append([])

    # Connects source to all flatmates with the capacity set as the minimum amount of meals they have to make
    for i in range(1,6,1):
        x = edge(0, i, person_min)
        adj_list[0].append(x)

    # Connects source to restraunt with max restraunt capacity
    x = edge(0, 6, rest_max)
    adj_list[0].append(x)
    
    # Connect the flatmates to all days
    # Set capacity to 1 as each flatmate can only cook once per day
    for i in range(num_days):
        # For flatmate 0
        flatmate_0 = edge(1, i+7, 1)
        adj_list[1].append(flatmate_0)

        # For flatmate 1
        flatmate_1 = edge(2, i+7+num_days, 1)
        adj_list[2].append(flatmate_1)

        # For flatmate 2
        flatmate_2 = edge(3, i+7+(2*num_days), 1)
        adj_list[3].append(flatmate_2)

        # For flatmate 3
        flatmate_3 = edge(4, i+7+(3*num_days), 1)
        adj_list[4].append(flatmate_3)

        # For flatmate 4
        flatmate_4 = edge(5, i+7+(4*num_days), 1)
        adj_list[5].append(flatmate_4)

    # Now we connect all the days for the flatmates to the meals they can cook
    # All capacities are set to 1 as only 1 person can cook for that meal
    for i in range(len(availability)):
        for j in range(len(availability[i])):
            if j == 0:
                if availability[i][j] == 1:
                    x = edge(i+7, (i*2)+7+(5*num_days), 1)
                    adj_list[i+7].append(x) 

                elif availability[i][j] == 2:
                    y = edge(i+7, (i*2)+8+(5*num_days), 1)
                    adj_list[i+7].append(y) 

                elif availability[i][j] == 3:
                    x = edge(i+7, (i*2)+7+(5*num_days), 1)
                    adj_list[i+7].append(x) 

                    y = edge(i+7, (i*2)+8+(5*num_days), 1)
                    adj_list[i+7].append(y)  
                
                # If they aren't availabile then set the capacity to 0
                else:
                    x = edge(i+7, (i*2)+7+(5*num_days), 0)
                    adj_list[i+7].append(x) 

            elif j == 1:
                if availability[i][j] == 1:
                    x = edge(i+7+num_days, (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+num_days].append(x) 

                elif availability[i][j] == 2:
                    y = edge(i+7+num_days, (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+num_days].append(y) 

                elif availability[i][j] == 3:
                    x = edge(i+7+num_days, (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+num_days].append(x)

                    y = edge(i+7+num_days, (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+num_days].append(y) 

                # If they aren't availabile then set the capacity to 0
                else:
                    x = edge(i+7+num_days, (i*2)+7+(5*num_days), 0)
                    adj_list[i+7+num_days].append(x) 

            elif j == 2:
                if availability[i][j] == 1:
                    x = edge(i+7+(2*num_days), (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+(2*num_days)].append(x) 

                elif availability[i][j] == 2:
                    y = edge(i+7+(2*num_days), (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+(2*num_days)].append(y) 

                elif availability[i][j] == 3:
                    x = edge(i+7+(2*num_days), (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+(2*num_days)].append(x)

                    y = edge(i+7+(2*num_days), (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+(2*num_days)].append(y) 

                # If they aren't availabile then set the capacity to 0
                else:
                    x = edge(i+7+(2*num_days), (i*2)+7+(5*num_days), 0)
                    adj_list[i+7+(2*num_days)].append(x) 

            elif j == 3:
                if availability[i][j] == 1:
                    x = edge(i+7+(3*num_days), (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+(3*num_days)].append(x) 

                elif availability[i][j] == 2:
                    y = edge(i+7+(3*num_days), (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+(3*num_days)].append(y) 

                elif availability[i][j] == 3:
                    x = edge(i+7+(3*num_days), (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+(3*num_days)].append(x) 

                    y = edge(i+7+(3*num_days), (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+(3*num_days)].append(y)  

                # If they aren't availabile then set the capacity to 0
                else:
                    x = edge(i+7+(3*num_days), (i*2)+7+(5*num_days), 0)
                    adj_list[i+7+(3*num_days)].append(x) 

            elif j == 4:
                if availability[i][j] == 1:
                    x = edge(i+7+(4*num_days), (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+(4*num_days)].append(x) 

                elif availability[i][j] == 2:
                    y = edge(i+7+(4*num_days), (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+(4*num_days)].append(y) 

                elif availability[i][j] == 3:
                    x = edge(i+7+(4*num_days), (i*2)+7+(5*num_days), 1)
                    adj_list[i+7+(4*num_days)].append(x) 

                    y = edge(i+7+(4*num_days), (i*2)+8+(5*num_days), 1)
                    adj_list[i+7+(4*num_days)].append(y) 

                # If they aren't availabile then set the capacity to 0
                else:
                    x = edge(i+7+(4*num_days), (i*2)+7+(5*num_days), 0)
                    adj_list[i+7+(4*num_days)].append(x) 

    # Adds all meals as an option for the restraunt order
    for i in range(meals):
        x = edge(6, i+7+(5*num_days),1)
        adj_list[6].append(x)

    # Finally connect the meals to the sink
    for i in range(meals):
        x = edge(i + 7+(5*num_days), total-1, 1)
        adj_list[i + 7+(5*num_days)].append(x)

##### end of adjacency list creation #####

    # Setting the source and the sink
    s = adj_list[0]
    t = adj_list[-1]

    # Now I run the Ford Fulkerson algorithm to find the max flow for the minimum amount of meals each flatmate must cook
    x = ford_fulkerson(adj_list, s, t)  #O(maxflow * E) E = length of the adjacency list

    # Now we have found the max capacity for the minimum amount of meals each person must cook
    # Now we set all capacities from the minimum amount to the max amount keeping the flows that were previously calculated
    # So source to all flatmates need to be increased
    for i in range(0,5,1):
        adj_list[0][i].cap = person_max
        # Now we reset the residule flow
        adj_list[0][i].reverse = 0

    # We run the algorithm again with the new capacitys
    y = ford_fulkerson(adj_list, s, t)  #O(maxflow * E) E = length of the adjacency list

    # Check if we can not satisfy all constraints
    # We add the max flow from both runs of Ford Fulkerson to hopefully get the same number as meals required
    # if this happens then we know there is a viable solution
    # If not return None
    if (x + y) < meals:
        return None

    # Now we run distribute_meals which finds who does what meal
    returnlist = distribute_meals(adj_list, meals, num_days)    #O(N^2)

    return returnlist


def ford_fulkerson(adj_list, s, t):
    """
    This function finds the max amount of flow that can go from the source to the sink. As I have already created
    the adjacency list this function will basically check to see if there is a viable path that can satisfy the 
    demands of the problem. 
    If there is a solution I'll be able to find which flatmate does what meal later by using the adjacency list which is
    updated as this graph runs. 

    - Input:
        adj_list: A list that holds all nodes
        s: The source 
        t: The sink

    - Output:
        max_flow: The max amount of flow that can go through the graph

    Time complexity: O(maxflow * E) E = length of the adjacency list
    Aux space complexity: O(maxflow * E) E = length of the adjacency list

    """
    # Set max flow as 0
    max_flow = 0
    # Set the bottleneck to infinity so it can be changed later
    bottleneck = float('inf')

    #This will keep going till augment == 0
    while True:
        # Create an array to check if we have visited the node
        visited = [False] * len(adj_list) #O(1)
        # Call DFS to run and find the max flow
        augment = dfs(adj_list, s, t, bottleneck, visited) #O(N)
        max_flow += augment

        if augment == 0:
            break

    return max_flow

def dfs(adj_list, u, t, bottleneck, visited):
    """
    This is my depth first search function. DFS is used to find all the viable paths from the source to the sink.
    It does this recursively.

    - Input:
        adj_list: A list that holds all nodes
        u: The starting node/the node that we are on
        t: The sink
        bottleneck: The amount of flow that can get through the edge with minimum capacity available
        visited: A list to see if we have already visited the node

    - Output:
        augment: Which is the max flow found in the path

    Time complexity: O(N)
    Aux space complexity: O(N)

    """
    if u == t:  # If we hit sink return
        return bottleneck

    visited[u[0].start] = True  # Mark as visited

    # This will loop through all nodes connected to u
    for i in range(len(u)):
        residual = u[i].cap - u[i].flow

        # As long as there is capacity for more flow & we haven't wisited the node before we can call DFS again
        if residual > 0 and not visited[u[i].end]:
            # Now we call DFS again with the updated values
            augment = dfs(adj_list, adj_list[u[i].end], t, min(bottleneck, residual), visited)
            if augment > 0: # We found an augmenting path - add the flow and deduct from the reverse flow
                u[i].flow += augment
                u[i].reverse -= augment
                return augment

    return 0 # If we can not find an augmenting path

def distribute_meals(adj_list, meals, num_days):
    """
    This function finds which flatmate does what meal. To do this we must go through all the nodes connected
    to the flatmates, then if there is a flow going to the day that is connected to them we check to see what
    meal is connect to that day and if there is a flow going to it. Finally we append the flatmate to the meals
    index in the final list.
    Then after we have found all possible meals for each flatmate the remaining empty meals will be replaced with
    restaurant orders as the restaurant is connected to all meals. 
    After that we spit the final list into the breakfast list and the dinner list and return them to the allocate
    function.

    - Input:
        adj_list: A list that holds all nodes
        meals: This is the number of meals that need to be made 
        num_days: This is the number of days (length of availability)

    - Output:
        breakfast: A list of who does each breakfast meal
        dinner: A list of who does each dinner meal

    Time complexity: O(N^2)
    Aux space complexity: O(N^2)

    """
    # Set up a list that is the length of meals and set all characters as 9 (This was mainly to check the output worked)
    final = [9] * meals

    # Initialise the breakfast and dinner lists
    breakfast = []
    dinner = []

    # Set up a variable that keeps track of which flatmate is doing each meal
    number = 0
    # Now we loop through all the flatmates
    for i in range(1,6,1):
        # We loop through the days that are conencted to each flatmate
        for j in range(num_days):
            # if flow == 1 then it can go to the day
            if adj_list[i][j].flow == 1:
                # I subtract 1 because flatmate 0's node is set as 1 since node 0 is the source
                number = adj_list[i][j].start - 1
                # This finds what node we are pointing to so we can start from that node to find what meals we can make
                new_start = adj_list[i][j].end

                # if their availablity is 3 then there will be 2 poosible melas that can be made
                if len(adj_list[new_start]) != 1:
                    # This checks the first option
                    if adj_list[new_start][0].flow == 1:
                        
                        # If the flow is 1 then we must find whether the meal is a breakfast or a dinner meal
                        # Breakfast meals are on even nodes
                        # Dinner meals are on odd nodes
                        if adj_list[new_start][0].end%2 == 0:
                            # Now we find the meals index in the final list so we subract 5*number of days and subtract 7 as 
                            # 7 is the number of nodes from source to day 1
                            final[(adj_list[new_start][0].end)-(5*num_days)-7] = number

                        elif adj_list[new_start][0].end%2 != 0:
                            final[(adj_list[new_start][0].end)-(5*num_days)-7] = number

                    # This checks the second option
                    elif adj_list[new_start][1].flow == 1:

                        if adj_list[new_start][1].end%2 == 0:
                            final[(adj_list[new_start][1].end)-(5*num_days)-7] = number
                        elif adj_list[new_start][1].end%2 != 0:
                            final[(adj_list[new_start][1].end)-(5*num_days)-7] = number

                # if there is only 1 node connect to the day (so their availability is 1 or 2)
                elif adj_list[new_start][0].flow == 1:
                    # If the flow is 1 then we must find whether the meal is a breakfast or a dinner meal
                    # Breakfast meals are on even nodes
                    # Dinner meals are on odd nodes

                    if adj_list[new_start][0].end%2 == 0:
                        final[(adj_list[new_start][0].end)-(5*num_days)-7] = number
                    elif adj_list[new_start][0].end%2 != 0:
                        final[(adj_list[new_start][0].end)-(5*num_days)-7] = number

            else:
                continue

    # Sets all other meals to be restraunt orders
    for i in range(len(final)):
        if final[i] == 9:
            final[i] = 5
        else:
            continue

    # Now I append the first 10 meals to breakfast and that last 10 meals to dinner
    for i in range(len(final)):
        if i < num_days:
            breakfast.append(final[i])
        else:
            dinner.append(final[i])

    # Return the two lists
    return breakfast, dinner

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   
#                    END OF PART 1
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   
#                   START OF PART 2
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   # 

# PART 2
class Node:
    def __init__(self):
        """
        This function is used to create Nodes. This class just stores the children the the node points to.

         - Input:
                No input is required

         - Output:
                There is no output. It just holds the children of the node.

        Time complexity: O(1)
        Aux space complexity: O(1)

        """

        self.child = [] 

class suffix_tree:

    def __init__(self):
        """
        This function is used to initialise the graph data structure. In this function I initialise Node() for the root.

         - Input:
                No input is required

         - Output:
                There is no output for this function.

        Time complexity: O(1)
        Aux space complexity: O(1)

        """
        # Now we initialise the node
        self.root = Node()

    def inserting(self, sub1):
        """
        We are inserting each letter one by one sequentially. And as we get further into the input list we will traverse
        through the tree to find where the letter needs to go. 

        - Input:
            sub1: This is a list of lists containing the orignial characters in the submission but each iteration has one less 
                  character in it until we reach the last letter in the phrase.

        - Output:
            There is no output as this function is building the suffix tree with the given string of letters. 

        Time complexity: O(N+M)^2
        Aux space complexity: O(N+M)

        """
        # This is where we insert the letters from the submissions into the suffix tree

        for item in sub1:   # This is O(N) as it loops for however many items there are in sub1

            pointer = self.root # We initialise the pointer at the root 

            for character in item: # O(M) as we go through each letter in the word

                letter_in_tree = False # We set a variable as False as we don't know if the letter is in the tree already

                # If there is a child at the node we are at then we loop through the children
                if pointer.child:
                    # Loop through all the children
                    for i in pointer.child: 
                    # O(children) This should not affect the time complexity as the loop would never be the size of N or M

                        #If we find a child with the same character, we move the pointer so we know where that character is
                        if i[0] == character:
                            pointer = i[1]
                            #We make letter_in_tree = true as we have found a place for the letter already in the tree
                            letter_in_tree = True
                            break

                # If the character is not already in the tree then we must add the character to the tree  
                if letter_in_tree == False:
                    #If the is not already a child for the letter we add the letter to the child
                    pointer.child.append([character, Node()])
                    pointer = pointer.child[-1][1]


    def find_longest(self, sub2):
        """

        - Input:
            sub1: This is a list of lists containing the orignial characters in the submission but each iteration has one less 
                  character in it until we reach the last letter in the phrase.

        - Output:
            substring_max: This is a list that holds all the character from the longest common substring
            count_max: This is the amount of character in the substring_max

        Time complexity: O(N+M)
        Aux space complexity: O(N+M)

        """
        # Initalising all counters and empty lists to find the longest common substring
        count = 0
        count_max = 0
        substring = []
        substring_max = []

        # Similar to the insert function but we are not adding any new chaacters to the tree
        for item in sub2:   # This is O(N) as it loops for however many items there are in sub2

            pointer = self.root # We initialise the pointer at the root 

            for character in item: # O(M) as we go through each letter in the word

                letter_in_tree = False # We this as False at the start 

                # If there is a child at the node we are at then we loop through the children hoping to find the character
                if pointer.child:
                    # Loop through all the children
                    for i in pointer.child: 
                    # O(children) This should not affect the time complexity as the loop would never be the size of N or M
                        
                        # If we find a child with the same character we change the pointer
                        if i[0] == character:
                            pointer = i[1]
                            # We make letter_in_tree = true as we have found a place for the letter already in the tree
                            letter_in_tree = True
                            # Now we increase the count by 1
                            count += 1
                            # We append the letter to the substring
                            substring.append(i[0])
                            break

                # If the character is not found 
                if letter_in_tree == False:
                    # Now we see if the substring is longer than current max_substring
                    if count > count_max:
                        # We change the max count
                        count_max = count
                        # Clear the current substring_max list
                        substring_max = []
                        substring_max.append(substring) #O(1)
                    # If the count is bigger than the current max count then we clear the substring and the count to start on a new substring
                    substring = []
                    count = 0

            # Finally if we reach the end of the list we have to check if the current max substring is still the largest
            if count > count_max:
                count_max = count
                substring_max = []
                substring_max.append(substring)
            count = 0 
            substring = []

        return substring_max, count_max



def compare_subs(submission1, submission2):
    """
    This is my compare function which is used to compare the two input strings and return the longest common substring as well
    as the similarity score for each input. 
    To do this first I created two new lists which is a list of the original inputs just with one less character in every iteration.
    This is used later in the suffix tree to build it and then find the longest substring. 
    After creating these two new lists I create my suffix tree which I made a class for as it was easier to build in a class form, as 
    I need to loop through different nodes and their children. 
    First I insert the first list into the suffix tree using the insert function. This builds the suffix tree with the list.
    Then I insert the second submission into the tree using another function called find_longest. This function is the same as the 
    insert function although it find the longest common substring and doesn't add any new charcters.
    Finally the output from find_longest is returned and I divide the length of the substring by the total length of the original 
    lists to get the similarity percentage. I also join the substring together as when it is in the find_longest function the 
    characters are added to a list indiviually. Then I return the required output.

    - Input:
        submission1: a string containing only characters in the range [a-z] or the space character
        submission2: a string containing only characters in the range [a-z] or the space character

    - Output:
        final_list: A list which has the longest common substring between submission1 and submission2, the similarity score for 
                    submission1 as a percentage and the similarity score for submission2 as a percentage 

    Time complexity: 
        - To build the suffix tree: O(N+M)^2
        - Computing the comparison between the two strings: O(N+M)
    Aux space complexity: O(N+M)

    """
    # Creating the new lists
    sub1 = []   
    sub2 = []

    # Looping through the lists to create a list of lists with the original input minus a character each iteration
    for i in range(len(submission1)):   #O(M)
        sub1.append(submission1[i:])    #O(1)


    for i in range(len(submission2)):   #O(N)
        sub2.append(submission2[i:])    #O(1)

    # Now I create the suffix tree
    tree = suffix_tree()

    # Insert the first submission to the create the tree
    tree.inserting(sub1)

    # Now I insert the second submission to add to the tree and find the longest substring
    x = tree.find_longest(sub2)

    # Calculating the similarity
    sub1_percent = round((x[1]/len(sub1)) * 100)
    sub2_percent = round((x[1]/len(sub2)) * 100)

    # Join the chartacters together
    final_list = list(map(''.join, x[0]))   # I believe this is O(N^2) as the list and map functions are both O(N) complexity

    # Finally I append everything to final_list
    final_list.append(sub1_percent)
    final_list.append(sub2_percent)

    return final_list