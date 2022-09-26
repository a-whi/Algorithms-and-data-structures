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
    
