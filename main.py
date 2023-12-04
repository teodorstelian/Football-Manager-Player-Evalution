import re
import pandas as pd
import numpy as np

import settings
from positions import calculate_value

# Constants for file paths and column names
INPUT_FILE = settings.INPUT_FILE
OUTPUT_GENERAL_FILE = settings.OUTPUT_GENERAL_FILE
OUTPUT_SETPIECES_FILE = settings.OUTPUT_SETPIECES_FILE
ALL_POSITIONS = settings.ALL_POSITIONS

def main():
    # Read raw data from HTML file
    squad_rawdata = read_html_data(INPUT_FILE)

    # Calculate additional attributes
    squad_rawdata = calculate_extra_attributes(squad_rawdata)

    # Calculate Appearances
    squad_rawdata["First_11"], squad_rawdata["Subs"], squad_rawdata["Total_Apps"] = calculate_appearances(
        squad_rawdata["Apps"])

    # Calculate values and generates html for each position
    for pos in ALL_POSITIONS:
        squad_rawdata = calculate_value(pos, squad_rawdata)
        calculate_position(pos)

    # Prepare dataframes for general squad and set pieces
    squad_general = prepare_squad_dataframe(squad_rawdata)
    squad_set_pieces = prepare_set_pieces_dataframe(squad_rawdata)

    # Generate HTML and write to files for general squad and set pieces
    generate_output(squad_general, OUTPUT_GENERAL_FILE)
    generate_output(squad_set_pieces, OUTPUT_SETPIECES_FILE)


def read_html_data(file_path):
    """Read HTML data from the specified file."""
    return pd.read_html(file_path, header=0, encoding="utf-8", keep_default_na=False)[0]

def calculate_extra_attributes(data):
    """Calculate additional attributes."""
    data['Spd'] = (data['Pac'] + data['Acc']) / 2
    data['Work'] = (data['Wor'] + data['Sta']) / 2
    data['SetP'] = (data['Jum'] + data['Bra']) / 2
    return data

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

def prepare_squad_dataframe(data):
    """Prepare dataframe for general squad."""
    columns_to_keep = ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', 'GK', 'LB', 'CB', 'RB', 'CM', 'LW', 'RW', 'ST', 'Total_Apps', 'Gls', 'Ast', 'Av Rat']
    return data[columns_to_keep]

def prepare_set_pieces_dataframe(data):
    """Prepare dataframe for set pieces."""
    columns_to_keep = ['Name', 'Age', 'Position', 'Nat', '2nd Nat', 'Transfer Value', 'Fre', 'Pen', 'Cor']
    return data[columns_to_keep]

def calculate_position(position):
    """Calculate values and generate HTML for a specific position."""
    data = read_html_data(f"input/{position}.html")
    data = calculate_extra_attributes(data)

    data["First_11"], data["Subs"], data["Total_Apps"] = calculate_appearances(data["Apps"])

    data = calculate_value(position, data)
    data = calculate_league_standard(position, data, settings.CURRENT_NATION)

    squad = data[['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', 'Club', position, 'Total_Apps', 'Gls', 'Ast', 'Av Rat', 'Status']]
    generate_output(squad, f"output/{position}.html")

def calculate_league_standard(position, data, country):
    """Calculate league standard and assign status."""
    divisions = settings.DIVISIONS.get(country, [])

    value_at_position = data[position]

    condition_mask = [
        value_at_position > 18,
        value_at_position > 16,
        value_at_position > 14.5,
        value_at_position > 13,
        value_at_position > 12,
        value_at_position > 11,
        value_at_position > 10,
        value_at_position > 9,
        value_at_position > 8,
        value_at_position <= 8
    ]

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
    ]

    msg = np.select(condition_mask, msg_options)

    data["Status"] = msg
    return data

def generate_output(squad, html):
    """Generate HTML and write to file."""
    generated_html = generate_html(squad)
    open(html, "w", encoding="utf-8").write(generated_html)

def generate_html(dataframe: pd.DataFrame):
    """Generate HTML with DataTables for the given dataframe."""
    table_html = dataframe.to_html(table_id="table", index=False)
    return f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                paging: false,
                order: [[1, 'desc']],
            }});
        }});
    </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    main()
