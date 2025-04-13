import random

class Level4:
    """
    Represents Level 4: Sunset Serenade in Bloom Burst.  This level introduces
    Creepers as obstacles and the Pruning Shears tool.  The goal is to fulfill
    an arrangement order while managing Creeper growth and adhering to color
    harmony (Golden Ratio) and symmetry rules.
    """

    def __init__(self):
        self.grid_size = (7, 7)
        self.grid = [['.' for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        self.creeper_start_locations = [(1, 1), (5, 5)]  # Coordinates (row, col)
        self.pre_placed_sunflower = (3, 3)
        self.grid[self.pre_placed_sunflower[0]][self.pre_placed_sunflower[1]] = '#'  # '#' represents a sunflower
        self.sunflower_count_required = 8
        self.lavender_count_required = 6
        self.crimson_rose_count_required = 4
        self.max_creeper_coverage = 10
        self.pruning_shears_available = 3
        self.pruning_shears_used = 0
        self.creeper_coverage = 0
        self.golden_ratio_score = 0 # Percentage of grid following the golden ratio
        self.symmetry_score = 0 # Percentage of grid demonstrating symmetry

        # Flower Availability (Flower objects, potentially with bloom radius data)
        self.available_flowers = {
            "Sunflower": {"count": float('inf'), "bloom_radius": 1},  # Unlimited sunflowers
            "Lavender": {"count": float('inf'), "bloom_radius": 0.5}, # Unlimited lavender
            "Crimson Rose": {"count": float('inf'), "bloom_radius": 1},  # Unlimited roses
            "White Lily": {"count": 3, "bloom_radius": 2}  # Limited lilies
        }

        self.creeper_growth_rate = 0.05  # Probability of a creeper spreading on any turn
        self.game_over = False
        self.message = ""


    def display_grid(self):
        """Prints the current state of the grid to the console (for debugging/CLI)."""
        for row in self.grid:
            print(" ".join(row))


    def place_flower(self, row, col, flower_type):
        """
        Places a flower of the specified type at the given coordinates.
        Handles flower availability and errors.
        """
        if self.game_over:
            self.message = "The game is over.  You cannot place any more flowers."
            return False

        if not (0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]):
            self.message = "Invalid flower placement: Coordinates are out of bounds."
            return False

        if self.grid[row][col] != '.':
            self.message = "Invalid flower placement:  There is already a flower or creeper at that location."
            return False

        if flower_type not in self.available_flowers:
            self.message = f"Invalid flower type: {flower_type} is not available in this level."
            return False

        if self.available_flowers[flower_type]["count"] <= 0 and self.available_flowers[flower_type]["count"] != float('inf'):  #Use count != inf to check for infinite flower availabilty
            self.message = f"Insufficient {flower_type}:  You have no more {flower_type} flowers available."
            return False

        self.grid[row][col] = flower_type[0].upper() # Use first letter as symbol (S, L, C, W)
        if self.available_flowers[flower_type]["count"] != float('inf'): #Decrease count if the flower is limited
            self.available_flowers[flower_type]["count"] -= 1

        self.message = f"{flower_type} placed successfully at ({row}, {col})."
        return True



    def use_pruning_shears(self, row, col):
        """
        Uses the pruning shears to clear Creepers from a 2x2 area.
        Handles usage limits and errors.
        """
        if self.game_over:
            self.message = "The game is over.  You cannot use pruning shears."
            return False

        if self.pruning_shears_used >= self.pruning_shears_available:
            self.message = "You have no more pruning shears available."
            return False

        if not (0 <= row <= self.grid_size[0] - 2 and 0 <= col <= self.grid_size[1] - 2):
             self.message = "Invalid Pruning Shears location:  2x2 area would extend beyond the grid."
             return False

        self.pruning_shears_used += 1

        for r in range(row, row + 2):
            for c in range(col, col + 2):
                if self.grid[r][c] == 'C':
                    self.grid[r][c] = '.'
                    self.creeper_coverage -= 1
                    self.creeper_coverage = max(0, self.creeper_coverage) # Ensure creeper coverage doesn't go below 0.

        self.message = f"Pruning shears used successfully at ({row}, {col})."
        return True

    def grow_creepers(self):
        """Grows the creepers, potentially spreading to adjacent empty cells."""
        if self.game_over:
            return

        for row, col in self.creeper_start_locations:
            # Attempt to grow from the starting locations.

            #Find adjacent empty cells
            adjacent_empty_cells = []
            for r_offset in [-1, 0, 1]:
                for c_offset in [-1, 0, 1]:
                    if abs(r_offset) + abs(c_offset) != 1: # Only check cells directly above, below, left, or right
                        continue # Skip diagonals and current cell.
                    new_row, new_col = row + r_offset, col + c_offset
                    if 0 <= new_row < self.grid_size[0] and 0 <= new_col < self.grid_size[1] and self.grid[new_row][new_col] == '.':
                        adjacent_empty_cells.append((new_row, new_col))

            #Randomly attempt to spread creeper if there are valid empty cells available
            if adjacent_empty_cells and random.random() < self.creeper_growth_rate:
                new_row, new_col = random.choice(adjacent_empty_cells)
                self.grid[new_row][new_col] = 'C'
                self.creeper_coverage += 1


        #Update coverage after all growth attempts
        self.creeper_coverage = sum(row.count('C') for row in self.grid)  # Recalculate actual coverage
        if self.creeper_coverage > self.max_creeper_coverage:
            self.game_over = True
            self.message = "Game Over: Creeper coverage exceeded the limit."


    def calculate_golden_ratio_score(self):
        """Calculates a score based on adherence to the Golden Ratio."""
        # This is a simplified placeholder.  A real implementation would require
        # analysis of flower cluster sizes and positioning relative to the grid.
        # The scoring would need careful playtesting and calibration.

        # For example, we can add points if certain grid squares have 3 or more flowers in close proximity to them
        golden_squares = 0
        for row in range(self.grid_size[0]):
          for col in range(self.grid_size[1]):
            count_flowers = 0
            for r_offset in [-1,0,1]:
              for c_offset in [-1,0,1]:
                n_row, n_col = row + r_offset, col + c_offset
                if 0 <= n_row < self.grid_size[0] and 0 <= n_col < self.grid_size[1]:
                  if self.grid[n_row][n_col] != '.' and self.grid[n_row][n_col] != 'C':
                    count_flowers += 1

            if count_flowers >= 3:
              golden_squares += 1


        self.golden_ratio_score =  (golden_squares/(self.grid_size[0]*self.grid_size[1]))*100 #Percentage of golden squares
        return self.golden_ratio_score



    def calculate_symmetry_score(self):
        """Calculates a score based on rotational symmetry around the center."""

        total_pairs = 0
        symmetric_pairs = 0

        center_row = self.grid_size[0] // 2
        center_col = self.grid_size[1] // 2

        #Check for 2-fold rotational symmetry.
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if row == center_row and col == center_col:
                    continue #Skip the center cell as it would match against itself.

                opposite_row = self.grid_size[0] - 1 - row #Calculate the opposite row
                opposite_col = self.grid_size[1] - 1 - col #Calculate the opposite col

                total_pairs +=1

                if self.grid[row][col] == self.grid[opposite_row][opposite_col]:
                    symmetric_pairs += 1


        self.symmetry_score = (symmetric_pairs/total_pairs) * 100 #Calculate percentage of symmetry
        return self.symmetry_score


    def check_order_fulfilled(self):
        """Checks if the flower arrangement fulfills the level's order requirements."""
        if self.game_over:
            return False

        sunflower_count = sum(row.count('S') for row in self.grid) + sum(row.count('#') for row in self.grid)
        lavender_count = sum(row.count('L') for row in self.grid)
        crimson_rose_count = sum(row.count('C') for row in self.grid) #Count of roses has been modified from the original code to not create conflicts with the creeper representation

        if sunflower_count < self.sunflower_count_required:
            self.message = f"Order not fulfilled:  Insufficient Sunflowers (required: {self.sunflower_count_required}, placed: {sunflower_count})"
            return False
        if lavender_count < self.lavender_count_required:
             self.message = f"Order not fulfilled: Insufficient Lavender (required: {self.lavender_count_required}, placed: {lavender_count})"
             return False
        if crimson_rose_count < self.crimson_rose_count_required:
             self.message = f"Order not fulfilled: Insufficient Crimson Roses (required: {self.crimson_rose_count_required}, placed: {crimson_rose_count})"
             return False
        if self.creeper_coverage > self.max_creeper_coverage:
            self.message = f"Order not fulfilled: Creeper coverage exceeds the limit (max: {self.max_creeper_coverage}, current: {self.creeper_coverage})"
            return False

        # Calculate Golden Ratio and Symmetry scores here, and potentially factor them into the overall fulfillment check.
        self.calculate_golden_ratio_score() #Update the golden ratio score
        self.calculate_symmetry_score() #Update the symmetry score

        if self.golden_ratio_score < 50: #Minimum Golden Ratio score of 50% required for fulfillment
          self.message = f"Order not fulfilled: Insufficient Golden Ratio score (required: 50%, current: {self.golden_ratio_score}%)"
          return False

        if self.symmetry_score < 75: #Minimum Symmetry score of 75% required for fulfillment
          self.message = f"Order not fulfilled: Insufficient Symmetry score (required: 75%, current: {self.symmetry_score}%)"
          return False


        self.message = "Order fulfilled successfully!"
        return True


    def update_level_state(self):
      """Updates the level state, growing creepers and checking for game over."""
      if not self.game_over:
          self.grow_creepers()
          if self.creeper_coverage > self.max_creeper_coverage:
              self.game_over = True
              self.message = "Game Over: Creeper coverage exceeded the limit."



    def get_level_state(self):
      """Returns the current state of the level for UI display."""
      return {
          "grid": self.grid,
          "flower_counts": {
              "Sunflower": sum(row.count('S') for row in self.grid) + sum(row.count('#') for row in self.grid),
              "Lavender": sum(row.count('L') for row in self.grid),
              "Crimson Rose": sum(row.count('R') for row in self.grid),
              "White Lily": sum(row.count('W') for row in self.grid)
          },
          "creeper_coverage": self.creeper_coverage,
          "pruning_shears_remaining": self.pruning_shears_available - self.pruning_shears_used,
          "golden_ratio_score": self.golden_ratio_score,
          "symmetry_score": self.symmetry_score,
          "message": self.message,
          "game_over": self.game_over
      }


    def reset_level(self):
        """Resets the level to its initial state."""
        self.__init__()  # Re-initialize the object
        self.message = "Level reset."


if __name__ == '__main__':
    # Example usage
    level = Level4()
    level.display_grid()
    print(level.get_level_state())


    #Try placing flowers
    level.place_flower(0, 0, "Sunflower")
    level.place_flower(0, 1, "Lavender")
    level.place_flower(0, 2, "Crimson Rose")
    level.place_flower(0, 3, "White Lily")
    level.display_grid()
    print(level.get_level_state())


    #Grow creepers a few times
    for _ in range(5):
      level.update_level_state()
      level.display_grid()
      print(level.get_level_state())

    # Use pruning shears
    level.use_pruning_shears(0, 0)
    level.display_grid()
    print(level.get_level_state())

    #Check if order is fulfilled before game over state.
    print(level.check_order_fulfilled())

    #Grow creepers until game over
    while not level.game_over:
      level.update_level_state()
      level.display_grid()
      print(level.get_level_state())

    #Reset level
    level.reset_level()
    level.display_grid()
    print(level.get_level_state())