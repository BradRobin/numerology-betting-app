from functools import reduce

# Dictionary for letter to number conversion (Numerology values)
MANAGER_LUCKY_NUMBERS = {1, 3, 4, 7, 11, 13, 22, 33}

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
    7: "Cat",  
    8: "Dragon",
    9: "Snake",
    10: "Horse",
    11: "Goat",  
}

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

def calculate_life_path(day, month, year):
    total = sum(map(int, str(day))) + sum(map(int, str(month))) + sum(map(int, str(year)))
    return reduce_to_single_digit(total)

def check_manager_bonus(day, life_path):
    return day in MANAGER_LUCKY_NUMBERS or life_path in MANAGER_LUCKY_NUMBERS

def get_zodiac_sign(year):
    year_mod = year % 12
    return zodiac_signs.get(year_mod, "Unknown")

def calculate_secondary_energy(day):
    return reduce_to_single_digit(day)

def calculate_primary_energy(day, month, year):
    total = sum(map(int, str(day))) + sum(map(int, str(month))) + sum(map(int, str(year)))
  
def process_manager_info(team_name):
    first_name = input(f"Enter the manager's first name for {team_name}: ")
    last_name = input(f"Enter the manager's last name for {team_name}: ")

    # Calculate numerology for manager's full name
    first_name_value = calculate_numerology(first_name, letterConversions)
    last_name_value = calculate_numerology(last_name, letterConversions)
    total_name_value = reduce_to_single_digit(first_name_value + last_name_value)

    print(f"{team_name} Manager Name Numerology: {total_name_value}")

    # Calculate points based on name numerology
    name_points = 1 if total_name_value in [1, 3, 4, 7, 11, 22, 33] else 0

    # Manager's birthdate processing
    print(f"Enter the manager's birthdate for {team_name} (format: day/month/year): ")
    day, month, year = map(int, input().split('/'))

    life_path = calculate_life_path(day, month, year)
    birthdate_points = 1 if check_manager_bonus(day, life_path) else 0

    # Manager's zodiac sign
    manager_zodiac = get_zodiac_sign(year)
    print(f"{team_name} Manager Zodiac: {manager_zodiac}")

    return name_points, birthdate_points, manager_zodiac

def process_team_players(team_name, num_players):
    print(f"Processing {team_name} players...")
    player_zodiacs = []
    player_points = 0 # Access the global player points

    print(f"Enter the details of the captain for {team_name}:")
    captain_name = input(f"Enter the captain's name for {team_name}: ")

    # Calculate numerology for the captain's name
    captain_name_numerology = calculate_numerology(captain_name, letterConversions)

    if captain_name_numerology in [1, 3, 4, 11, 22, 33]:
        player_points += 1
        print(f"{team_name} earns a point for the captain {captain_name}'s numerology ({captain_name_numerology})")
    elif captain_name_numerology == 7:
        player_points -= 1
        print(f"{team_name} loses a point for the captain {captain_name}'s numerology")

    # Get captain's birthdate
    captain_birthdate = input(f"Enter the captain's birthdate (dd/mm/yyyy): ")
    day, month, year = map(int, captain_birthdate.split('/'))

    # Check if captain's day of birth is special or adds up to 1
    if day in [1, 10, 19, 28] or calculate_numerology(captain_birthdate, letterConversions) == 1:
        player_points += 1
        print(f"{team_name} earns a point because the captain {captain_name} was born on a 1 day or numerology adds up to 1")

    # Calculate and store the captain's zodiac sign
    captain_zodiac = calculate_zodiac(captain_birthdate)
    player_zodiacs.append(captain_zodiac)
    print(f"The captain's zodiac is {captain_zodiac}.")

    # Process the rest of the players
    for i in range(num_players):
        player_name = input(f"Enter the name of the player {i+1} for {team_name}: ")

        # Calculate numerology for the player's name
        player_name_numerology = calculate_numerology(player_name, letterConversions)

        if player_name_numerology in {1, 3, 4, 11, 22, 33}:
            player_points += 1
            print(f"Player {player_name} earns 1 point for the team based on numerology.")
        elif player_name_numerology == 7:
            player_points -= 1
            print(f"Player {player_name} loses 1 point for the team based on numerology.")

        # Get player's birthdate and process it
        player_birthdate = input(f"Enter birthdate for player {i+1} (format: dd/mm/yyyy): ")
        day, month, year = map(int, player_birthdate.split('/'))

        secondary_energy = calculate_secondary_energy(day)
        primary_energy = calculate_primary_energy(day, month, year)

        player_zodiac = calculate_zodiac(player_birthdate)
        player_zodiacs.append(player_zodiac)

        print(f"Player {i+1}: Secondary Energy = {secondary_energy}, Primary Energy = {primary_energy}, Zodiac = {player_zodiac}")

        # Add point if energies are 1 or 11
        if secondary_energy in [1, 11] or primary_energy in [1, 11]:
            player_points += 1

    return player_points, player_zodiacs


