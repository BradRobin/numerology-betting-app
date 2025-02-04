from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

ENEMY_NUMEROLOGY_PAIRS = {(3, 4), (1, 9), (11, 9)}
# Constants for letter conversions and numerology
letterConversions = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 11, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 11, "U": 3, "V": 22, "W": 5, "X": 6, "Y": 7, "Z": 8
}

zodiac_relations = {
    "Rat": {"friends": ["Dragon", "Monkey"], "enemies": ["Horse"]},
    "Ox": {"friends": ["Snake", "Rooster"], "enemies": ["Goat"]},
    "Tiger": {"friends": ["Horse", "Dog"], "enemies": ["Monkey"]},
    "Cat": {"friends": ["Goat", "Pig"], "enemies": ["Rooster"]},
    "Dragon": {"friends": ["Rat", "Monkey"], "enemies": ["Dog"]},
    "Snake": {"friends": ["Ox", "Rooster"], "enemies": ["Pig"]},
    "Horse": {"friends": ["Tiger", "Dog"], "enemies": ["Rat"]},
    "Goat": {"friends": ["Cat", "Pig"], "enemies": ["Ox"]},
    "Monkey": {"friends": ["Rat", "Dragon"], "enemies": ["Tiger"]},
    "Rooster": {"friends": ["Ox", "Snake"], "enemies": ["Cat"]},
    "Dog": {"friends": ["Tiger", "Horse"], "enemies": ["Dragon"]},
    "Pig": {"friends": ["Goat", "Cat"], "enemies": ["Snake"]},
}

lunar_new_year_dates = {
    2024: "10/02", 2023: "22/01", 2022: "01/02", 2021: "12/02", 2020: "25/01",
    2019: "05/02", 2018: "16/02", 2017: "28/01", 2016: "08/02", 2015: "19/02",
    2014: "31/01", 2013: "10/02", 2012: "23/01", 2011: "03/02", 2010: "14/02",
    2009: "26/01", 2008: "07/02", 2007: "18/02", 2006: "29/01", 2005: "09/02",
    2004: "22/01", 2003: "01/02", 2002: "12/02", 2001: "24/01", 2000: "05/02",
    1999: "16/02", 1998: "28/01", 1997: "07/02", 1996: "19/02", 1995: "31/01",
    1994: "10/02", 1993: "23/01", 1992: "04/02", 1991: "15/02", 1990: "27/01",
    1989: "06/02", 1988: "17/02", 1987: "29/01", 1986: "09/02", 1985: "20/02",
    1984: "02/02", 1983: "13/02", 1982: "25/01", 1981: "05/02", 1980: "16/02",
    1979: "28/01", 1978: "07/02", 1977: "18/02", 1976: "31/01", 1975: "11/02",
    1974: "23/01", 1973: "03/02", 1972: "15/02", 1971: "27/01", 1970: "06/02",
    1969: "17/02", 1968: "30/01", 1967: "09/02", 1966: "21/01", 1965: "02/02",
    1964: "13/02", 1963: "25/01", 1962: "05/02", 1961: "15/02", 1960: "28/01",
    1959: "08/02", 1958: "18/02", 1957: "31/01", 1956: "12/02", 1955: "24/01",
    1954: "03/02", 1953: "14/02", 1952: "27/01", 1951: "06/02", 1950: "17/02",
    1949: "29/01", 1948: "10/02", 1947: "22/01", 1946: "02/02", 1945: "13/02",
    1944: "25/01", 1943: "04/02", 1942: "15/02", 1941: "27/01", 1940: "08/02",
    1939: "19/02", 1938: "31/01", 1937: "11/02", 1936: "24/01", 1935: "05/02",
    1934: "14/02", 1933: "26/01", 1932: "06/02", 1931: "17/02", 1930: "30/01",
    1929: "10/02", 1928: "23/01", 1927: "02/02", 1926: "13/02", 1925: "24/01",
    1924: "05/02", 1923: "16/02", 1922: "28/01", 1921: "08/02", 1920: "20/02",
    1919: "31/01", 1918: "11/02", 1917: "23/01", 1916: "03/02", 1915: "14/02",
    1914: "26/01", 1913: "06/02", 1912: "18/02", 1911: "30/01", 1910: "10/02",
    1909: "21/01", 1908: "02/02", 1907: "13/02", 1906: "25/01", 1905: "04/02",
    1904: "16/02", 1903: "29/01", 1902: "08/02", 1901: "19/02", 1900: "31/01",
    1899: "11/02", 1898: "22/01", 1897: "02/02", 1896: "13/02", 1895: "25/01",
    1894: "05/02", 1893: "15/02", 1892: "27/01", 1891: "09/02", 1890: "20/01",
    1889: "31/01", 1888: "11/02", 1887: "23/01", 1886: "03/02", 1885: "14/02",
    1884: "26/01", 1883: "06/02", 1882: "17/02", 1881: "29/01", 1880: "09/02",
    1879: "20/01", 1878: "31/01", 1877: "11/02", 1876: "22/01", 1875: "02/02",
    1874: "13/02", 1873: "24/01", 1872: "05/02", 1871: "16/02", 1870: "28/01",
    1869: "09/02", 1868: "20/01", 1867: "31/01", 1866: "12/02", 1865: "23/01",
    1864: "03/02", 1863: "14/02", 1862: "26/01", 1861: "06/02", 1860: "18/02"
}

