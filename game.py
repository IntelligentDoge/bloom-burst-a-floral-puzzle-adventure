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

class GameBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def place_flower(self, flower, row, col):
        """Places a flower on the board, handling errors."""
        self._validate_coordinates(row, col)
        if self.grid[row][col] is not None:
            raise ValueError("That spot is already occupied.")
        self.grid[row][col] = flower

    def remove_flower(self, row, col):
        """Removes a flower from the board, handling errors."""
        self._validate_coordinates(row, col)
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
        self.available_flowers = [
            Flower("Rose", "red", "small"),
            Flower("Tulip", "yellow", "medium"),
            Flower("Daisy", "white", "small"),
            Flower("Sunflower", "yellow", "large"),
            Flower("Lavender", "purple", "small")
        ]
        self.current_order = None
        self.score = 0
        self.zen_mode = False
        self.possible_colors = set(flower.color for flower in self.available_flowers)
        self.possible_sizes = set(flower.size for flower in self.available_flowers)
        self.attributes = {'color': self.possible_colors, 'size': self.possible_sizes}

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

        while True:
            self.display_game_state()

            choice = self.get_player_choice()

            if choice == '1':
                self.place_flower_action()
            elif choice == '2':
                self.remove_flower_action()
            elif choice == '3':
                self.check_order_action()
            elif choice == '4':
                print("Thanks for playing Bloom Burst!")
                break
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
        if self.current_order.requirements:
            for req, val in self.current_order.requirements.items():
                print(f"- Must have {req}: {val}")
        else:
            print("- No specific requirements. Create a beautiful arrangement!")

        print("\n--- Available Flowers ---")
        for i, flower in enumerate(self.available_flowers):
            print(f"{i + 1}. {flower}")

        print("\n--- Current Arrangement ---")
        self.board.display_board()

    def get_player_choice(self):
        """Gets the player's choice of action."""
        print("\n--- Actions ---")
        print("1. Place Flower")
        print("2. Remove Flower")
        print("3. Check Order")
        print("4. Exit")
        return input("Enter your choice: ")

    def place_flower_action(self):
        """Handles the action of placing a flower on the board."""
        try:
            flower_index = int(input("Enter flower number to place: ")) - 1
            if not (0 <= flower_index < len(self.available_flowers)):
                raise IndexError("Invalid flower index.")

            row = int(input("Enter row (0-{}): ".format(self.board.rows - 1)))
            col = int(input("Enter column (0-{}): ".format(self.board.cols - 1)))

            flower = self.available_flowers[flower_index]
            self.board.place_flower(flower, row, col)
        except ValueError as e:
            print(f"Error: Invalid input - {e}")
        except IndexError:
            print("Error: Invalid flower index.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def remove_flower_action(self):
        """Handles the action of removing a flower from the board."""
        try:
            row = int(input("Enter row to remove flower from (0-{}): ".format(self.board.rows - 1)))
            col = int(input("Enter column to remove flower from (0-{}): ".format(self.board.cols - 1)))
            self.board.remove_flower(row, col)
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
                return

if __name__ == "__main__":
    game = BloomBurstGame()
    game.start_game()