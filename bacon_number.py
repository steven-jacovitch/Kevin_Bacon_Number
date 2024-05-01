import random

random.seed(17)

from collections import deque


class BaconNumberCalculator:
    """
    A class to calculate the Kevin Bacon number in a network of actors.

    Parameters
    ----------
    fileName : str
        The name of the file containing the movie data.

    Attributes
    ----------
    adjList : dict of dict/dict of list/ dict of tuple/etc...

    Methods
    -------
    generateAdjList(fileName)
        Constructs the adjacency list from the given file.

    calcBaconNumber(startActor, endActor)
        Calculates the Bacon number between two actors.

    calcAvgNumber(startActor, threshold)
        Calculates the average Bacon number for a given actor.
    """

    def __init__(self, fileName):
        """
        Constructs all the necessary attributes for the BaconNumberCalculator object.

        Parameters
        ----------
        fileName : str
            The name of the file containing the movie data.
        """
        self.adjList = {}
        self.generateAdjList(fileName)

    def generateAdjList(self, fileName):
        """
        Reads a file and builds an adjacency list representing actor connections.

        Parameters
        ----------
        fileName : str
            The name of the file to read the movie data from.
            You need to think about which encoding you should use,
                To load the file.



        Attributes
        ----------
        adjList : dict of dict/dict of list/ dict of tuple/etc...
        The key of the adjList should be the original(unmodified) actor name
        in the inputted file. You should not and do not need to modify it.
        For example:
        Bacon, Kevin
        Kidman, Nicole


        Note
        ----------
        Adjacency list representing the actor connections.
        For example:
        adjList = {actor1 : {actor2: movie1} ,{actor3: movie1}}
        or
        adjList = {actor1 : [[actor2,movie1],[actor3, movie1]]}
        or
        ...

        Hint
        ------
        Do we need all of the movie information/name in which two
        actors performed together stored in the adjList?
        Or just one pair is sufficient?
        ie  {actor1 : {actor2: movie1} }
        not  {actor1 : {actor2: [movie1,movie2]} }
        Think about how many pathes we need to find between the inputted actor,
        just one or many.


        Returns
        -------
        None
        """
        try:
            # Open the file with the specified encoding
            with open(fileName, "r", encoding="ISO-8859-1") as file:
                # Iterate over each line in the file
                for line in file:
                    # Strip leading/trailing whitespaces and split the line by '/'
                    parts = line.strip().split("/")
                    # The first part is the movie
                    movie = parts[0]
                    # The remaining parts are the actors
                    actors = parts[1:]
                    # Iterate over each actor
                    for i in range(len(actors)):
                        if actors[i] not in self.adjList:
                            self.adjList[actors[i]] = {}
                        for j in range(i + 1, len(actors)):
                            if actors[j] not in self.adjList[actors[i]]:
                                self.adjList[actors[i]][actors[j]] = movie
                            # Check if the co-actor is in the adjacency list
                            if actors[j] not in self.adjList:
                                self.adjList[actors[j]] = {}
                            # Add the actor to the co-actor's adjacency list
                            if actors[i] not in self.adjList[actors[j]]:
                                self.adjList[actors[j]][actors[i]] = movie
        # If an exception occurs, print the error message
        except Exception as e:
            print(f"An error occurred: {e}")

    def calcBaconNumber(self, startActor, endActor):
        """
        Calculates the Bacon number (shortest path) between two actors.

        Parameters
        ----------
        startActor : str
            The name of the starting actor.
        endActor : str
            The name of the ending actor.

        Returns
        -------
        List[int, List[str]]
            A List containing the Bacon number and the path of connections.
            The second List should be in the following form.
            [startActor, moive1, actor1, moive2,actor1, movie3,endActor]

        Note
        -------
        1.A local variable visited:set() is needed, which aviod visiting the same
        actor more than once.

        2.List should not be used to simulate the behavior of a queue.
        related reading:https://docs.python.org/3/tutorial/datastructures.html
        solution to is question is in the next line of the reason in the website

        3. It should return [-1, []], if one of the inputted actor is not
        in our graph.

        4.It should return [0, [start actor]], if the start actor is the end actor

        Hint
        -------
        What infomation you should store in the queue?
        Should it be the whole current path, or a single actor, or a tuple with
        length of two?

        If the whole path, think about how many new list object you might create
        during the process. Notice, create a new list is not very time efficient.

        If a single actor, think about how to reconstruct the path from startActor
        to endActor. Will you need a dictionary to do so?

        If a tuple, think about what information need to be in the tuple, and
        how to reconstruct the path. Will you need a dictionary to do so?

        BFS is a search algorithm that extends step by step, so if a point is traversed,
        there is one and only one path to the point due to the visited set.
        Each time, you enqueue an actor,
        record the actor and movie before it in a dictionary.

        """

        # If either actor is not in the adjacency list, return [-1, []]
        # This means that there is no path between the actors
        if startActor not in self.adjList or endActor not in self.adjList:
            return [-1, []]

        # If the start and end actors are the same, return [0, [startActor]]
        # This means that the path is just the actor themselves
        if startActor == endActor:
            return [0, [startActor]]

        # Initialize a set to keep track of visited actors
        visited = set()

        # Initialize a queue with the start actor
        queue = deque([startActor])

        # Initialize a dictionary to keep track of the previous actor and movie for each actor
        # This will be used to reconstruct the path
        prev = {
            startActor: (None, None)
        }

        # While there are still actors to visit
        while queue:
            # Get the next actor from the queue
            actor = queue.popleft()

            # If this is the end actor, we've found a path
            if actor == endActor:
                # Initialize an empty list to store the path
                path = []

                # Go backwards from the end actor to the start actor, adding each actor and movie to the path
                while actor is not None:
                    path.append(actor)
                    actor, movie = prev[actor]
                    if movie is not None:
                        path.append(movie)

                # Reverse the path so it goes from start to end, and return it along with its length
                path.reverse()
                return [len(path) // 2, path]

            # If we haven't visited this actor yet
            if actor not in visited:
                # Mark it as visited
                visited.add(actor)

                # For each co-actor of this actor
                for coActor, movie in self.adjList[actor].items():
                    # If we haven't visited the co-actor yet and it's not already in the path
                    if (
                        coActor not in visited and coActor not in prev
                    ):
                        # Add the co-actor to the path and queue it up for visiting
                        prev[coActor] = (actor, movie)
                        queue.append(coActor)

        # If we've gone through all actors and haven't found a path, return [-1, []]
        return [-1, []]

    def calcAvgNumber(self, startActor, threshold):
        """
        Calculates the average Bacon number for a given actor until convergence.

        The method iteratively selects a random actor and computes the Bacon number
        from the startActor to this random actor. It updates and calculates the
        average Bacon number. This process continues until the difference between
        successive averages is less than the specified threshold, indicating convergence.

        pseudocode
        ----------
        Initialize previousAvg to 0, curDiff to a large number (acting as infinity)
        Create a list of all possible actors from the adjacency list.
        Enter a while loop that continues as long as curDiff is greater than the threshold.
        a. Increment round count.
        b. Choose a random actor from the list of possible actors.
        c. Calculate the Bacon number (bNum) from startActor to the chosen actor.
        d. If bNum is valid (not -1 and not 0):
            addjust totalBNum and calculate the difference (curDiff) between the current and previous averages.
            Update previousAvg to the current average.
        e. If bNum is invalid, exclude it and adjust round count, undo the effect of this unsuccessful round.
        Return the previousAvg once the loop exits.

        Parameters
        ----------
        startActor : str
            The actor for whom the average Bacon number is to be calculated.
        threshold : float
            The convergence threshold for the average calculation.

        Returns
        -------
        float
            The converged average Bacon number for the startActor.
        """

        # If the start actor is not in the adjacency list, return -1
        if startActor not in self.adjList:
            return -1

        # Get a list of all actors
        actors = list(self.adjList.keys())
        # Initialize the previous average Bacon number to 0
        previousAvg = 0
        # Initialize the current difference to infinity
        curDiff = float("inf")
        # Initialize the total Bacon number to 0
        totalBNum = 0
        # Initialize the number of rounds to 0
        rounds = 0

        # While the current difference is greater than the threshold
        while curDiff > threshold:
            # Increment the number of rounds
            rounds += 1
            # Choose a random actor
            actor = random.choice(actors)
            # Calculate the Bacon number from the start actor to the chosen actor
            bNum = self.calcBaconNumber(startActor, actor)[0]

            # If the Bacon number is valid (not -1 and not 0)
            if bNum != -1 and bNum != 0:
                # Add the Bacon number to the total
                totalBNum += bNum
                # Calculate the current average Bacon number
                currentAvg = totalBNum / rounds
                # Calculate the current difference between the current and previous averages
                curDiff = abs(currentAvg - previousAvg)
                # Update the previous average to the current average
                previousAvg = currentAvg
            else:
                # If the Bacon number is invalid, undo the effect of this unsuccessful round
                rounds -= 1

        # Return the previous average Bacon number
        return previousAvg


def main():
    """
    The main function to demonstrate the BaconNumberCalculator class.
    """
    # Create a BaconNumberCalculator object with the specified file
    bnc = BaconNumberCalculator("data/BaconCastFull.txt")

    # Calculate the Bacon number between two actors
    print(bnc.calcBaconNumber("Bacon, Kevin", "Kidman, Nicole"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Bacon, Kevin"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Smith, Will"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Damon, Matt"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Hanks, Tom"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Cruise, Tom"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Pitt, Brad"))
    print(bnc.calcBaconNumber("Bacon, Kevin", "Jolie, Angelina"))

    bnc2 = BaconNumberCalculator("data/Bacon_06.txt")
    print(bnc2.calcBaconNumber("Bacon, Kevin", "Kidman, Nicole"))
    print(bnc2.calcBaconNumber("Sakata, Jeanne", "Tye, Kevin"))


if __name__ == "__main__":
    main()