def get_valid_zodiac_year():
    valid_zodiac_years = [
        "Rat", "Ox", "Tiger", "Cat", "Dragon", "Snake", 
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]
    while True:
        zodiac_year = input("Enter the zodiac year: ").capitalize()
        if zodiac_year in valid_zodiac_years:
            return zodiac_year
        else:
            print(f"Invalid zodiac year. Please enter one of the following: {', '.join(valid_zodiac_years)}")


# Helper Functions (kept the same as before)
def calculate_life_path(day, month, year):
    total = sum(map(int, str(day))) + sum(map(int, str(month))) + sum(map(int, str(year)))
    while total > 9 and total not in {11, 22, 33}:
        total = sum(map(int, str(total)))
    return total

def reduce_day_to_single_digit(day):
    if day in {11, 22}:
        return day
    return sum(map(int, str(day)))

def calculate_name_numerology(name):
    total = sum(letterConversions.get(char.upper(), 0) for char in name if char.isalpha())
    while total > 9 and total not in {11, 22, 33}:
        total = sum(map(int, str(total)))
    return total

def get_zodiac_sign(day, month, year):
    """
    Determine the Chinese Zodiac sign for a given birth date based on the Lunar New Year dates.
    """
    # Check if the Lunar New Year date exists for the year
    lunar_new_year_date = lunar_new_year_dates.get(year)
    if not lunar_new_year_date:
        raise ValueError(f"Lunar New Year date for the year {year} is not defined in the dataset.")

    try:
        # Extract lunar month and day
        lunar_day, lunar_month = map(int, lunar_new_year_date.split('/'))
    except ValueError:
        raise ValueError(f"Invalid Lunar New Year date format for the year {year}: {lunar_new_year_date}. Expected 'dd/mm'.")

    # Validate the month and day
    if not (1 <= lunar_month <= 12):
        raise ValueError(f"Invalid lunar month {lunar_month} in Lunar New Year date for year {year}.")

    # Create datetime objects for the birth date and Lunar New Year date
    lunar_date = datetime(year, lunar_month, lunar_day)
    birth_date = datetime(year, month, day)

    # Adjust the year if the birth date is before the Lunar New Year
    if birth_date < lunar_date:
        year -= 1  # Move to the previous zodiac year

    # List of zodiac animals in the correct order
    zodiac_animals = [
        "Rat", "Ox", "Tiger", "Cat", "Dragon", "Snake",
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]

    # Return the zodiac sign based on the adjusted year
    return zodiac_animals[year % 12]


def evaluate_zodiac_compatibility(person_zodiac, team_zodiac, today_zodiac_year):
    """Evaluate zodiac compatibility."""
    points = 0
    try:
        if person_zodiac == team_zodiac:
            points += 2
            print(f"Zodiac Match! +2 points.")
        elif person_zodiac in zodiac_relations[team_zodiac]["friends"]:
            points += 1
            print(f"Zodiac Friend! +1 point.")
        elif person_zodiac in zodiac_relations[team_zodiac]["enemies"]:
            points -= 1
            print(f"Zodiac Enemy! -1 point.")
        
        if person_zodiac in zodiac_relations[today_zodiac_year]["friends"]:
            points += 1
            print(f"Zodiac Friend of the Year! +1 point.")
        elif person_zodiac in zodiac_relations[today_zodiac_year]["enemies"]:
            points -= 1
            print(f"Zodiac Enemy of the Year! -1 point.")
    except KeyError:
        print(f"Error: Zodiac year '{today_zodiac_year}' not recognized.")
    return points


