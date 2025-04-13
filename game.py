```python
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
        self.requirements = requirements  # Dictionary: {'color': 'red', 'size': 'small', 'symmetry': True}

    def check_fulfillment(self, arrangement):
        """
        Checks if the arrangement fulfills the order requirements.
        """
        for requirement, value in self.requirements.items():
            if requirement == 'color':
                arrangement_colors = set()
                for flower in arrangement:
                    arrangement_colors.add(flower.color)
                if value not in arrangement_colors:
                    return False  # Required color is missing

            elif requirement == 'size':
                arrangement_sizes = set()
                for flower in arrangement:
                    arrangement_sizes.add(flower.size)

                if value not in arrangement_sizes:
                    return False  # Required size is missing
            #Add more requirments here

        return True  # All requirements met

class GameBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def place_flower(self, flower, row, col):
        """
        Places a flower on the board at the specified row and column.
        Handles placement errors.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("Invalid row or column index.")

        if self.grid[row][col] is not None:
            raise ValueError("That spot is already occupied.")

        self.grid[row][col] = flower

    def remove_flower(self, row, col):
        """
        Removes a flower from the board at the specified row and column.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("Invalid row or column index.")

        self.grid[row][col] = None

    def get_arrangement(self):
        """
        Returns a list of flowers in the arrangement.
        """
        arrangement = []
        for row in self.grid:
            for flower in row:
                if flower:
                    arrangement.append(flower)
        return arrangement

    def display_board(self):
        """Displays the game board in the console."""
        for row in self.grid:
            row_str = ""
            for flower in row:
                if flower:
                    row_str += flower.name[0] + " "  # Display first letter of flower name
                else:
                    row_str += "- "
            print(row_str)

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
        self.zen_mode = False  # Added Zen Mode

    def generate_order(self):
        """
        Generates a random order based on available flower attributes.
        """
        possible_colors = set(flower.color for flower in self.available_flowers)
        possible_sizes = set(flower.size for flower in self.available_flowers)

        order_requirements = {}

        if random.random() < 0.5:  # 50% chance to require a color
            order_requirements['color'] = random.choice(list(possible_colors))

        if random.random() < 0.5:  # 50% chance to require a size
            order_requirements['size'] = random.choice(list(possible_sizes))

        self.current_order = Order(order_requirements)

    def start_game(self):
        """
        Main game loop.
        """
        print("Welcome to Bloom Burst!")
        self.zen_mode = input("Play in Zen mode (y/n)? ").lower() == 'y' # Added Zen Mode selection
        self.generate_order()

        while True:
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

            print("\n--- Actions ---")
            print("1. Place Flower")
            print("2. Remove Flower")
            print("3. Check Order")
            print("4. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == '1':
                    flower_index = int(input("Enter flower number to place: ")) - 1
                    row = int(input("Enter row (0-{}): ".format(self.board.rows - 1)))
                    col = int(input("Enter column (0-{}): ".format(self.board.cols - 1)))

                    flower = self.available_flowers[flower_index]
                    self.board.place_flower(flower, row, col)

                elif choice == '2':
                    row = int(input("Enter row to remove flower from (0-{}): ".format(self.board.rows - 1)))
                    col = int(input("Enter column to remove flower from (0-{}): ".format(self.board.cols - 1)))
                    self.board.remove_flower(row, col)

                elif choice == '3':
                    arrangement = self.board.get_arrangement()
                    if self.current_order.check_fulfillment(arrangement):
                        print("Congratulations! You fulfilled the order!")
                        self.score += 100  # Award points
                        print(f"Score: {self.score}")
                        self.generate_order() # Generate new order
                    else:
                        print("The arrangement does not meet the requirements.")
                        if not self.zen_mode: # Added Zen Mode check
                            print("Game Over")
                            return

                elif choice == '4':
                    print("Thanks for playing Bloom Burst!")
                    break
                else:
                    print("Invalid choice. Please try again.")

            except ValueError as e:
                print(f"Error: {e}")
            except IndexError:
                print("Invalid flower index.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    game = BloomBurstGame()
    game.start_game()
```