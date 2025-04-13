import random

class Flower:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

    def __str__(self):
        return f"{self.name} ({self.color}, {self.size})"

class Order:
    def __init__(self, requirements):
        self.requirements = requirements

    def check_fulfillment(self, arrangement):
        """Checks if the arrangement fulfills the order requirements."""
        for requirement, value in self.requirements.items():
            arrangement_values = set(getattr(flower, requirement) for flower in arrangement)
            if value not in arrangement_values:
                return False
        return True

    def describe(self):
        if self.requirements:
            description = "\n".join(f"- Must have {req}: {val}" for req, val in self.requirements.items())
            return description
        else:
            return "- No specific requirements. Create a beautiful arrangement!"


class GameBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def place_flower(self, flower, row, col):
        """Places a flower on the board, handling errors."""
        self._validate_coordinates(row, col)
        if self.grid[row][col] is not None:
            raise ValueError(f"That spot is already occupied by a {self.grid[row][col].name}")
        self.grid[row][col] = flower

    def remove_flower(self, row, col):
        """Removes a flower from the board, handling errors."""
        self._validate_coordinates(row, col)
        if self.grid[row][col] is None:
            raise ValueError("There is no flower at this spot.")
        self.grid[row][col] = None

    def get_arrangement(self):
        """Returns a list of flowers in the arrangement."""
        return [flower for row in self.grid for flower in row if flower]

    def display_board(self):
        """Displays the game board in the console."""
        header = "  " + " ".join(str(i) for i in range(self.cols))
        print(header)
        for i, row in enumerate(self.grid):
            row_str = f"{i} "
            for flower in row:
                if flower:
                    row_str += flower.name[0] + " "
                else:
                    row_str += "- "
            print(row_str)

    def _validate_coordinates(self, row, col):
        """Validates row and column indices."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("Invalid row or column index.")


class BloomBurstGame:
    def __init__(self, rows=5, cols=5):
        self.board = GameBoard(rows, cols)
        self.available_flowers = {
            1: Flower("Rose", "red", "small"),
            2: Flower("Tulip", "yellow", "medium"),
            3: Flower("Daisy", "white", "small"),
            4: Flower("Sunflower", "yellow", "large"),
            5: Flower("Lavender", "purple", "small")
        }
        self.current_order = None
        self.score = 0
        self.zen_mode = False
        self.possible_colors = set(flower.color for flower in self.available_flowers.values())
        self.possible_sizes = set(flower.size for flower in self.available_flowers.values())
        self.attributes = {'color': self.possible_colors, 'size': self.possible_sizes}
        self.game_over = False
        self.rows = rows
        self.cols = cols

    def generate_order(self):
        """Generates a random order based on available flower attributes."""
        order_requirements = {}
        num_requirements = random.randint(0, len(self.attributes))  # Random number of requirements
        selected_attributes = random.sample(list(self.attributes.keys()), num_requirements)

        for attr in selected_attributes:
            order_requirements[attr] = random.choice(list(self.attributes[attr]))

        self.current_order = Order(order_requirements)

    def start_game(self):
        """Main game loop."""
        print("Welcome to Bloom Burst!")
        self.zen_mode = self.get_zen_mode_preference()
        self.generate_order()

        while not self.game_over:
            self.display_game_state()

            choice = self.get_player_choice()

            if choice == '1':
                self.place_flower_action()
            elif choice == '2':
                self.remove_flower_action()
            elif choice == '3':
                self.check_order_action()
            elif choice == '4':
                self.show_instructions()
            elif choice == '5':
                self.exit_game()
            else:
                print("Invalid choice. Please try again.")

    def get_zen_mode_preference(self):
        """Asks the player if they want to play in Zen mode."""
        while True:
            zen_mode = input("Play in Zen mode (y/n)? ").lower()
            if zen_mode in ('y', 'n'):
                return zen_mode == 'y'
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def display_game_state(self):
        """Displays the current game state to the player."""
        print("\n--- Current Order ---")
        print(self.current_order.describe())

        print("\n--- Available Flowers ---")
        for i, flower in self.available_flowers.items():
            print(f"{i}. {flower}")

        print("\n--- Current Arrangement ---")
        self.board.display_board()
        print(f"Score: {self.score}")

    def get_player_choice(self):
        """Gets the player's choice of action."""
        print("\n--- Actions ---")
        print("1. Place Flower")
        print("2. Remove Flower")
        print("3. Check Order")
        print("4. Instructions")
        print("5. Exit")
        return input("Enter your choice: ")

    def place_flower_action(self):
        """Handles the action of placing a flower on the board."""
        while True:
            try:
                flower_index = int(input("Enter flower number to place: "))
                if flower_index not in self.available_flowers:
                    print("Invalid flower number.")
                    continue

                row = int(input(f"Enter row (0-{self.rows - 1}): "))
                col = int(input(f"Enter column (0-{self.cols - 1}): "))

                flower = self.available_flowers[flower_index]
                self.board.place_flower(flower, row, col)
                print(f"Placed {flower.name} at ({row}, {col}).")
                break

            except ValueError as e:
                print(f"Error: Invalid input - {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def remove_flower_action(self):
        """Handles the action of removing a flower from the board."""
        while True:
            try:
                row = int(input(f"Enter row to remove flower from (0-{self.rows - 1}): "))
                col = int(input(f"Enter column to remove flower from (0-{self.cols - 1}): "))
                self.board.remove_flower(row, col)
                print(f"Removed flower from ({row}, {col}).")
                break

            except ValueError as e:
                print(f"Error: Invalid input - {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def check_order_action(self):
        """Handles the action of checking the order fulfillment."""
        arrangement = self.board.get_arrangement()
        if self.current_order.check_fulfillment(arrangement):
            print("Congratulations! You fulfilled the order!")
            self.score += 100  # Award points
            print(f"Score: {self.score}")
            self.generate_order()  # Generate new order
        else:
            print("The arrangement does not meet the requirements.")
            if not self.zen_mode:  # Added Zen Mode check
                print("Game Over")
                self.game_over = True

    def show_instructions(self):
        print("\n--- Instructions ---")
        print("Bloom Burst is a game where you create flower arrangements to fulfill orders.")
        print("Place flowers on the board according to the order requirements.")
        print("Available actions:")
        print("  1. Place Flower: Choose a flower and a location to place it on the board.")
        print("  2. Remove Flower: Remove a flower from the board.")
        print("  3. Check Order: Check if your arrangement fulfills the current order.")
        print("  4. Exit: Quit the game.")
        print("Fulfilling orders earns you points. The game ends if you fail an order in normal mode.")
        print("In Zen mode, you can continue playing even if you fail an order.")

    def exit_game(self):
        print("Thanks for playing Bloom Burst!")
        self.game_over = True


if __name__ == "__main__":
    game = BloomBurstGame()
    game.start_game()