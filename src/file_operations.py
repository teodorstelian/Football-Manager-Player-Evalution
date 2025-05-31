import pandas as pd
from pathlib import Path

from positions import calculate_value
from src import settings
from src.html_generation import generate_html
from src.utils import calculate_extra_attributes, calculate_left_right_foot_attributes, calculate_appearances, \
    calculate_position

ALL_POSITIONS = settings.POSITIONS

def remove_input_file(input_file):
    input_file_path = Path(input_file)
    try:
        input_file_path.unlink()  # This removes the file
        print(f"Successfully deleted the input file: {input_file}")
    except Exception as e:
        print(f"Error deleting file {input_file}: {e}")

def read_html_data(file_path):
    """Read HTML data from the specified file."""
    return pd.read_html(file_path, header=0, encoding="utf-8", keep_default_na=False)[0]

def run_evaluation(input_file, output_file):
    # Read raw data from HTML file
    squad_rawdata = read_html_data(input_file)

    # Calculate additional attributes
    squad_rawdata = calculate_extra_attributes(squad_rawdata)

    # Calculate left and right foot attributes
    squad_rawdata = calculate_left_right_foot_attributes(squad_rawdata)

    # Calculate Appearances
    squad_rawdata["First_11"], squad_rawdata["Subs"], squad_rawdata["Total_Apps"] = calculate_appearances(
        squad_rawdata["Apps"])

    position_tables = {}
    # Calculate values and generates html for each position
    for pos in ALL_POSITIONS:
        squad_rawdata = calculate_value(pos, squad_rawdata)
        position_tables[pos] = calculate_position(pos, squad_rawdata)

    # Prepare dataframes for general squad and set pieces
    squad_general = squad_rawdata[settings.ATTRIB_TO_KEEP_GENERAL]
    squad_set_pieces = squad_rawdata[settings.ATTRIB_TO_KEEP_SET_PIECES]
    squad_national_team = squad_rawdata[settings.ATTRIB_TO_KEEP_NATIONAL_TEAM]
    squad_versatility = squad_rawdata[settings.ATTRIB_TO_KEEP_VERSATILITY]

    # Generate HTML and write to a file containing multiple tables
    generate_html(squad_general, squad_set_pieces, squad_national_team, squad_versatility, position_tables, output_file)
