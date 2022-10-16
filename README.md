# othello-atomic-object
 
This is my submission for the coding challange for Atomic Objects Accelertor Program, 2023

What Strategy did I use?

First, my program finds ALL avaliable empty slots surronding a white piece. Seeing that you MUST flank every turn, this seemed the safest route to go.

After finding all Empty slots, we check every slot if it has a leading ally piece, meaning if we place this piece, will we find a corrosponding piece on the other end to close the flank?

Finally, for a little (possibly unnessccarry? (Needs more testing)) efficency, I implemented 4 rules

Rule 1) ALWAYS capture the corner when it is avaliable
Rule 2) If you are player 1, you are better off playing random pieces because of the starting advantage (Slightly tested)
Rule 3) If you are player 2, you are to stay next to the center as possible...
Rule 4) While also trying to capture the edges.

Rule 3 and 4 where two strategies that I found many people argue on line, decided to implement both and flip a coin every time to see which strategy to implement. 

This is actually a feature, as this somewhat implements another strategy (Avoid putting slots on the 4x4 square from the center, also on line strategy)

This was fun! Thank you for your consideration!
