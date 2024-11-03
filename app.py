from functools import reduce
from datetime import datetime

# Dictionary for letter to number conversion (Numerology values)
MANAGER_LUCKY_NUMBERS = {1, 3, 4, 7, 11, 13, 22, 33}

letterConversions = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 11, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 11, "U": 3, "V": 22, "W": 5, "X": 6, "Y": 7, "Z": 8,
}

zodiac_signs = {
    0: "Monkey", 1: "Rooster", 2: "Dog", 3: "Pig", 4: "Rat", 5: "Ox",
    6: "Tiger", 7: "Cat", 8: "Dragon", 9: "Snake", 10: "Horse", 11: "Goat",
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
    "Pig": {"friends": ["Goat", "Cat"], "enemies": ["Snake"]}
}


# Lunar New Year start dates from 1860 to 2024
lunar_new_year_dates = {
    1860: "01/20", 1861: "02/08", 1862: "01/28", 1863: "02/15",
    1864: "02/03", 1865: "01/23", 1866: "02/10", 1867: "01/30",
    1868: "02/17", 1869: "02/05", 1870: "01/25", 1871: "02/12",
    1872: "02/01", 1873: "01/22", 1874: "02/10", 1875: "01/30",
    1876: "02/19", 1877: "02/07", 1878: "01/28", 1879: "02/15",
    1880: "02/05", 1881: "01/24", 1882: "02/13", 1883: "02/02",
    1884: "01/23", 1885: "02/10", 1886: "01/30", 1887: "01/20",
    1888: "02/08", 1889: "01/29", 1890: "02/16", 1891: "02/06",
    1892: "01/26", 1893: "02/14", 1894: "02/02", 1895: "01/22",
    1896: "02/10", 1897: "01/30", 1898: "02/17", 1899: "02/07",
    1900: "01/27", 1901: "02/15", 1902: "02/08", 1903: "01/29",
    1904: "02/16", 1905: "02/04", 1906: "01/25", 1907: "02/13",
    1908: "02/02", 1909: "01/22", 1910: "02/10", 1911: "01/30",
    1912: "02/18", 1913: "02/06", 1914: "01/26", 1915: "02/14",
    1916: "02/03", 1917: "01/23", 1918: "02/11", 1919: "02/01",
    1920: "02/20", 1921: "02/08", 1922: "01/28", 1923: "02/16",
    1924: "02/05", 1925: "01/24", 1926: "02/13", 1927: "02/02",
    1928: "01/23", 1929: "02/10", 1930: "01/30", 1931: "02/17",
    1932: "02/06", 1933: "01/26", 1934: "02/14", 1935: "02/04",
    1936: "01/24", 1937: "02/11", 1938: "01/31", 1939: "02/19",
    1940: "02/08", 1941: "01/27", 1942: "02/15", 1943: "02/05",
    1944: "01/25", 1945: "02/13", 1946: "02/02", 1947: "01/22",
    1948: "02/10", 1949: "01/29", 1950: "02/17", 1951: "02/06",
    1952: "01/27", 1953: "02/14", 1954: "02/03", 1955: "01/24",
    1956: "02/12", 1957: "01/31", 1958: "02/18", 1959: "02/08",
    1960: "01/28", 1961: "02/15", 1962: "02/05", 1963: "01/25",
    1964: "02/13", 1965: "02/02", 1966: "01/21", 1967: "02/09",
    1968: "01/30", 1969: "02/17", 1970: "02/06", 1971: "01/27",
    1972: "02/15", 1973: "02/03", 1974: "01/23", 1975: "02/11",
    1976: "01/31", 1977: "02/18", 1978: "02/07", 1979: "01/28",
    1980: "02/16", 1981: "02/05", 1982: "01/25", 1983: "02/13",
    1984: "02/02", 1985: "02/20", 1986: "02/09", 1987: "01/29",
    1988: "02/17", 1989: "02/06", 1990: "01/27", 1991: "02/15",
    1992: "02/04", 1993: "01/23", 1994: "02/10", 1995: "01/31",
    1996: "02/19", 1997: "02/07", 1998: "01/28", 1999: "02/16",
    2000: "02/05", 2001: "01/24", 2002: "02/12", 2003: "02/01",
    2004: "01/22", 2005: "02/09", 2006: "01/29", 2007: "02/18",
    2008: "02/07", 2009: "01/26", 2010: "02/14", 2011: "02/03",
    2012: "01/23", 2013: "02/10", 2014: "01/31", 2015: "02/19",
    2016: "02/08", 2017: "01/28", 2018: "02/16", 2019: "02/05",
    2020: "01/25", 2021: "02/12", 2022: "02/01", 2023: "01/22",
    2024: "02/10"
}

