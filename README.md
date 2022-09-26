# FIT2004
Assignment work from my FIT2004 computer science class at university.


Assignment 1:
 - The assignment was based of implementing count sort & radix sort to sort through an unsorted list of matches. Within the given time complexity of O(NM). 
    O(N) --> refers to N being the number of matches in results
    O(M) --> refers to the number of characters within a team names for each match.
    
    Inputs:
      - results: A list of lists with: 'team 1', 'team 2', 'match score'
      - roster: An integer that denotes how many the character set is
      - score: An integer value in the range of 0 to 100 inclusive
    
    Output:
      - top10matches: A list of 10 matches with the highest score, or the max amount of matches if there are less than 10
      - searchedmatches: A list of matches with the same score as 'score' or with the closest score which is higher
      
    An example:
    
    Input:
    
    results = [['C', 'A', 100],['A', 'B', 43],['C', 'A', 32],['C', 'A', 22],['C', 'C', 12],['C', 'B', 1],['B', 'B', 0], ['B', 'A', 23]]
    analyze(results, 3, 98)
    
    Output:
    
    [['B', 'B', 100], ['C', 'A', 100], ['B', 'C', 99], ['C', 'C', 88], ['A', 'C', 78], ['A', 'B', 77], ['A', 'C', 68], ['B', 'A', 57], ['A', 'B', 43],    ['C', 'A', 32]] [['B', 'C', 99]]
    
    
Assignment 2:
 - Part 1:
  For this part of the assignment I needed to find the shortest path between two points in a given graph whilest stopping at 'coffee shop' on the way. Within the time complexity of O(|E|log|V|) & O(|V|+|E|) space complexity.  
  O(V): the set of unique locations in roads
  O(E): the set roads
  
   To do this I used Dijkstra's algorithm first finding the shortest path from the start to a coffee shop then again from the end point to the same coffee shop. Then combined the two paths.
  Input:
    - start: The starting location on the graph
    - end: The location we are trying to get to
    - roads: A list of roads represented as a list of tuples (u, v, w). 'u' is the starting point, 'v' is the end point and 'w' is the time taken to travel from location u to location v
    - cafes: A list of coffee locations represented as a list of tuples (location, waiting_time)

   Output:
    - The shortest route in the form of a list of integers going from the start point to the end by passing a cafe to get a coffee.
    - If no such route exists from the start location to one of the cafes and proceeding next to the end location is possible, then the function will return None.
  
   An example:
  
   Inputs:
  
   roads = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
(5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
(8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    cafes = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
 
    mygraph.routing(start, end) (1 & 3 for this example)
  
    Output:
    [1, 5, 6, 3]
  
  
 - Part 2:
  For this part of the assignment I a path from two points that would return the highest score. The input was an directed acyclic graph so I had to use topological sort on the nodes to order them from highest to lowest. After that I found the the best path using the critcal path algorithm. This had to be done in a time complexity of O(D+P) & aux space complexity of O(D).
  
   O(D): number of downhill segments
   O(P): the number of intersection points
  
   Input:
    - downhillScores: A list of tuples containing: the start point of the downhill segment, the end point of the downhill segment and the score that can be achieved by going down it.
    - start: The point which we are starting at 
    - finish: The end point
  
   Output:
    - The route from start to finish that will result in the most points 
   
    An example:
   
    Input:
    downhillScores = [(0, 6, -500), (1, 4, 100), (1, 2, 300),
(6, 3, -100), (6, 1, 200), (3, 4, 400), (3, 1, 400),
(5, 6, 700), (5, 1, 1000), (4, 2, 100)]
    start = 6
    finish = 2
   
    Output:
    [6, 3, 1, 2]
