import random
import time
import matplotlib.pyplot as plt
import numpy as np
import json

# Explanation of Libraries:
# random: Used to generate random numbers for simulating different events, such as energy loss, mood changes, etc.
# time: Used to add delays, simulating the passing of time.
# matplotlib.pyplot: Used for visualizing data. Here we can plot energy, mood, and productivity over the days.
# numpy: Used for numerical operations, such as creating arrays to store energy, mood, and productivity data.
# json: Used for saving and loading player data to/from a file.

class Player:
    def __init__(self, name, energy=100, mood=50, productivity=70):
        self.name = name
        self.energy = energy
        self.mood = mood
        self.productivity = productivity

    def to_dict(self):
        return {
            'name': self.name,
            'energy': self.energy,
            'mood': self.mood,
            'productivity': self.productivity
        }

    @staticmethod
    def from_dict(data):
        return Player(data['name'], data['energy'], data['mood'], data['productivity'])


def create_player():
    name = input("Enter the player's name: ")
    return Player(name)


def display_player_stats(players):
    print("\nCurrent Player Stats:")
    for player in players:
        print(f"Name: {player.name}, Energy: {player.energy}%, Mood: {player.mood}%, Productivity: {player.productivity}%")


def update_player_attributes(players):
    for player in players:
        print(f"\nUpdating attributes for {player.name}:")
        player.energy = int(input(f"Enter new energy level for {player.name} (current: {player.energy}%): "))
        player.mood = int(input(f"Enter new mood level for {player.name} (current: {player.mood}%): "))
        player.productivity = int(input(f"Enter new productivity level for {player.name} (current: {player.productivity}%): "))


def save_player_data(players, filename="player_data.json"):
    with open(filename, 'w') as f:
        json.dump([player.to_dict() for player in players], f)
    print(f"Player data saved to {filename}")


