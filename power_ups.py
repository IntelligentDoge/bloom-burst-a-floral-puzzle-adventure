```python
import random
import time

class PowerUp:
    """
    Represents a power-up in the Bloom Burst game.
    """

    def __init__(self, name, description, duration, effect_function):
        """
        Initializes a new PowerUp instance.

        Args:
            name (str): The name of the power-up (e.g., "Bloom Boost").
            description (str): A brief description of what the power-up does.
            duration (int): The duration of the power-up's effect in seconds.
            effect_function (callable): A function that is called when the power-up is activated.
                                       It should take the game state as input.
        """
        self.name = name
        self.description = description
        self.duration = duration
        self.effect_function = effect_function
        self.is_active = False
        self.start_time = None

    def activate(self, game_state):
        """
        Activates the power-up, applying its effect and setting the active flag.

        Args:
            game_state: The current state of the game (e.g., a dictionary containing game data).
        """
        if not self.is_active:
            self.is_active = True
            self.start_time = time.time()
            self.effect_function(game_state)  # Apply the power-up's effect
            print(f"{self.name} activated! {self.description}")  # Provide feedback to the user
        else:
            print(f"{self.name} is already active.")

    def deactivate(self, game_state):
        """
        Deactivates the power-up, reverting its effect.  Override in subclass if needed.

        Args:
            game_state: The current state of the game.
        """
        self.is_active = False
        self.start_time = None
        print(f"{self.name} deactivated.")

    def update(self, game_state):
        """
        Updates the power-up state, checking if it has expired.

        Args:
            game_state: The current state of the game.

        Returns:
            bool: True if the power-up has expired and needs deactivation, False otherwise.
        """
        if self.is_active:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.duration:
                self.deactivate(game_state)
                return True  # Signal that the power-up has expired
        return False

    def __str__(self):
        return f"{self.name}: {self.description} (Duration: {self.duration} seconds)"


def grant_extra_time(game_state):
    """
    A power-up effect function that grants extra time.

    Args:
        game_state (dict): The game state dictionary.  Must contain a 'time_remaining' key.
    """
    if 'time_remaining' in game_state:
        extra_time = 10  # Seconds to add
        game_state['time_remaining'] += extra_time
        print(f"Added {extra_time} seconds! Time remaining: {game_state['time_remaining']}")
    else:
        print("Error: Time remaining not found in game state.")


def double_score(game_state):
    """
    A power-up effect function that doubles the player's score.

    Args:
        game_state (dict): The game state dictionary.  Must contain a 'score_multiplier' key.
    """
    if 'score_multiplier' in game_state:
        game_state['score_multiplier'] *= 2
        print(f"Score multiplier doubled! Current multiplier: {game_state['score_multiplier']}")
    else:
        print("Error: Score multiplier not found in game state.")


def clear_board(game_state):
    """
    A power-up effect function that clears the board. Assumes a 'board' key in game_state.

    Args:
        game_state (dict): The game state dictionary.
    """
    if 'board' in game_state:
        rows = len(game_state['board'])
        cols = len(game_state['board'][0]) if rows > 0 else 0 # handle empty boards
        game_state['board'] = [[' ' for _ in range(cols)] for _ in range(rows)]  # Clear the board
        print("Board cleared!")
    else:
        print("Error: Game board not found in game state.")


class PowerUpManager:
    """
    Manages the power-ups in the game, including creation, activation, and tracking.
    """

    def __init__(self):
        """
        Initializes the PowerUpManager with a list of available power-ups.
        """
        self.available_power_ups = [
            PowerUp("Bloom Boost", "Grants extra time", 10, grant_extra_time),
            PowerUp("Score Surge", "Doubles your score", 5, double_score),
            PowerUp("Board Blast", "Clears the entire board", 0.1, clear_board),
        ]
        self.active_power_ups = []

    def create_power_up(self, power_up_name):
        """
        Creates a new power-up instance based on its name.

        Args:
            power_up_name (str): The name of the power-up to create.

        Returns:
            PowerUp: A new PowerUp instance, or None if the power-up name is invalid.
        """
        for power_up in self.available_power_ups:
            if power_up.name.lower() == power_up_name.lower():
                return PowerUp(power_up.name, power_up.description, power_up.duration, power_up.effect_function)
        print(f"Error: Invalid power-up name: {power_up_name}")
        return None

    def activate_power_up(self, power_up_name, game_state):
        """
        Activates a power-up by name.

        Args:
            power_up_name (str): The name of the power-up to activate.
            game_state: The current state of the game.

        Returns:
            bool: True if the power-up was activated successfully, False otherwise.
        """
        power_up = self.create_power_up(power_up_name)
        if power_up:
            power_up.activate(game_state)
            self.active_power_ups.append(power_up)
            return True
        return False

    def update_power_ups(self, game_state):
        """
        Updates the state of all active power-ups, deactivating any that have expired.

        Args:
            game_state: The current state of the game.
        """
        expired_power_ups = []
        for power_up in self.active_power_ups:
            if power_up.update(game_state):
                expired_power_ups.append(power_up)

        for power_up in expired_power_ups:
            self.active_power_ups.remove(power_up)


# Example Usage
if __name__ == '__main__':
    # Initialize game state
    game_state = {
        'time_remaining': 30,
        'score_multiplier': 1,
        'board': [['R', 'G', 'B'], ['Y', 'R', 'G'], ['B', 'Y', 'R']]
    }

    # Initialize power-up manager
    power_up_manager = PowerUpManager()

    # Player uses a power-up
    print("\nActivating Bloom Boost...")
    power_up_manager.activate_power_up("Bloom Boost", game_state)

    # Simulate game running and updating power-ups
    print("\nSimulating game running...")
    for _ in range(12):
        time.sleep(1)
        game_state['time_remaining'] -= 1
        print(f"Time Remaining: {game_state['time_remaining']}")
        power_up_manager.update_power_ups(game_state)

        #Check score multiplier during the 'Score Surge' power up
        if _ == 2:
            print("\nActivating Score Surge...")
            power_up_manager.activate_power_up("Score Surge", game_state)
        if _ == 7:
            print("\nActivating Board Blast...")
            power_up_manager.activate_power_up("Board Blast", game_state)
            print(f"Game Board: {game_state['board']}")

    print("\nGame over!")
```