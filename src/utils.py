import re

import numpy as np

from src import settings
from src.positions import calculate_value


def calculate_extra_attributes(data):
    """Calculate additional attributes."""
    data['Spd'] = (data['Pac'] + data['Acc']) / 2
    data['Work'] = (data['Wor'] + data['Sta']) / 2
    data['SetP'] = (data['Jum'] + data['Bra']) / 2

    # Apply split and convert 'Transfer Value' for each row
    def process_transfer_value(value):
        if "-" in value:
            value_split = value.split(" - ")
            min_value, max_value = value_split[0], value_split[1]
            min_value = process_units(min_value)
            max_value = process_units(max_value)
            avg_value = (float(min_value) + float(max_value)) / 2
            avg_value_str = f"€{avg_value:.2f}M"
        else:
            new_value = process_units(value)
            avg_value_str = f"€{float(new_value):.2f}M"
        return avg_value_str

    data['Transfer Value'] = data['Transfer Value'].apply(process_transfer_value)

    return data

def calculate_left_right_foot_attributes(data):
    data['lfv'] = data['Left Foot'].apply(calc_foot_strength)
    data['rfv'] = data['Right Foot'].apply(calc_foot_strength)

    return data

def calc_foot_strength(foot):
    foot_map = {
        "Very Weak": 1,
        "Weak": 4,
        "Fairly Weak": 8,
        "Fairly Strong": 12,
        "Strong": 16,
        "Very Strong": 20
    }
    return foot_map.get(foot, 0)

def process_units(value):
    if 'K' in value:
        new_value = value.replace(',', '.').replace('€', '').replace('K', '')
        new_value = float(new_value) / 1000
    elif 'M' in value:
        new_value = value.replace(',', '.').replace('€', '').replace('M', '')
    else:
        new_value = float(value.replace('€', '')) / 1000000
    return new_value


def calculate_appearances(apps):
    """Calculate appearances, first 11, subs, and total apps."""
    first_11, sub, total_apps = [], [], []
    values = list(apps)

    for value in values:
        if value == '-':
            first_11.append(0)
            sub.append(0)
            total_apps.append(0)
        else:
            match_f11 = re.match(r'(\d+)(:\((\d+)\))?', str(value))
            match_sub = re.search(r'\((\d+)\)', str(value))
            apps_first11 = int(match_f11[1]) if match_f11[1] else 0
            apps_sub = int(match_sub[1]) if match_sub else 0
            first_11.append(apps_first11)
            sub.append(apps_sub)
            total_apps.append(apps_first11 + apps_sub)

    return first_11, sub, total_apps


def calculate_position(position, data):
    """Calculate values and generate HTML for a specific position."""

    data["First_11"], data["Subs"], data["Total_Apps"] = calculate_appearances(data["Apps"])

    data = calculate_value(position, data)
    data = calculate_league_standard(position, data, settings.CURRENT_NATION)
    data = calculate_european_standard(position, data)

    switch_dict = {
        "GK": data['Position'].str.contains(settings.GK_REGEX),
        "LB": data['Position'].str.contains(settings.LB_REGEX),
        "CB": data['Position'].str.contains(settings.CB_REGEX),
        "RB": data['Position'].str.contains(settings.RB_REGEX),
        "CM": data['Position'].str.contains(settings.CM_REGEX),
        "LW": data['Position'].str.contains(settings.LW_REGEX),
        "RW": data['Position'].str.contains(settings.RW_REGEX),
        "ST": data['Position'].str.contains(settings.ST_REGEX)
    }

    data = data[switch_dict.get(position)]

    return data[
        ['Inf', 'Name', 'Age', 'Position', 'Nat', 'Transfer Value', 'Club', position, 'Total_Apps',
         'Gls', 'Ast', 'Av Rat', 'League Status', 'European Status']]


def calculate_league_standard(position, data, country):
    """Calculate league standard and assign league status."""
    divisions = settings.DIVISIONS.get(country, [])[1:]
    division_diff = settings.DIVISIONS.get(country)[0]
    division_values = settings.DIVISIONS_VALUES.get(division_diff, [])
    value_at_position = data[position]

    condition_mask = [value_at_position >= threshold for threshold in division_values]

    msg_options = [
        "One of the best in the world",
        f"Leading {divisions[0]} player",
        f"Great {divisions[0]} player",
        f"Decent {divisions[0]} player",
        f"Leading {divisions[1]} player",
        f"Great {divisions[1]} player",
        f"Decent {divisions[1]} player",
        f"Leading {divisions[2]} player",
        f"Great {divisions[2]} player",
        f"Decent {divisions[2]} player",
        f"{divisions[3]} player"
    ]

    msg = np.select(condition_mask, msg_options)

    data["League Status"] = msg
    return data


def calculate_european_standard(position, data):
    """Calculate league standard and assign league status."""
    divisions = settings.EUROPEAN_DIVISIONS
    division_values = settings.EUROPEAN_VALUES
    value_at_position = data[position]

    condition_mask = [value_at_position >= threshold for threshold in division_values]

    msg_options = [
        "One of the best in the world",
        f"Leading {divisions[0]} player",
        f"Great {divisions[0]} player",
        f"Decent {divisions[0]} player",
        f"Leading {divisions[1]} player",
        f"Great {divisions[1]} player",
        f"Decent {divisions[1]} player",
        f"Leading {divisions[2]} player",
        f"Great {divisions[2]} player",
        f"Decent {divisions[2]} player",
        f"{divisions[3]} player"
    ]

    msg = np.select(condition_mask, msg_options)

    data["European Status"] = msg
    return data