def evaluate_player_zodiac_points(player_zodiac, team_zodiac, today_zodiac_year):
    """Evaluate zodiac compatibility between player and team."""
    points = 0
    
    # General Zodiac Compatibility (team vs player)
    if player_zodiac == team_zodiac:
        points += 2  # Same zodiac: Award 2 points
        print(f"Player's Zodiac matches Team's Zodiac! +2 points.")
    elif player_zodiac in zodiac_relations[team_zodiac]["friends"]:
        points += 1  # Zodiac friends: Award 1 point
        print(f"Player's Zodiac is a Friend of the Team's Zodiac! +1 point.")
    elif player_zodiac in zodiac_relations[team_zodiac]["enemies"]:
        points -= 1  # Zodiac enemies: Deduct 1 point
        print(f"Player's Zodiac is an Enemy of the Team's Zodiac! -1 point.")
    
    # Zodiac Compatibility with the Year (today's zodiac year)
    if player_zodiac in zodiac_relations[today_zodiac_year]["friends"]:
        points += 1  # Player's zodiac is a friend of the year's zodiac
        print(f"Player's Zodiac is a Friend of the Year's Zodiac! +1 point.")
    elif player_zodiac in zodiac_relations[today_zodiac_year]["enemies"]:
        points -= 1  # Player's zodiac is an enemy of the year's zodiac
        print(f"Player's Zodiac is an Enemy of the Year's Zodiac! -1 point.")
    
    return points

def calculate_name_numerology_points(name, is_manager=True):
    """Calculate name numerology and evaluate if it matches specific numerology points."""
    # Convert the name to upper case and calculate its numerology sum based on the letterConversions dictionary
    total = sum(letterConversions.get(char.upper(), 0) for char in name if char.isalpha())
    
    # Reduce to a single digit unless it's a Master Number (11, 22, 33)
    while total > 9 and total not in {11, 22, 33}:
        total = sum(map(int, str(total)))
    
    # Print the numerology value for debugging or feedback
    print(f"Name Numerology Value: {total}")
    
    # Evaluation of the points based on numerology
    if total in {1, 3, 4, 11, 22, 33}:
        return 1  # Award 1 point if it matches the specified numerology numbers
    elif total == 7:
        return -1  # Deduct 1 point if the numerology sum is 7
    return 0  # No points if none of the conditions match


def get_valid_zodiac_year():
    valid_zodiac_years = [
        "Rat", "Ox", "Tiger", "Cat", "Dragon", "Snake", 
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]
    while True:
        zodiac_year = input("Enter the zodiac year: ").capitalize()
        if zodiac_year in valid_zodiac_years:
            return zodiac_year
        else:
            print(f"Invalid zodiac year. Please enter one of the following: {', '.join(valid_zodiac_years)}")

@app.route('/process_manager', methods=['POST'])
def process_manager_info(team_name, team_zodiac, today_life_path, today_day, today_zodiac_year):
    """Process manager details for a team."""
    # Placeholder for form inputs; Flask will pass these
    first_name = "SampleFirstName"  # Replace with form input
    last_name = "SampleLastName"  # Replace with form input
    birth_date = "01/01/2000"  # Replace with form input

    # Calculate life path and zodiac sign
    day, month, year = map(int, birth_date.split('/'))
    life_path = calculate_life_path(day, month, year)
    zodiac = get_zodiac_sign(day, month, year)

    # Calculate name numerology
    name_numerology = calculate_name_numerology(first_name + last_name)

    # Print details for debugging (or log for production)
    print(f"{team_name} Manager Name Numerology: {name_numerology}")
    print(f"{team_name} Manager Life Path: {life_path}")
    print(f"{team_name} Manager Zodiac: {zodiac}")

    # Evaluate points
    points = 0
    points += evaluate_zodiac_compatibility(zodiac, team_zodiac, today_zodiac_year)
    if life_path == today_life_path:
        points += 1

    return points


