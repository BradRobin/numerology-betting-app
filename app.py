from functools import reduce

# Dictionary for letter to number conversion (Numerology values)
MANAGER_LUCKY_NUMBERS = {1, 4, 7, 11, 13, 22, 31}

letterConversions = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 11, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 11, "U": 3, "V": 22, "W": 5, "X": 6, "Y": 7, "Z": 8,
}

zodiac_signs = {
    0: "Monkey",
    1: "Rooster",
    2: "Dog",
    3: "Pig",
    4: "Rat",
    5: "Ox",
    6: "Tiger",
    7: "Cat",  # Changed to "Cat" as per preference
    8: "Dragon",
    9: "Snake",
    10: "Horse",
    11: "Goat",  # Changed to "Goat" as per preference
}

def calculate_life_path(day, month, year):
    total = sum(map(int, str(day))) + sum(map(int, str(month))) + sum(map(int, str(year)))
    return reduce_to_single_digit(total)

def check_manager_bonus(day, life_path):
    return day in MANAGER_LUCKY_NUMBERS or life_path in MANAGER_LUCKY_NUMBERS

def reduce_to_single_digit(num):
    while num > 9 and num not in {11, 22, 33}:
        num = sum(map(int, str(num)))
    return num

def calculate_numerology(name, conversions):
    total = 0
    for letter in name.upper():
        if letter in conversions:
            total += conversions[letter]
    return reduce_to_single_digit(total)

def get_zodiac_sign(year):
    year_mod = year % 12
    return zodiac_signs.get(year_mod, "Unknown")

def calculate_secondary_energy(day):
    return reduce_to_single_digit(day)

def calculate_primary_energy(day, month, year):
    total = sum(map(int, str(day))) + sum(map(int, str(month))) + sum(map(int, str(year)))
    return reduce_to_single_digit(total)

def process_manager_birthdate(team_name):
    print(f"Enter the manager's birthdate for {team_name} (format: day/month/year): ")
    day, month, year = map(int, input().split('/'))
    secondary_energy = calculate_secondary_energy(day)
    primary_energy = calculate_primary_energy(day, month, year)

    print(f"Manager's secondary energy (born day): {secondary_energy}")
    print(f"Manager's primary energy (born day): {primary_energy}")

    life_path = calculate_life_path(day, month, year)
    manager_bonus = 1 if check_manager_bonus(day, life_path) else 0
    return secondary_energy, primary_energy, manager_bonus

def process_team_players(team_name, num_players):
    print(f"Processing {team_name} players...")
    player_energies = []
    player_zodiacs = []
    for i in range(num_players):
        print(f"Enter birthdate for player {i+1} (format: day/month/year): ")
        day, month, year = map(int, input().split('/'))
        secondary_energy = calculate_secondary_energy(day)
        primary_energy = calculate_primary_energy(day, month, year)

        player_zodiac = get_zodiac_sign(year)
        player_zodiacs.append(player_zodiac)

        print(f"Player {i+1}: Secondary Energy = {secondary_energy}, Primary Energy = {primary_energy}, Zodiac = {player_zodiac}")
        player_energies.append((secondary_energy, primary_energy))

    return player_energies, player_zodiacs

def calculate_team_points(first_value, second_value, manager_bonus):
    points = 0
    if first_value in {1, 11}:
        points += 1
    if second_value in {1, 11}:
        points += 1
    if first_value in {1, 11} and second_value in {1, 11}:
        points += 1
    return points + manager_bonus

