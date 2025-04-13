```python
import random

class PowerUp:
    """
    Represents a power-up that can be collected and used by the player.
    """
    def __init__(self, name, description, duration, effect):
        """
        Initializes a PowerUp object.

        Args:
            name (str): The name of the power-up (e.g., "Color Bomb").
            description (str): A brief description of the power-up's effect.
            duration (int): The number of turns the power-up lasts for. A value of -1 indicates a permanent effect.
            effect (function): A function that applies the power-up's effect to the game state. The function should accept the game state as input.
        """
        self.name = name
        self.description = description
        self.duration = duration
        self.effect = effect
        self.remaining_duration = 0 # initially not active

    def activate(self):
        """
        Activates the power-up, setting its remaining duration.
        """
        self.remaining_duration = self.duration

    def deactivate(self):
        """
        Deactivates the power-up by setting its remaining duration to zero.
        """
        self.remaining_duration = 0

    def is_active(self):
        """
        Checks if the power-up is currently active.

        Returns:
            bool: True if the power-up is active, False otherwise.
        """
        return self.remaining_duration > 0

    def decrement_duration(self):
        """
        Decrements the remaining duration of the power-up by one turn, if it is active.
        """
        if self.is_active():
            self.remaining_duration -= 1

    def __str__(self):
        return f"{self.name}: {self.description} (Duration: {self.remaining_duration if self.is_active() else self.duration})"

class PowerUpSystem:
    """
    Manages the power-up system, including spawning, collection, and application.
    """

    def __init__(self, available_power_ups):
        """
        Initializes the PowerUpSystem with a list of available power-ups.

        Args:
            available_power_ups (list[PowerUp]): A list of PowerUp objects that can be spawned in the game.
        """
        self.available_power_ups = available_power_ups
        self.active_power_ups = [] #List of active powerups
        self.player_power_ups = [] # List of powerups the player currently possesses

    def spawn_power_up(self, rarity_weights=None):
        """
        Spawns a random power-up based on a given probability distribution.

        Args:
            rarity_weights (dict[str, int], optional): Dictionary representing the relative rarities of power-ups.
                The keys are the names of the power-ups, and the values are their weights. Defaults to None (equal probability).

        Returns:
            PowerUp: A randomly selected PowerUp object.  Returns None if there are no available powerups.
        """
        if not self.available_power_ups:
            return None

        if rarity_weights is None:
            # Assign equal probability to each power-up
            rarity_weights = {power_up.name: 1 for power_up in self.available_power_ups}

        power_up_names = list(rarity_weights.keys())
        weights = list(rarity_weights.values())

        if sum(weights) == 0:
            return None

        try:
            chosen_power_up_name = random.choices(power_up_names, weights=weights, k=1)[0]  # k=1 returns a list with one element
            # Find the power-up object by its name
            chosen_power_up = next((p for p in self.available_power_ups if p.name == chosen_power_up_name), None)
            return chosen_power_up

        except IndexError:
            print("Error: Invalid rarity weights provided.")
            return None # or raise the exception again

    def collect_power_up(self, power_up):
        """
        Adds a power-up to the player's inventory.

        Args:
            power_up (PowerUp): The PowerUp object to add.
        """
        if power_up:
            self.player_power_ups.append(power_up)
            print(f"Collected power-up: {power_up.name}")
        else:
            print("Attempted to collect a null power-up")

    def activate_power_up(self, power_up):
        """
        Activates a power-up from the player's inventory.

        Args:
            power_up (PowerUp): The PowerUp object to activate.

        Returns:
            bool: True if the power-up was successfully activated, False otherwise.
        """
        if power_up in self.player_power_ups:
             power_up.activate()
             self.active_power_ups.append(power_up)
             self.player_power_ups.remove(power_up)
             print(f"Activated power-up: {power_up.name}")
             return True
        else:
             print(f"You do not have {power_up.name} in your inventory.")
             return False
    
    def deactivate_power_up(self, power_up):
        """
        Deactivates a power-up
        """
        if power_up in self.active_power_ups:
            power_up.deactivate()
            self.active_power_ups.remove(power_up)
            print(f"Deactivated power-up: {power_up.name}")
        else:
            print(f"{power_up.name} is not active")

    def apply_active_power_ups(self, game_state):
        """
        Applies the effects of all active power-ups to the game state.

        Args:
            game_state: The current state of the game. This could be any data structure relevant to the game's logic.
        """
        for power_up in self.active_power_ups:
            power_up.effect(game_state)

    def update_power_up_durations(self):
        """
        Updates the remaining duration of active power-ups, deactivating any that have expired.
        """
        power_ups_to_remove = []
        for power_up in self.active_power_ups:
            power_up.decrement_duration()
            if power_up.remaining_duration == 0:
                print(f"{power_up.name} has expired.")
                power_ups_to_remove.append(power_up)

        for power_up in power_ups_to_remove:
            self.deactivate_power_up(power_up)

    def get_player_power_ups(self):
        """
        Returns a list of powerups the player currently possess.
        """
        return self.player_power_ups
    
    def get_active_power_ups(self):
        """
        Returns a list of active powerups
        """
        return self.active_power_ups
    

def example_effect(game_state):
    """
    An example of a power-up effect.  This simply prints a message to the console,
    but in a real game, this would modify the game_state in some way.

    Args:
        game_state: The current state of the game.
    """
    print("Applying example effect to game state!")
    if 'score' in game_state:
        game_state['score'] += 10  # Example: Increase the score
    else:
        game_state['score'] = 10

if __name__ == '__main__':
    # Example Usage
    # Define some power-ups
    color_bomb = PowerUp("Color Bomb", "Destroys all flowers of a chosen color.", 3, example_effect)
    row_clear = PowerUp("Row Clear", "Clears an entire row.", 1, example_effect)
    score_multiplier = PowerUp("Score Multiplier", "Doubles your score for 5 turns.", 5, example_effect)

    # Create a PowerUpSystem
    power_up_system = PowerUpSystem([color_bomb, row_clear, score_multiplier])

    # Example game state
    game_state = {'level': 1, 'score': 0}

    # Spawn a power-up
    spawned_power_up = power_up_system.spawn_power_up()
    if spawned_power_up:
        print(f"Spawned: {spawned_power_up.name}")

        # Collect the power-up
        power_up_system.collect_power_up(spawned_power_up)

        # Print inventory
        print ("Player powerups: ", power_up_system.get_player_power_ups())

        # Activate the power-up
        power_up_system.activate_power_up(spawned_power_up)

        #Apply power ups
        power_up_system.apply_active_power_ups(game_state)
        print("Game state after applying power-up:", game_state)

        # Update power-up durations
        power_up_system.update_power_up_durations()
        print("Game state after turn:", game_state)
        print("Active powerups:", power_up_system.get_active_power_ups())

        # Update power-up durations again, until the powerup is deactivated
        while len(power_up_system.get_active_power_ups()) > 0:
            power_up_system.update_power_up_durations()
            print("Game state after turn:", game_state)
            print("Active powerups:", power_up_system.get_active_power_ups())

    else:
        print("No power-ups available to spawn.")
```