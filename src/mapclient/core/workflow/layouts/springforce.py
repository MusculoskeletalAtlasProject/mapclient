from itertools import combinations
import random
from typing import List, Dict, FrozenSet
from abc import ABC, abstractmethod
import math

from cmlibs.maths.vectorops import magnitude, sub


def _calc_theta(dist_x, dist_y):
    if dist_x == 0 and dist_y > 0:
        theta = math.pi / 2
    elif dist_x == 0 and dist_y < 0:
        theta = - math.pi / 2
    else:
        theta = math.atan2(dist_y, dist_x)

    return theta


class Node:
    __slots__ = ['_adjacent', '_non_adjacent', 'datapoint', 'x', 'y', 'vx', 'vy']

    def __init__(self, x, y, vx: float = 0.0, vy: float = 0.0) -> None:
        self._adjacent = []
        self._non_adjacent = []
        self.datapoint = [x, y]
        self.vx = vx
        self.vy = vy

    def add_adjacent(self, node):
        self._adjacent.append(node)

    def add_non_adjacent(self, node):
        self._non_adjacent.append(node)

    def set_velocity(self, c1, c2, c3, c4):
        total_force_x = 0
        total_force_y = 0

        for edge in self._adjacent:
            dist_x = self.datapoint[0] - edge.datapoint[0]
            dist_y = self.datapoint[1] - edge.datapoint[1]
            dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
            dist = dist if dist else jiggle()
            dist = max(dist, 0.001)
            force = -c1 * math.log(dist / c2)
            theta = _calc_theta(dist_x, dist_y)
            total_force_x += force * math.cos(theta)
            total_force_y += force * math.sin(theta)

        part_sqrt_c3 = 0.06 * math.sqrt(c3)
        for non_edge in self._non_adjacent:
            dist_x = self.datapoint[0] - non_edge.datapoint[0]
            dist_y = self.datapoint[1] - non_edge.datapoint[1]
            dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
            dist = max(dist, random.uniform(0.92 * part_sqrt_c3, 1.08 * part_sqrt_c3))
            force = c3 / dist ** 2
            theta = _calc_theta(dist_x, dist_y)
            total_force_x += force * math.cos(theta)
            total_force_y += force * math.sin(theta)

        self.vx = c4 * total_force_x
        self.vy = c4 * total_force_y

    def add_velocity(self, vx: float, vy: float) -> None:
        self.vx += vx
        self.vy += vy

    def apply_velocity(self) -> None:
        self.datapoint[0] += self.vx
        self.datapoint[1] += self.vy
        self.clear_velocity()

    def clear_velocity(self) -> None:
        self.vx = 0.0
        self.vy = 0.0

    def __str__(self) -> str:
        return f'Node<{self.datapoint}>({self.datapoint[0]} + {self.vx}, {self.datapoint[1]} + {self.vy})'

    def __repr__(self) -> str:
        return f'Node<{self.datapoint}>'


def mean(lst: List[float]) -> float:
    return sum(lst) / len(lst)


def euclidean(v1, v2) -> float:
    return math.sqrt(magnitude(sub(v2, v1)))


def jiggle() -> float:
    """
    Return a random small non zero number
    """
    small_non_zero = (random.random() - 0.5) * 1e-6
    while small_non_zero == 0:
        small_non_zero = (random.random() - 0.5) * 1e-6
    return small_non_zero


def _build_nodes(dataset) -> List[Node]:
    """
    Construct a Node for each datapoint.
    """
    nodes = [Node(v.getPos().x(), v.getPos().y()) for v in dataset['vertices']]
    for index, node in enumerate(nodes):
        current_vertex = dataset['vertices'][index]
        for v in dataset['adjacent'][current_vertex]:
            v_index = dataset['vertices'].index(v)
            node.add_adjacent(nodes[v_index])
        for v in dataset['non_adjacent'][current_vertex]:
            v_index = dataset['vertices'].index(v)
            node.add_non_adjacent(nodes[v_index])

    return nodes