@app.route('/process_players', methods=['POST'])
def process_team_players(team_name, num_players, team_zodiac, today_life_path, today_zodiac_year, today_day, players):
    
    total_player_points = 0
    player_life_paths = []

    for i, player in enumerate(players, start=1):
        print(f"Processing player {i} for {team_name}...")

        # Retrieve player details from the `players` list
        player_name = player['name']
        player_birthdate = player['birthdate']

        try:
            day, month, year = map(int, player_birthdate.split('/'))
        except ValueError:
            print(f"Invalid birthdate format for player {i}: {player_birthdate}. Skipping player.")
            continue

        # Calculate player's life path and zodiac sign
        player_life_path = calculate_life_path(day, month, year)
        player_zodiac = get_zodiac_sign(day, month, year)
        player_life_paths.append(player_life_path)

        print(f"{team_name} Player {i} Zodiac: {player_zodiac}")
        print(f"{team_name} Player {i} Life Path: {player_life_path}")

        # Evaluate name numerology points
        name_numerology_points = calculate_name_numerology_points(player_name, is_manager=False)
        total_player_points += name_numerology_points
        if name_numerology_points != 0:
            print(f"Player {i} of {team_name} earns {name_numerology_points} point(s) from name numerology.")

        # Evaluate compatibility with today's life path
        if player_life_path == today_life_path:
            total_player_points += 1
            print(f"Player {i} of {team_name} matches today's life path! +1 point")
        elif (player_life_path, today_life_path) in ENEMY_NUMEROLOGY_PAIRS or \
             (today_life_path, player_life_path) in ENEMY_NUMEROLOGY_PAIRS:
            total_player_points -= 1
            print(f"Player {i} of {team_name} has an enemy life path with today! -1 point")

        # Evaluate compatibility with today's zodiac year
        zodiac_points = evaluate_player_zodiac_points(player_zodiac, team_zodiac, today_zodiac_year)
        total_player_points += zodiac_points
        if zodiac_points > 0:
            print(f"Player {i} of {team_name} earns {zodiac_points} point(s) for zodiac compatibility.")
        elif zodiac_points < 0:
            print(f"Player {i} of {team_name} loses {abs(zodiac_points)} point(s) for zodiac incompatibility.")

    return total_player_points, player_life_paths


# Main Route for the Web App
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get today's date and other details
        today_date = request.form['today_date']
        today_day = reduce_day_to_single_digit(int(today_date.split('/')[0]))
        today_life_path = calculate_life_path(*map(int, today_date.split('/')))
        today_zodiac_year = request.form['today_zodiac_year'].capitalize()

        # Team details input
        home_team_name = request.form['home_team_name']
        away_team_name = request.form['away_team_name']
        home_team_founding_date = request.form['home_team_founding_date']
        away_team_founding_date = request.form['away_team_founding_date']

        # Process manager info for both teams
        home_manager_points = process_manager_info(home_team_name, get_zodiac_sign(*map(int, home_team_founding_date.split('/'))), today_life_path, today_day, today_zodiac_year)
        away_manager_points = process_manager_info(away_team_name, get_zodiac_sign(*map(int, away_team_founding_date.split('/'))), today_life_path, today_day, today_zodiac_year)

        # Process home players
        home_players = []
        for i in range(1, int(request.form['num_players_home']) + 1):
            player_name = request.form.get(f"home_player_name_{i}")
            player_birthdate = request.form.get(f"home_player_birthdate_{i}")
            home_players.append({'name': player_name, 'birthdate': player_birthdate})

        # Extract total_player_points from the returned tuple
        home_player_points, _ = process_team_players(
            home_team_name, len(home_players), get_zodiac_sign(*map(int, home_team_founding_date.split('/'))),
            today_life_path, today_zodiac_year, today_day, home_players
        )

        # Process away players
        away_players = []
        for i in range(1, int(request.form['num_players_away']) + 1):
            player_name = request.form.get(f"away_player_name_{i}")
            player_birthdate = request.form.get(f"away_player_birthdate_{i}")
            away_players.append({'name': player_name, 'birthdate': player_birthdate})

        # Extract total_player_points from the returned tuple
        away_player_points, _ = process_team_players(
            away_team_name, len(away_players), get_zodiac_sign(*map(int, away_team_founding_date.split('/'))),
            today_life_path, today_zodiac_year, today_day, away_players
        )

        # Calculate total scores
        home_total_score = home_manager_points + home_player_points
        away_total_score = away_manager_points + away_player_points

        # Total scores
        home_total_score = home_manager_points + home_player_points
        away_total_score = away_manager_points + away_player_points

        # Determine the winner
        if home_total_score > away_total_score:
            winner = home_team_name
        elif away_total_score > home_total_score:
            winner = away_team_name
        else:
            winner = "It's a tie!"

        return render_template('result.html', home_team_name=home_team_name, away_team_name=away_team_name, home_total_score=home_total_score, away_total_score=away_total_score, winner=winner)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
