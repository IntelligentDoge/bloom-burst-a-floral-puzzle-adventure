```python
import random
import time

class PowerUp:
    """
    Base class for all power-ups. Defines the core attributes and methods.
    """
    def __init__(self, name, description, duration):
        """
        Initializes a new power-up instance.

        Args:
            name (str): The name of the power-up.
            description (str): A brief description of what the power-up does.
            duration (int): The duration of the power-up's effect in seconds.
        """
        self.name = name
        self.description = description
        self.duration = duration
        self.start_time = None
        self.is_active = False

    def activate(self, player):
        """
        Activates the power-up, applying its effects.  Must be overridden by subclasses.
        Should also set self.is_active to True and self.start_time to the current time.

        Args:
            player: The player object to apply the power-up's effects to.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("activate() method must be implemented in a subclass")

    def deactivate(self, player):
        """
        Deactivates the power-up, removing its effects.  Must be overridden by subclasses.
        Should also set self.is_active to False.

        Args:
            player: The player object to remove the power-up's effects from.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("deactivate() method must be implemented in a subclass")

    def is_expired(self):
        """
        Checks if the power-up has expired.

        Returns:
            bool: True if the power-up's duration has passed, False otherwise.
        """
        if not self.is_active:
            return True  # Consider inactive power-ups as expired
        return time.time() - self.start_time > self.duration

    def __str__(self):
        return f"{self.name}: {self.description} (Duration: {self.duration} seconds)"


class BloomBoost(PowerUp):
    """
    A power-up that temporarily increases the bloom potential of flowers.
    """
    def __init__(self):
        super().__init__("Bloom Boost", "Temporarily increases bloom potential by 25%.", 10)
        self.bloom_boost_percentage = 0.25  # 25% boost

    def activate(self, player):
        """
        Activates the bloom boost, increasing the player's bloom potential modifier.

        Args:
            player: The player object.
        """
        if self.is_active:
            print("Bloom Boost is already active!")
            return
        
        print("Activating Bloom Boost!")
        player.bloom_potential_modifier += self.bloom_boost_percentage
        self.is_active = True
        self.start_time = time.time()

    def deactivate(self, player):
        """
        Deactivates the bloom boost, restoring the player's bloom potential modifier.

        Args:
            player: The player object.
        """
        if not self.is_active:
            print("Bloom Boost is not active!")
            return
            
        print("Deactivating Bloom Boost!")
        player.bloom_potential_modifier -= self.bloom_boost_percentage
        self.is_active = False


class ColorHarmony(PowerUp):
    """
    A power-up that temporarily increases score for matching flower colors.
    """
    def __init__(self):
        super().__init__("Color Harmony", "Temporarily increases score for matching flower colors by 50%.", 15)
        self.color_harmony_bonus = 0.50  # 50% bonus

    def activate(self, player):
        """
        Activates the color harmony bonus.

        Args:
            player: The player object.
        """
        if self.is_active:
            print("Color Harmony is already active!")
            return
        
        print("Activating Color Harmony!")
        player.color_matching_bonus += self.color_harmony_bonus
        self.is_active = True
        self.start_time = time.time()

    def deactivate(self, player):
        """
        Deactivates the color harmony bonus.

        Args:
            player: The player object.
        """
        if not self.is_active:
            print("Color Harmony is not active!")
            return

        print("Deactivating Color Harmony!")
        player.color_matching_bonus -= self.color_harmony_bonus
        self.is_active = False

class SymmetrySurge(PowerUp):
    """
    A power-up that temporarily grants bonus points for arrangement symmetry.
    """
    def __init__(self):
        super().__init__("Symmetry Surge", "Temporarily grants bonus points for arrangement symmetry.", 20)
        self.symmetry_bonus = 100  # Flat bonus for symmetrical arrangements

    def activate(self, player):
        """
        Activates the symmetry surge.

        Args:
            player: The player object.
        """
        if self.is_active:
            print("Symmetry Surge is already active!")
            return
            
        print("Activating Symmetry Surge!")
        player.symmetry_bonus_active = True
        self.is_active = True
        self.start_time = time.time()

    def deactivate(self, player):
        """
        Deactivates the symmetry surge.

        Args:
            player: The player object.
        """
        if not self.is_active:
            print("Symmetry Surge is not active!")
            return

        print("Deactivating Symmetry Surge!")
        player.symmetry_bonus_active = False
        self.is_active = False

class PowerUpManager:
    """
    Manages power-up collection and usage.
    """
    def __init__(self):
        """
        Initializes the PowerUpManager.
        """
        self.power_ups = []  # List to store collected power-ups

    def add_power_up(self, power_up):
        """
        Adds a power-up to the player's inventory.

        Args:
            power_up (PowerUp): The power-up to add.
        """
        self.power_ups.append(power_up)
        print(f"You collected a {power_up.name}!")

    def use_power_up(self, power_up_name, player):
        """
        Uses a power-up from the player's inventory.

        Args:
            power_up_name (str): The name of the power-up to use.
            player: The player object.

        Returns:
            bool: True if the power-up was used successfully, False otherwise.
        """
        for power_up in self.power_ups:
            if power_up.name == power_up_name and not power_up.is_active:
                power_up.activate(player)
                #self.power_ups.remove(power_up)  # Remove after activation for single use, can comment out for reusable
                return True
        print(f"You don't have a {power_up_name} or it is already active.")
        return False

    def check_expired_power_ups(self, player):
         """
         Checks for and deactivates expired power-ups.

         Args:
             player: The player object.
         """
         for power_up in list(self.power_ups): # Iterate over a copy to allow modification
            if power_up.is_active and power_up.is_expired():
                 power_up.deactivate(player)

    def list_power_ups(self):
        """
        Lists the power-ups in the player's inventory.
        """
        if not self.power_ups:
            print("You have no power-ups.")
            return

        print("Your Power-ups:")
        for i, power_up in enumerate(self.power_ups):
            print(f"{i+1}. {power_up}")

# Example Usage (Illustrative)

class Player: # Dummy Player class for example
    def __init__(self, name):
        self.name = name
        self.bloom_potential_modifier = 1.0
        self.color_matching_bonus = 0.0
        self.symmetry_bonus_active = False

    def calculate_score(self, base_score, color_matches, is_symmetrical):
        score = base_score * self.bloom_potential_modifier
        score += color_matches * self.color_matching_bonus
        if self.symmetry_bonus_active and is_symmetrical:
            score += 100 # Example symmetry bonus
        return score

def main():
    """
    Illustrates the power-up system in a game loop.
    """
    player = Player("Alice")
    power_up_manager = PowerUpManager()

    # Game loop simulation
    for i in range(25): # Simulate some game turns
        print(f"\n--- Turn {i+1} ---")

        # Chance to find a power-up
        if random.random() < 0.2:  # 20% chance to find a power-up
            power_up_type = random.choice([BloomBoost, ColorHarmony, SymmetrySurge])
            power_up_manager.add_power_up(power_up_type())

        # List and use power-ups (example)
        if power_up_manager.power_ups:
            power_up_manager.list_power_ups()
            
            # Try to use a random power-up
            power_up_to_use = random.choice(power_up_manager.power_ups)
            power_up_manager.use_power_up(power_up_to_use.name, player)
        
        # Simulate game activity and score calculation
        base_score = 50
        color_matches = random.randint(0, 5)
        is_symmetrical = random.random() < 0.5 # Randomly say it's symmetrical half the time
        
        score = player.calculate_score(base_score, color_matches, is_symmetrical)
        print(f"Score: {score}")
        
        # Check and deactivate expired power-ups
        power_up_manager.check_expired_power_ups(player)

        time.sleep(1) # Simulate time passing

if __name__ == "__main__":
    main()
```