def load_player_data(filename="player_data.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return [Player.from_dict(player_data) for player_data in data]
    except FileNotFoundError:
        print(f"No save file found with the name {filename}.")
        return []


def simulate_sleep_deprivation(player, days):
    # Initialize lists to store daily values for visualization
    energy_levels = []
    mood_levels = []
    productivity_levels = []

    for day in range(1, days + 1):
        print(f"\nDay {day} for {player.name}:")

        # Wake up
        energy_loss = random.randint(10, 30)
        player.energy -= energy_loss
        print(f"Waking up... Energy level: {player.energy}% (lost {energy_loss}%)")

        # Breakfast
        breakfast_success = random.random() > 0.2
        if breakfast_success:
            energy_gain = random.randint(5, 15)
            player.energy += energy_gain
            print(f"Had breakfast. Energy level: {player.energy}% (gained {energy_gain}%)")
        else:
            print("Skipped breakfast. Energy level remains low.")

        # Commute
        commute_mood_loss = random.randint(5, 10)
        player.mood -= commute_mood_loss
        print(f"Commute was exhausting. Mood level: {player.mood} (lost {commute_mood_loss})")

        # Work
        work_efficiency = max(0, player.productivity - (100 - player.energy) * 0.5)
        work_hours = random.randint(6, 9)
        print(f"Worked for {work_hours} hours with {work_efficiency:.2f}% efficiency.")

        # Productivity and Mood
        if work_efficiency < 50:
            mood_loss = random.randint(5, 20)
            player.mood -= mood_loss
            print(f"Struggled to concentrate. Mood level: {player.mood} (lost {mood_loss})")
        else:
            mood_gain = random.randint(5, 15)
            player.mood += mood_gain
            print(f"Felt productive. Mood level: {player.mood} (gained {mood_gain})")

        # Sleep
        sleep_quality = random.choice(['poor', 'okay', 'good'])
        if sleep_quality == 'poor':
            energy_gain = random.randint(5, 20)
        elif sleep_quality == 'okay':
            energy_gain = random.randint(20, 40)
        else:
            energy_gain = random.randint(40, 60)
        player.energy += energy_gain
        print(f"Sleep was {sleep_quality}. Energy level: {player.energy}% (gained {energy_gain}%)")

        # Ensure energy and mood stay within bounds
        player.energy = max(0, min(100, player.energy))
        player.mood = max(0, min(100, player.mood))

        # Store the values for visualization
        energy_levels.append(player.energy)
        mood_levels.append(player.mood)
        productivity_levels.append(work_efficiency)

        # Display summary of the day
        if player.mood < 30:
            print("The day ended with a feeling of exhaustion and irritability.")
        elif player.mood > 70:
            print("Despite the lack of sleep, ended the day with a surprisingly good mood.")
        else:
            print("The day ended feeling tired but manageable.")

        # Short pause to simulate time progression
        time.sleep(1)

    # Plot the results
    days_array = np.arange(1, days + 1)
    plt.figure(figsize=(10, 6))

    # Plot energy levels
    plt.plot(days_array, energy_levels, label=f'{player.name} Energy Level', marker='o')
    # Plot mood levels
    plt.plot(days_array, mood_levels, label=f'{player.name} Mood Level', marker='o')
    # Plot productivity levels
    plt.plot(days_array, productivity_levels, label=f'{player.name} Productivity Level', marker='o')

    plt.xlabel('Days')
    plt.ylabel('Percentage')
    plt.title(f'Sleep Deprivation Simulation Over Time for {player.name}')
    plt.legend()
    plt.grid(True)
    plt.show()


def simulate_100_players_for_100_days():
    players = [Player(f'Player_{i+1}') for i in range(100)]
    
    for player in players:
        for day in range(1, 101):
            # Wake up
            energy_loss = random.randint(10, 30)
            player.energy -= energy_loss

            # Breakfast
            breakfast_success = random.random() > 0.2
            if breakfast_success:
                energy_gain = random.randint(5, 15)
                player.energy += energy_gain

            # Commute
            commute_mood_loss = random.randint(5, 10)
            player.mood -= commute_mood_loss

            # Work
            work_efficiency = max(0, player.productivity - (100 - player.energy) * 0.5)
            work_hours = random.randint(6, 9)

            # Productivity and Mood
            if work_efficiency < 50:
                mood_loss = random.randint(5, 20)
                player.mood -= mood_loss
            else:
                mood_gain = random.randint(5, 15)
                player.mood += mood_gain

            # Sleep
            sleep_quality = random.choice(['poor', 'okay', 'good'])
            if sleep_quality == 'poor':
                energy_gain = random.randint(5, 20)
            elif sleep_quality == 'okay':
                energy_gain = random.randint(20, 40)
            else:
                energy_gain = random.randint(40, 60)
            player.energy += energy_gain

            # Ensure energy and mood stay within bounds
            player.energy = max(0, min(100, player.energy))
            player.mood = max(0, min(100, player.mood))

            # Termination condition
            if player.energy < 30 or player.mood < 30 or (player.energy + player.mood + player.productivity) < 100:
                print(f"The player {player.name} has almost worked himself to death. He will go out of the game and he lasts {day} days.")
                break


def main():
    print("Welcome to the Sleep Deprivation Simulator!")
    players = load_player_data()

    if not players:
        num_players = int(input("Enter the number of players: "))
        for _ in range(num_players):
            players.append(create_player())

    while True:
        print("\nMenu:")
        print("1. Display Player Stats")
        print("2. Update Player Attributes")
        print("3. Simulate Sleep Deprivation")
        print("4. Save Player Data")
        print("5. Load Player Data")
        print("6. Simulate 100 Players for 100 Days")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            display_player_stats(players)
        elif choice == '2':
            update_player_attributes(players)
        elif choice == '3':
            days = int(input("Enter the number of days to simulate: "))
            for player in players:
                simulate_sleep_deprivation(player, days)
        elif choice == '4':
            save_player_data(players)
        elif choice == '5':
            players = load_player_data()
        elif choice == '6':
            simulate_100_players_for_100_days()
        elif choice == '7':
            print("Exiting the simulator. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the main function
if __name__ == "__main__":
    main()
