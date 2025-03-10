import random
from collections import deque
#si
class EightPuzzle:
    def __init__(self):
        """Inicializa el puzzle solicitando el estado inicial y el estado objetivo."""
        self.grid_size = 3  # Tamaño del tablero 3x3
        self.tiles = self.get_initial_state()
        self.goal_state = self.get_goal_state()
        
        if not self.is_solvable(self.tiles, self.goal_state):
            print("\nEl puzzle no es solucionable. Reinicie el programa con un estado válido.")
            exit()

    def get_initial_state(self):
        """Solicita al usuario el estado inicial del puzzle."""
        while True:
            user_input = input("\nIngrese el estado inicial (ejemplo: 1 2 3 4 5 6 7 8 0): ")
            tiles = self.parse_input(user_input)
            if tiles:
                return tiles
            print("Orden inválido, intente de nuevo.")

    def get_goal_state(self):
        """Solicita al usuario el estado objetivo del puzzle."""
        while True:
            user_input = input("\nIngrese el estado objetivo (ejemplo: 1 2 3 4 5 6 7 8 0): ")
            goal = self.parse_input(user_input)
            if goal:
                return goal
            print("Orden inválido, intente de nuevo.")

    def parse_input(self, user_input):
        """Convierte la entrada del usuario en una lista de números."""
        try:
            nums = list(map(int, user_input.split()))
            if sorted(nums) == list(range(9)):  # Debe contener los números 0-8
                return [num if num != 0 else None for num in nums]  # 0 representa el espacio vacío
        except ValueError:
            pass
        return None

    def is_solvable(self, tiles, goal):
        """Verifica si el puzzle es solucionable."""
        def count_inversions(array):
            nums = [tile for tile in array if tile is not None]
            return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > nums[j])

        return count_inversions(tiles) % 2 == count_inversions(goal) % 2

    def print_board(self, board):
        """Muestra el estado del tablero en la consola."""
        for i in range(self.grid_size):
            row = board[i * self.grid_size:(i + 1) * self.grid_size]
            print(" ".join(str(num) if num is not None else " " for num in row))
        print("\n")

    def solve(self):
        """Resuelve el puzzle automáticamente usando BFS."""
        print("\nResolviendo el puzzle automáticamente...\n")
        solution = self.bfs_solve()
        if solution:
            for step in solution:
                self.print_board(step)
            print(f"Puzzle resuelto en {len(solution)} pasos.")
        else:
            print("No se encontró una solución.")

    def bfs_solve(self):
        """Algoritmo de búsqueda en anchura (BFS) para encontrar la solución."""
        queue = deque([(self.tiles[:], [])])
        visited = set()
        visited.add(tuple(self.tiles))

        while queue:
            current_state, path = queue.popleft()
            if current_state == self.goal_state:
                return path

            empty_index = current_state.index(None)
            empty_row, empty_col = divmod(empty_index, self.grid_size)
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimientos posibles

            for dr, dc in moves:
                new_row, new_col = empty_row + dr, empty_col + dc
                if 0 <= new_row < self.grid_size and 0 <= new_col < self.grid_size:
                    new_index = new_row * self.grid_size + new_col
                    new_state = current_state[:]
                    new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]

                    if tuple(new_state) not in visited:
                        queue.append((new_state, path + [new_state]))
                        visited.add(tuple(new_state))

        return None  # No hay solución

if __name__ == "__main__":
    game = EightPuzzle()
    game.solve()
