# agent.py
import math
import random
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)


class SearchAgent:
    """An agent that solves problems using search algorithms."""

    def manhattan_distance(self, pos, goal):
        """
        Calculates Manhattan distance (taxicab distance) between two positions.
        Formula: h(n) = |x_1 - x_2| + |y_1 - y_2|
        """
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """
        Calculates Euclidean distance (straight-line distance) between two positions.
        Formula: h(n) = sqrt((x_1 - x_2)^2 + (y_1 - y_2)^2)
        """
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)


# Testing Checkpoint
if __name__ == "__main__":
    agent = SearchAgent()
    start = (0, 0)
    goal = (3, 4)

    manhattan = agent.manhattan_distance(start, goal)
    euclidean = agent.euclidean_distance(start, goal)

    print(f"Manhattan distance from {start} to {goal}: {manhattan}")
    print(f"Euclidean distance from {start} to {goal}: {euclidean}")
    print(f"\nExpected: Manhattan = 7, Euclidean = 5.0")
    print(f"Actual: Manhattan = {manhattan}, Euclidean = {euclidean}")