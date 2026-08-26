# agent.py
from collections import deque
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
    """An agent that uses various search algorithms (BFS, DFS, UCS) to find optimal paths."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
        self.plan = []
        self.active_algo = 'DFS'

    def bfs_search(self, start, goal, grid_width, grid_height, walls):
        """
        Breadth-First Search (BFS) - explores shallowest nodes first using FIFO queue.
        """
        frontier = deque([(start, [])])
        reached = {tuple(start)}

        while frontier:
            node, path = frontier.popleft()

            if node == goal:
                return path

            for action in self.actions_pool:
                new_node = list(node)

                if action == 'Up':
                    new_node[1] = min(grid_height - 1, new_node[1] + 1)
                elif action == 'Down':
                    new_node[1] = max(0, new_node[1] - 1)
                elif action == 'Left':
                    new_node[0] = max(0, new_node[0] - 1)
                elif action == 'Right':
                    new_node[0] = min(grid_width - 1, new_node[0] + 1)

                new_node_tuple = tuple(new_node)

                if new_node_tuple not in reached and new_node_tuple not in walls:
                    reached.add(new_node_tuple)
                    frontier.append((new_node, path + [action]))

        return []

    def dfs_search(self, start, goal, grid_width, grid_height, walls):
        """
        Depth-First Search (DFS) - explores deepest nodes first using LIFO stack.
        """
        frontier = [(start, [])]
        reached = {tuple(start)}

        while frontier:
            node, path = frontier.pop()

            if node == goal:
                return path

            for action in self.actions_pool:
                new_node = list(node)

                if action == 'Up':
                    new_node[1] = min(grid_height - 1, new_node[1] + 1)
                elif action == 'Down':
                    new_node[1] = max(0, new_node[1] - 1)
                elif action == 'Left':
                    new_node[0] = max(0, new_node[0] - 1)
                elif action == 'Right':
                    new_node[0] = min(grid_width - 1, new_node[0] + 1)

                new_node_tuple = tuple(new_node)

                if new_node_tuple not in reached and new_node_tuple not in walls:
                    reached.add(new_node_tuple)
                    frontier.append((new_node, path + [action]))

        return []

    def ucs_search(self, start, goal, grid_width, grid_height, walls):
        """
        Uniform Cost Search (UCS) - explores nodes ordered by total path cost g(n) using Priority Queue.
        """
        frontier = [(0, start, [])]
        reached = {tuple(start): 0}

        while frontier:
            cost, node, path = heapq.heappop(frontier)

            if node == goal:
                return path

            if cost > reached.get(tuple(node), float('inf')):
                continue

            for action in self.actions_pool:
                new_node = list(node)

                if action == 'Up':
                    new_node[1] = min(grid_height - 1, new_node[1] + 1)
                elif action == 'Down':
                    new_node[1] = max(0, new_node[1] - 1)
                elif action == 'Left':
                    new_node[0] = max(0, new_node[0] - 1)
                elif action == 'Right':
                    new_node[0] = min(grid_width - 1, new_node[0] + 1)

                new_node_tuple = tuple(new_node)
                new_cost = cost + 1

                if new_node_tuple not in walls and new_cost < reached.get(new_node_tuple, float('inf')):
                    reached[new_node_tuple] = new_cost
                    heapq.heappush(frontier, (new_cost, new_node, path + [action]))

                def find_closest_food(self, agent_pos, food_list):
                    """Find the closest food pellet from the list."""
                    if not food_list:
                        return None

                    closest = None
                    min_distance = float('inf')

                    for food in food_list:
                        distance = abs(agent_pos[0] - food[0]) + abs(agent_pos[1] - food[1])
                        if distance < min_distance:
                            min_distance = distance
                            closest = food

                    return closest

                def sense_and_act(self, percept: dict) -> str:
                    """Execute plan step-by-step. If plan is empty, create a new plan to nearest food."""
                    if not self.plan:
                        agent_pos = percept['agent_pos']
                        food_list = percept.get('all_food', [])

                        if food_list:
                            closest_food = self.find_closest_food(agent_pos, food_list)

                            if closest_food:
                                walls = set(tuple(w) for w in percept.get('walls', []))
                                grid_size = percept.get('grid_size', (4, 4))

                                if self.active_algo == 'BFS':
                                    self.plan = self.bfs_search(agent_pos, closest_food, grid_size[0], grid_size[1],
                                                                walls)
                                elif self.active_algo == 'DFS':
                                    self.plan = self.dfs_search(agent_pos, closest_food, grid_size[0], grid_size[1],
                                                                walls)
                                elif self.active_algo == 'UCS':
                                    self.plan = self.ucs_search(agent_pos, closest_food, grid_size[0], grid_size[1],
                                                                walls)

                    if self.plan:
                        return self.plan.pop(0)
                    else:
                        return 'Up'

        return []