def calculate_zodiac_points(team_zodiac, player_zodiacs, manager_zodiac):
    zodiac_friendships = {
        "Rat": ["Dragon", "Monkey"],
        "Ox": ["Snake", "Rooster"],
        "Tiger": ["Horse", "Dog"],
        "Cat": ["Goat", "Pig"],
        "Dragon": ["Rat", "Monkey"],
        "Snake": ["Rooster", "Ox"],
        "Horse": ["Tiger", "Dog"],
        "Goat": ["Cat", "Pig"],
        "Monkey": ["Dragon", "Rat"],
        "Rooster": ["Snake", "Ox"],
        "Dog": ["Tiger", "Horse"],
        "Pig": ["Cat", "Goat"]
    }
    zodiac_enemies = {
        "Rat": ["Horse", "Goat"],
        "Ox": ["Goat", "Horse"],
        "Tiger": ["Monkey", "Snake"],
        "Cat": ["Rooster", "Dragon"],
        "Dragon": ["Cat", "Dog"],
        "Snake": ["Pig", "Tiger"],
        "Horse": ["Rat", "Ox"],
        "Goat": ["Ox", "Rat"],
        "Monkey": ["Tiger", "Pig"],
        "Rooster": ["Cat", "Dog"],
        "Dog": ["Dragon", "Rooster"],
        "Pig": ["Snake", "Monkey"]
    }

    points = 0

    # Manager zodiac comparison
    if manager_zodiac == team_zodiac:
        points += 2
    elif manager_zodiac in zodiac_friendships.get(team_zodiac, []):
        points += 1
    elif manager_zodiac in zodiac_enemies.get(team_zodiac, []):
        points -= 1

    # Player zodiacs comparison
    for player_zodiac in player_zodiacs:
        if player_zodiac == team_zodiac:
            points += 2
        elif player_zodiac in zodiac_friendships.get(team_zodiac, []):
            points += 1
        elif player_zodiac in zodiac_enemies.get(team_zodiac, []):
            points -= 1

    return points

# User input for team names
home_team_first_name = input("Enter home team first name: ")
home_team_second_name = input("Enter home team second name: ")
away_team_first_name = input("Enter away team first name: ")
away_team_second_name = input("Enter away team second name: ")

# User input for founding years
home_team_founding_year = int(input("Enter home team's founding year: "))
away_team_founding_year = int(input("Enter away team's founding year: "))

# Calculate numerology values for team names
home_team_first_value = calculate_numerology(home_team_first_name, letterConversions)
home_team_second_value = calculate_numerology(home_team_second_name, letterConversions)
away_team_first_value = calculate_numerology(away_team_first_name, letterConversions)
away_team_second_value = calculate_numerology(away_team_second_name, letterConversions)

home_team_combined_value = reduce_to_single_digit(home_team_first_value + home_team_second_value)
away_team_combined_value = reduce_to_single_digit(away_team_first_value + away_team_second_value)

# Zodiac sign calculation
home_team_zodiac = get_zodiac_sign(home_team_founding_year)
away_team_zodiac = get_zodiac_sign(away_team_founding_year)

# Input number of players per team
home_team_players = int(input("Enter the number of players in the home team: "))
away_team_players = int(input("Enter the number of players in the away team: "))

# Process players and manager for both teams
home_team_energies, home_team_player_zodiacs = process_team_players("Home Team", home_team_players)
away_team_energies, away_team_player_zodiacs = process_team_players("Away Team", away_team_players)

home_team_manager_secondary, home_team_manager_primary, home_team_manager_bonus = process_manager_birthdate("Home Team")
home_team_manager_zodiac = get_zodiac_sign(int(input("Enter home manager's birth year: ")))

away_team_manager_secondary, away_team_manager_primary, away_team_manager_bonus = process_manager_birthdate("Away Team")
away_team_manager_zodiac = get_zodiac_sign(int(input("Enter away manager's birth year: ")))

home_team_points = calculate_team_points(home_team_first_value, home_team_second_value, home_team_manager_bonus)
away_team_points = calculate_team_points(away_team_first_value, away_team_second_value, away_team_manager_bonus)

# Calculate zodiac points
home_team_zodiac_points = calculate_zodiac_points(home_team_zodiac, home_team_player_zodiacs, home_team_manager_zodiac)
away_team_zodiac_points = calculate_zodiac_points(away_team_zodiac, away_team_player_zodiacs, away_team_manager_zodiac)

# Final score after adding zodiac points
home_team_final_score = home_team_points + home_team_zodiac_points
away_team_final_score = away_team_points + away_team_zodiac_points

# Output team numerology results
print(f"\nHome team ({home_team_first_name} {home_team_second_name}):")
print(f"  First name reduced value: {home_team_first_value}")
print(f"  Second name reduced value: {home_team_second_value}")
print(f"  Combined value: {home_team_combined_value}")
print(f"  Final score: {home_team_final_score}")

print(f"\nAway team ({away_team_first_name} {away_team_second_name}):")
print(f"  First name reduced value: {away_team_first_value}")
print(f"  Second name reduced value: {away_team_second_value}")
print(f"  Combined value: {away_team_combined_value}")
print(f"  Final score: {away_team_final_score}")

# Announce the winner
if home_team_final_score > away_team_final_score:
    print("\nHome team is likely to win!")
elif home_team_final_score < away_team_final_score:
    print("\nAway team is likely to win!")
else:
    print("\nIt's a Draw!")