def calculate_zodiac_points(team_zodiac, player_zodiacs, manager_zodiac):
    zodiac_friendships = {
        "Rat": ["Dragon", "Monkey"], "Ox": ["Snake", "Rooster"], "Tiger": ["Horse", "Dog"],
        "Cat": ["Goat", "Pig"], "Dragon": ["Rat", "Monkey"], "Snake": ["Rooster", "Ox"],
        "Horse": ["Tiger", "Dog"], "Goat": ["Cat", "Pig"], "Monkey": ["Dragon", "Rat"],
        "Rooster": ["Snake", "Ox"], "Dog": ["Tiger", "Horse"], "Pig": ["Cat", "Goat"]
    }
    zodiac_enemies = {
        "Rat": ["Horse", "Goat"], "Ox": ["Goat", "Horse"], "Tiger": ["Monkey", "Snake"],
        "Cat": ["Rooster", "Dragon"], "Dragon": ["Cat", "Dog"], "Snake": ["Pig", "Tiger"],
        "Horse": ["Rat", "Ox"], "Goat": ["Ox", "Rat"], "Monkey": ["Tiger", "Pig"],
        "Rooster": ["Cat", "Dog"], "Dog": ["Dragon", "Rooster"], "Pig": ["Snake", "Monkey"]
    }

    points = 0

    # Check manager zodiac vs team zodiac
    if manager_zodiac == team_zodiac:
        points += 2
    elif manager_zodiac in zodiac_friendships.get(team_zodiac, []):
        points += 1
    elif manager_zodiac in zodiac_enemies.get(team_zodiac, []):
        points -= 1

    # Check player zodiacs vs team zodiac
    for player_zodiac in player_zodiacs:
        if player_zodiac == team_zodiac:
            points += 2
        elif player_zodiac in zodiac_friendships.get(team_zodiac, []):
            points += 1
        elif player_zodiac in zodiac_enemies.get(team_zodiac, []):
            points -= 1

    return points

def calculate_zodiac(birthdate):
    day, month, year = map(int, birthdate.split('/'))
    
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    else:
        return "Capricorn"


home_team_name = input("Enter home team first name: ") + " " + input("Enter home team second name: ")
away_team_name = input("Enter away team first name: ") + " " + input("Enter away team second name: ")

home_team_founding_year = int(input("Enter home team's founding year: "))
away_team_founding_year = int(input("Enter away team's founding year: "))

# Calculate numerology for team names
home_team_numerology = calculate_numerology(home_team_name, letterConversions)
away_team_numerology = calculate_numerology(away_team_name, letterConversions)

home_team_zodiac = get_zodiac_sign(home_team_founding_year)
away_team_zodiac = get_zodiac_sign(away_team_founding_year)

# Manager info
home_manager_name_points, home_manager_birthdate_points, home_manager_zodiac = process_manager_info("Home Team")
away_manager_name_points, away_manager_birthdate_points, away_manager_zodiac = process_manager_info("Away Team")

# Player info
home_team_players = int(input("Enter the number of players in the home team: "))
away_team_players = int(input("Enter the number of players in the away team: "))

home_player_points, home_player_zodiacs = process_team_players("Home Team", home_team_players)
away_player_points, away_player_zodiacs = process_team_players("Away Team", away_team_players)

# Zodiac points
home_team_zodiac_points = calculate_zodiac_points(home_team_zodiac, home_player_zodiacs, home_manager_zodiac)
away_team_zodiac_points = calculate_zodiac_points(away_team_zodiac, away_player_zodiacs, away_manager_zodiac)

# Summing points for each team
home_team_total_points = (
    home_manager_name_points + home_manager_birthdate_points + home_player_points
    + home_team_numerology + home_team_zodiac_points
)
away_team_total_points = (
    away_manager_name_points + away_manager_birthdate_points + away_player_points
    + away_team_numerology + away_team_zodiac_points
)

# Output final points and declare winner
print(f"Home Team ({home_team_name}) Total Points: {home_team_total_points}")
print(f"Away Team ({away_team_name}) Total Points: {away_team_total_points}")

if home_team_total_points > away_team_total_points:
    print("Home Team is likely to win!")
elif away_team_total_points > home_team_total_points:
    print("Away Team is likely to win!")
else:
    print("The match is likely to be a draw!")