class BaseSpringLayout(ABC):
    """
    Base class for a spring layout algorithm
    """

    def __init__(self, dataset=None, nodes: List[Node] = None,
                 distance_fn=euclidean,
                 iterations: int = 50, target_node_speed: float = 0.0,
                 enable_cache: bool = True) -> None:
        assert iterations >= 0, "iterations must be non-negative"
        assert dataset is not None or nodes is not None, "must provide either dataset or nodes"

        self.nodes: List[Node] = nodes if nodes is not None else _build_nodes(dataset)
        self.iterations: int = iterations
        self.data_size_factor: float = 1
        self.optimal_distance_between = 1
        self._i: int = 0  # current iteration
        self.distance_fn = distance_fn
        self._average_speeds: List[float] = list()
        self.target_node_speed: float = target_node_speed
        self.enable_cache: bool = enable_cache
        if enable_cache:
            self.distances: Dict[FrozenSet[Node], float] = dict()
        else:
            # Change the distance function
            self.distance = self.distance_no_cache

    def current_iteration(self) -> int:
        return self._i

    def get_positions(self):
        return [n.datapoint for n in self.nodes]

    def set_positions(self, positions) -> None:
        for pos, node in zip(positions, self.nodes):
            node.datapoint = pos

    def get_stress(self) -> float:
        distance_diff: float = 0.0
        actual_distance: float = 0.0
        for source, target in combinations(self.nodes, 2):
            high_d_distance = self.distance(source, target, cache=False)
            low_d_distance = math.sqrt((target.x - source.x) ** 2 + (target.y - source.y) ** 2)
            distance_diff += (high_d_distance - low_d_distance) ** 2
            actual_distance += low_d_distance ** 2
        if actual_distance == 0:
            return math.inf
        return math.sqrt(distance_diff / actual_distance)

    def average_speed(self) -> float:
        """ Return the 5-running mean of the average node speeds """
        return mean(self._average_speeds[-5:]) if len(self._average_speeds) > 0 else math.inf

    def spring_layout(self, c1=2.0, c2=1.0, c3=1.0, c4=0.1, return_after: int = None):
        """
        Method to perform the main spring layout calculation, move the nodes up-to iterations
        number of times unless return_after is given.
        If return_after is specified then the nodes will be moved the value of return_after
        times. Subsequent calls to spring_layout will continue from the previous number of
        iterations.
        """
        if return_after is not None and self.average_speed() > self.target_node_speed:
            for i in range(return_after):
                self._spring_layout(c1, c2, c3, c4)
                self._i += 1
        else:
            while self.average_speed() > self.target_node_speed and self._i < self.iterations:
                self._spring_layout(c1, c2, c3, c4)
                self._i += 1

        # Return calculated positions for datapoints
        return self.get_positions()

    def distance_no_cache(self, source: Node, target: Node, cache: bool = False) -> float:
        """ Distance function to use when self.disable_cache = True """
        return self.distance_fn(source.datapoint, target.datapoint)

    def distance(self, source: Node, target: Node, cache: bool = False) -> float:
        """
        Returns the high dimensional distance between two nodes at source and target
        index using self.distance_fn
        """
        pair = frozenset({source, target})
        if pair in self.distances:
            return self.distances[pair]
        distance = self.distance_fn(source.datapoint, target.datapoint)
        if cache:
            self.distances[pair] = distance
        return distance

    @abstractmethod
    def _spring_layout(self, c1, c2, c3, c4) -> None:
        """
        Perform one iteration of the spring layout
        """
        pass

    def _force(self, current_distance, real_distance, alpha: float = 1) -> float:
        return (current_distance - real_distance) * alpha * self.data_size_factor / current_distance

    def _apply_velocities(self) -> None:
        """
        Apply the current velocity of each node to its position
        and reset velocity
        """
        total = 0.0
        for node in self.nodes:
            total += math.hypot(node.vx, node.vy)
            node.apply_velocity()
        total /= len(self.nodes)
        self._average_speeds.append(total)


class SpringForce(BaseSpringLayout):
    """
    Basic brute force spring layout implementation
    """

    def __init__(self, dataset,
                 distance_fn=euclidean,
                 iterations: int = 50, target_node_speed: float = 0.0,
                 enable_cache: bool = False) -> None:
        super().__init__(dataset=dataset, distance_fn=distance_fn, iterations=iterations,
                         target_node_speed=target_node_speed, enable_cache=enable_cache)

    def _spring_layout(self, c1, c2, c3, c4) -> None:
        # Calculate velocities
        for index, node in enumerate(self.nodes):
            # print('node:', index, node.datapoint)
            node.set_velocity(c1, c2, c3, c4)

        # Apply velocities
        self._apply_velocities()
