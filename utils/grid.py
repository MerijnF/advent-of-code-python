import heapq
from typing import Generator, Generic, Literal, Callable, TypeVar
import copy

T = TypeVar("T")

Directions = Literal["N", "E", "S", "W"]

DIRECTIONS: list[Directions] = ["N", "E", "S", "W"]
DIRECTION_VECTORS: dict[Directions, tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}


class Grid(Generic[T]):
    data: list[list[T]]

    def __init__(self, data: list[list[T]], orientation: Literal["XY", "YX"] = "YX"):

        self.orientation = orientation
        if orientation == "YX":
            self.width = len(data[0])
            self.height = len(data)
            self.data = data
        else:
            self.width = len(data)
            self.height = len(data[0])
            self.data = [
                [data[x][y] for y in range(self.height)] for x in range(self.width)
            ]

    def get(self, x: int, y: int) -> T:
        return self.data[y][x]

    def set(self, x: int, y: int, value: T) -> None:
        self.data[y][x] = value

    def find(self, value: T) -> list[tuple[int, int]]:
        result = []
        for x, y, val in self.iterate():
            if val == value:
                result.append((x, y))
        return result

    def find_first(self, value: T) -> tuple[int, int] | None:
        for x, y, val in self.iterate():
            if val == value:
                return (x, y)
        return None

    def iterate(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self.get(x, y)

    def in_bounds(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def print(self):
        for y_line in self.data:
            for val in y_line:
                print(val, end="")
            print()

    def deepcopy(self):
        return Grid(copy.deepcopy(self.data), self.orientation)


class GridPathfinder(Generic[T]):
    def __init__(
        self,
        grid: Grid[T],
        walkable: Callable[[T], bool],
        start: tuple[int, int] = (-1, -1),
        end: tuple[int, int] = (-1, -1),
    ):
        self.grid = grid
        self.start = start
        self.end = end
        self.walkable = walkable

    def find_shortest_dist(self) -> int | None:
        to_visit: list[tuple[tuple[int, int], int]] = []
        visited: dict[tuple[int, int], int] = {}

        visited[self.start] = 0

        heapq.heapify(to_visit)
        heapq.heappush(to_visit, (self.start, 0))

        while to_visit:
            pos, dist = heapq.heappop(to_visit)

            for direction in DIRECTIONS:
                next_pos = (
                    pos[0] + DIRECTION_VECTORS[direction][0],
                    pos[1] + DIRECTION_VECTORS[direction][1],
                )
                if not self.grid.in_bounds(*next_pos):
                    continue

                if not self.walkable(self.grid.get(*next_pos)):
                    continue

                new_dist = dist + 1

                if next_pos in visited and visited[next_pos] <= new_dist:
                    continue

                visited[(next_pos)] = new_dist
                heapq.heappush(to_visit, (next_pos, dist + 1))

        return visited.get(self.end, None)

    def find_start(self, start: T):
        found = self.grid.find_first(start)
        if found is not None:
            self.start = found

    def find_end(self, end: T):
        found = self.grid.find_first(end)
        if found is not None:
            self.end = found


class GridStepper(Generic[T]):

    on_collision: Callable[
        [int, int, int, int, Literal["U", "D", "L", "R"]],
        tuple[int, int, Literal["U", "D", "L", "R"]],
    ] = lambda x, y, prev_x, prev_y, direction: (prev_x, prev_y, direction)

    def __init__(
        self,
        grid: Grid[T],
        start: tuple[int, int] = (-1, -1),
        direction: Literal["U", "D", "L", "R"] = "U",
    ):
        self.grid = grid
        self.create_visited_mask()
        self.create_collision_mask()
        self.x, self.y = start
        self.direction = direction

    def find_start(self, start: T):
        found = self.grid.find_first(start)
        if found is not None:
            self.x, self.y = found
            self.visited_mask.set(self.x, self.y, (True, [self.direction]))

    def fill_collision_mask(self, walkable: Callable[[T], bool]):
        for x, y, val in self.grid.iterate():
            if not walkable(val):
                self.collision_mask.set(x, y, True)

    def create_collision_mask(self):
        self.collision_mask = Grid(
            [[False for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        )

    def create_visited_mask(self) -> None:
        self.visited_mask: Grid[tuple[bool, list[Literal["U", "D", "L", "R"]]]] = Grid(
            [
                [(False, []) for _ in range(self.grid.width)]
                for _ in range(self.grid.height)
            ]
        )

    def step(self) -> Literal["OUT-OF-BOUNDS", "LOOP", "COLLISION", "OK"]:
        match self.direction:
            case "U":
                next_x, next_y = self.x, self.y - 1
            case "D":
                next_x, next_y = self.x, self.y + 1
            case "L":
                next_x, next_y = self.x - 1, self.y
            case "R":
                next_x, next_y = self.x + 1, self.y

        if not self.grid.in_bounds(next_x, next_y):
            return "OUT-OF-BOUNDS"

        result: Literal["OUT-OF-BOUNDS", "LOOP", "COLLISION", "OK"] = "OK"

        if self.collision_mask.get(next_x, next_y):
            next_x, next_y, self.direction = self.on_collision(
                next_x, next_y, self.x, self.y, self.direction
            )
            result = "COLLISION"

        self.x = next_x
        self.y = next_y
        visited = self.visited_mask.get(self.x, self.y)
        if self.direction in visited[1]:
            return "LOOP"

        self.visited_mask.set(self.x, self.y, (True, visited[1] + [self.direction]))

        return result

    def step_until(
        self, until: list[Literal["OUT-OF-BOUNDS", "LOOP", "COLLISION", "OK"]]
    ):
        while True:
            result = self.step()
            if result in until:
                return result

    def visited(self) -> Generator[tuple[int, int]]:
        for x, y, val in self.visited_mask.iterate():
            visited, _ = val
            if visited:
                yield (x, y)
