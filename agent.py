# agent.py
import math
import random
import heapq


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

    def __init__(self, active_algo='AStar'):
        self.active_algo = active_algo
        self.plan = []

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

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type="manhattan"):
        """
        A* search algorithm to find the shortest path from start_pos to goal_pos.

        Args:
            start_pos: Tuple (x, y) representing the starting position
            goal_pos: Tuple (x, y) representing the goal position
            walls: List of tuples representing wall positions
            grid_size: Tuple (width, height) representing the grid dimensions
            heuristic_type: String "manhattan" or "euclidean" for heuristic choice

        Returns:
            List of action strings ['Up', 'Down', 'Left', 'Right'] or empty list if no path
        """
        # Choose heuristic function
        if heuristic_type == "manhattan":
            heuristic = self.manhattan_distance
        else:
            heuristic = self.euclidean_distance

        # Initialize priority queue and reached states
        priority_queue = []
        reached_states = set()

        # Convert walls to set for O(1) lookup
        walls_set = set(walls)

        # Calculate initial h(n) and f(n)
        h_start = heuristic(start_pos, goal_pos)
        f_start = 0 + h_start  # g(n) = 0 for start

        # Push initial state: (f_cost, g_cost, current_pos, path_taken)
        heapq.heappush(priority_queue, (f_start, 0, start_pos, []))

        # Direction mappings
        directions = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }

        # Process queue
        while priority_queue:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(priority_queue)

            # Check if goal is reached
            if current_pos == goal_pos:
                return path_taken

            # Mark as reached
            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)

            # Expand neighbors
            for action, (dx, dy) in directions.items():
                neighbor_pos = (current_pos[0] + dx, current_pos[1] + dy)

                # Check if neighbor is valid
                x, y = neighbor_pos
                if (0 <= x < grid_size[0] and
                        0 <= y < grid_size[1] and
                        neighbor_pos not in walls_set and
                        neighbor_pos not in reached_states):
                    # Calculate costs for neighbor
                    g_new = g_cost + 1
                    h_new = heuristic(neighbor_pos, goal_pos)
                    f_new = g_new + h_new

                    # Push new state to queue
                    new_path = path_taken + [action]
                    heapq.heappush(priority_queue, (f_new, g_new, neighbor_pos, new_path))

        # No path found
        return []

    def sense_and_act(self, percept: dict) -> str:
        """
        Perceives the environment and decides the next action.
        Uses A* search to find the path to the closest food.
        """
        current_pos = tuple(percept['agent_pos'])
        remaining_food = percept['remaining_food']

        # If no food left, do nothing
        if remaining_food == 0:
            return 'Stay'

        # Check if we need to plan a new path
        if not self.plan:
            # Extract grid information from percept
            walls = percept.get('walls', [])
            grid_size = percept.get('grid_size', (10, 10))
            food_positions = percept.get('food_positions', set())

            if food_positions:
                # Find closest food as goal
                goal_pos = min(food_positions, key=lambda f: self.manhattan_distance(current_pos, f))

                # Call A* search based on active algorithm
                if self.active_algo == 'AStar':
                    self.plan = self.astar_search(current_pos, goal_pos, walls, grid_size, heuristic_type="manhattan")

        # Execute the plan
        if self.plan:
            action = self.plan.pop(0)
            return action

        return random.choice(['Up', 'Down', 'Left', 'Right'])


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