def evaluate_zodiac_points(zodiac, team_zodiac):
    points = 0
    
    # Check if the manager's or player's zodiac is the same as the team's
    if zodiac == team_zodiac:
        points += 2
    elif zodiac in zodiac_relations[team_zodiac]["friends"]:
        points += 1
    elif zodiac in zodiac_relations[team_zodiac]["enemies"]:
        points -= 1

    return points



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

def get_zodiac_sign(day, month, year):
    # Determine the Lunar New Year date for the given year
    lunar_date_str = lunar_new_year_dates.get(year)
    if not lunar_date_str:
        raise ValueError("Year not available in Lunar New Year data.")
    lunar_date = datetime.strptime(f"{year}/{lunar_date_str}", "%Y/%m/%d")
    birth_date = datetime(year, month, day)
    
    # Adjust year if birth date is before the Lunar New Year
    if birth_date < lunar_date:
        year -= 1
    return zodiac_signs[year % 12]

def calculate_secondary_energy(day):
    return reduce_to_single_digit(day)

def calculate_primary_energy(day, month, year):
    total = sum(map(int, str(day))) + sum(map(int, str(month))) + sum(map(int, str(year)))
    return reduce_to_single_digit(total)

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
    manager_zodiac = get_zodiac_sign(day, month, year)
    print(f"{team_name} Manager Zodiac: {manager_zodiac}")

    return name_points, birthdate_points, manager_zodiac

def process_team_players(team_name, num_players):
    print(f"Processing {team_name} players...")
    
    player_zodiacs = []
    player_points = 0

    for i in range(num_players):
        player_name = input(f"Enter the name of player {i+1} for {team_name}: ")
        player_name_numerology = calculate_numerology(player_name, letterConversions)

        if player_name_numerology in {1, 3, 4, 11, 22, 33}:
            player_points += 1
            print(f"Player {player_name} earns 1 point for the team based on numerology.")
        elif player_name_numerology == 7:
            player_points -= 1
            print(f"Player {player_name} loses 1 point for the team based on name numerology.")

        player_birthdate = input(f"Enter birthdate for player {i+1} (dd/mm/yyyy): ")
        day, month, year = map(int, player_birthdate.split('/'))

        player_zodiac = get_zodiac_sign(day, month, year)
        player_zodiacs.append(player_zodiac)
        print(f"Player {i+1}'s Chinese zodiac is {player_zodiac}.")

        secondary_energy = calculate_secondary_energy(day)
        primary_energy = calculate_primary_energy(day, month, year)

        player_points += 1 if secondary_energy in [1, 11] or primary_energy in [1, 11] else 0

    return player_points, player_zodiacs

def main():
    home_team_name = input("Enter the name of the first team: ")
    away_team_name = input("Enter the name of the second team: ")

    # Prompt for the full founding date of each team
    home_team_founding_date = input("Enter home team's founding date (dd/mm/yyyy): ")
    day, month, year = map(int, home_team_founding_date.split('/'))
    home_team_zodiac = get_zodiac_sign(day, month, year)
    home_team_numerology = calculate_numerology(home_team_name, letterConversions)

    away_team_founding_date = input("Enter away team's founding date (dd/mm/yyyy): ")
    day, month, year = map(int, away_team_founding_date.split('/'))
    away_team_zodiac = get_zodiac_sign(day, month, year)
    away_team_numerology = calculate_numerology(away_team_name, letterConversions)

    # Process manager information for each team
    home_manager_points, home_manager_birthdate_points, home_manager_zodiac = process_manager_info(home_team_name)
    away_manager_points, away_manager_birthdate_points, away_manager_zodiac = process_manager_info(away_team_name)

    # Process players information for each team
    num_players_home = int(input(f"Enter the number of players for {home_team_name}: "))
    home_player_points, home_player_zodiacs = process_team_players(home_team_name, num_players_home)

    num_players_away = int(input(f"Enter the number of players for {away_team_name}: "))
    away_player_points, away_player_zodiacs = process_team_players(away_team_name, num_players_away)

    home_total_score = (home_manager_points + home_manager_birthdate_points + home_player_points +
                    evaluate_zodiac_points(home_manager_zodiac, home_team_zodiac) +
                    sum(evaluate_zodiac_points(player_zodiac, home_team_zodiac) for player_zodiac in home_player_zodiacs))

    away_total_score = (away_manager_points + away_manager_birthdate_points + away_player_points +
                    evaluate_zodiac_points(away_manager_zodiac, away_team_zodiac) +
                    sum(evaluate_zodiac_points(player_zodiac, away_team_zodiac) for player_zodiac in away_player_zodiacs))

    # Output results
    print(f"{home_team_name} Total Score: {home_total_score}")
    print(f"{away_team_name} Total Score: {away_total_score}")

    if home_total_score > away_total_score:
        print(f"{home_team_name} is more likely to win!")
    elif home_total_score < away_total_score:
        print(f"{away_team_name} is more likely to win!")
    else:
        print("It's a tie!")

# Run the main function
if __name__ == "__main__":
    main()

