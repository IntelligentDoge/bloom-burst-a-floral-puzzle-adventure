```python
import random

class PowerUp:
    """
    Represents a power-up in the Bloom Burst game.
    """

    def __init__(self, name, description, duration, effect_function):
        """
        Initializes a PowerUp object.

        Args:
            name (str): The name of the power-up.
            description (str): A brief description of the power-up's effect.
            duration (int): The duration (in turns/moves) the power-up lasts.
            effect_function (callable): A function that implements the power-up's effect.
                                         It should take the game state as input and modify it.
        """
        self.name = name
        self.description = description
        self.duration = duration
        self.effect_function = effect_function
        self.remaining_duration = 0  # Initially not active

    def activate(self):
        """
        Activates the power-up.
        """
        self.remaining_duration = self.duration

    def deactivate(self):
        """
        Deactivates the power-up.
        """
        self.remaining_duration = 0

    def is_active(self):
        """
        Checks if the power-up is currently active.

        Returns:
            bool: True if the power-up is active, False otherwise.
        """
        return self.remaining_duration > 0

    def tick(self):
        """
        Reduces the remaining duration of the power-up by 1.  Called each turn when active.
        """
        if self.is_active():
            self.remaining_duration -= 1
            if self.remaining_duration == 0:
                print(f"{self.name} has expired.")


class PowerUpManager:
    """
    Manages the power-ups available in the game.
    """

    def __init__(self, game_state):
        """
        Initializes the PowerUpManager.

        Args:
            game_state: A reference to the game state object. This allows power-ups
                        to directly affect the game.
        """
        self.power_ups = {}
        self.active_power_ups = []
        self.game_state = game_state  # Store a reference to the game state

    def add_power_up(self, power_up):
        """
        Adds a power-up to the manager's list of available power-ups.

        Args:
            power_up (PowerUp): The power-up object to add.
        """
        if power_up.name in self.power_ups:
            print(f"Warning: Power-up with name '{power_up.name}' already exists.")
        else:
            self.power_ups[power_up.name] = power_up

    def remove_power_up(self, power_up_name):
         """Removes a power-up from the manager."""
         if power_up_name in self.power_ups:
             del self.power_ups[power_up_name]
         else:
             print(f"Error: Power-up '{power_up_name}' not found.")


    def activate_power_up(self, power_up_name):
        """
        Activates a specific power-up by name.

        Args:
            power_up_name (str): The name of the power-up to activate.
        """
        if power_up_name in self.power_ups:
            power_up = self.power_ups[power_up_name]
            if power_up.is_active():
                print(f"Error: {power_up_name} is already active.")
            else:
                power_up.activate()
                self.active_power_ups.append(power_up)
                print(f"{power_up_name} activated! {power_up.description}")
                try:
                    power_up.effect_function(self.game_state)  # Apply effect immediately
                except Exception as e:
                    print(f"Error applying power-up effect: {e}")
        else:
            print(f"Error: Power-up '{power_up_name}' not found.")

    def deactivate_power_up(self, power_up_name):
        """
        Deactivates a power-up manually (e.g., if an issue occurs or the game requires it).

        Args:
            power_up_name (str): The name of the power-up to deactivate.
        """

        if power_up_name in self.power_ups:
            power_up = self.power_ups[power_up_name]
            if power_up.is_active():
                 power_up.deactivate()
                 self.active_power_ups.remove(power_up)
                 print(f"{power_up_name} deactivated.")
            else:
                 print(f"{power_up_name} is not active")
        else:
             print(f"Error: Power-up '{power_up_name}' not found.")

    def update(self):
        """
        Updates the state of all active power-ups (e.g., reduces duration).
        Should be called at the end of each turn.
        """
        # Iterate in reverse to allow safe removal of expired power-ups
        for power_up in list(self.active_power_ups):  # Iterate over a copy
            power_up.tick()
            if not power_up.is_active():
                self.active_power_ups.remove(power_up)

    def get_available_power_ups(self):
        """
        Returns a list of available power-up names.

        Returns:
            list: A list of power-up names.
        """
        return list(self.power_ups.keys())

    def get_active_power_ups(self):
        """
        Returns a list of currently active power-up names.

        Returns:
            list: A list of active power-up names.
        """
        return [power_up.name for power_up in self.active_power_ups]

    def display_power_ups(self):
        """
        Prints a list of available power-ups with their descriptions.
        """
        print("Available Power-Ups:")
        for name, power_up in self.power_ups.items():
            print(f"- {name}: {power_up.description} (Duration: {power_up.duration} turns)")

    def display_active_power_ups(self):
        """
        Prints a list of active power-ups with their remaining duration.
        """
        if self.active_power_ups:
            print("Active Power-Ups:")
            for power_up in self.active_power_ups:
                print(f"- {power_up.name}: Remaining Duration: {power_up.remaining_duration} turns")
        else:
            print("No power-ups are currently active.")


class GameState:
    """
    A placeholder for the game's state.  In a real game, this would
    contain the arrangement grid, player score, etc.
    """
    def __init__(self):
        self.score = 0
        self.grid = [] # Add grid for flowers

    def increase_score(self, amount):
        """Increases the game score."""
        self.score += amount
        print(f"Score increased by {amount}. New score: {self.score}")

    def decrease_score(self, amount):
        """Decreases the game score."""
        self.score -= amount
        print(f"Score decreased by {amount}. New score: {self.score}")

    def randomize_grid(self):
        """Randomizes the game grid (placeholder function)."""
        print("Randomizing grid...")
        self.grid = [random.randint(0, 5) for _ in range(9)] # basic 3x3 grid for testing
        print(f"New grid: {self.grid}")

    def print_grid(self): # added function for demo
        print("Current Grid:")
        print(self.grid)



# --- Example Power-Up Effects ---
def score_boost_effect(game_state):
    """
    Increases the player's score.

    Args:
        game_state: The game state object.
    """
    game_state.increase_score(100)

def randomize_grid_effect(game_state):
    """
    Randomizes the flower grid.

    Args:
        game_state: The game state object.
    """
    game_state.randomize_grid()

def flower_growth_effect(game_state):
    """Example: Increases the bloom value for next flower placed (PLACEHOLDER)"""
    print("Flower growth effect (placeholder)")

# --- Example Usage ---
if __name__ == '__main__':
    # 1. Initialize the game state
    game_state = GameState()

    # 2. Create a PowerUpManager and associate it with the game state
    power_up_manager = PowerUpManager(game_state)

    # 3. Create some power-ups
    score_boost = PowerUp("Score Boost", "Increases your score by 100.", 3, score_boost_effect)
    randomize_grid = PowerUp("Randomize Grid", "Randomizes the flower arrangement grid.", 1, randomize_grid_effect)
    flower_growth = PowerUp("Flower Growth", "Temporarily increases the growth rate of flowers.", 2, flower_growth_effect)

    # 4. Add the power-ups to the manager
    power_up_manager.add_power_up(score_boost)
    power_up_manager.add_power_up(randomize_grid)
    power_up_manager.add_power_up(flower_growth)

    # 5. Demonstrate usage
    power_up_manager.display_power_ups() # show available options

    # Player activates "Score Boost"
    power_up_manager.activate_power_up("Score Boost") # turn 1
    power_up_manager.display_active_power_ups()

    # End of turn 1
    power_up_manager.update()
    power_up_manager.display_active_power_ups()# turn 2

    # End of turn 2
    power_up_manager.update()
    power_up_manager.display_active_power_ups()# turn 3

    # End of turn 3
    power_up_manager.update()
    power_up_manager.display_active_power_ups()# turn 4

    # Try activating an invalid power-up
    power_up_manager.activate_power_up("Invalid Power-Up")

    # Activate Randomize Grid
    power_up_manager.activate_power_up("Randomize Grid")
    game_state.print_grid() # see initial grid
    power_up_manager.update() # randomize happens immediately on activation
    game_state.print_grid() # see new grid after powerup

    power_up_manager.display_active_power_ups()
    power_up_manager.update()
    power_up_manager.display_active_power_ups()

    # Manually deactivate a power-up
    power_up_manager.activate_power_up("Flower Growth")
    power_up_manager.display_active_power_ups()
    power_up_manager.deactivate_power_up("Flower Growth")
    power_up_manager.display_active_power_ups()
```