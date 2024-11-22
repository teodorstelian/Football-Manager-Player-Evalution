import re
import pandas as pd
import numpy as np
from pathlib import Path

import settings
from positions import calculate_value


ALL_POSITIONS = settings.POSITIONS


def main():

    input_folder = Path(__file__).parent / settings.INPUT_FOLDER
    output_folder = Path(__file__).parent / settings.OUTPUT_FOLDER

    for input_file in input_folder.glob("*.html"):
        output_file = output_folder / input_file.name
        run_evaluation(input_file, output_file)

def run_evaluation(input_file, output_file):
    # Read raw data from HTML file
    squad_rawdata = read_html_data(input_file)

    # Calculate additional attributes
    squad_rawdata = calculate_extra_attributes(squad_rawdata)

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

    # Generate HTML and write to a file containing multiple tables
    generate_html(squad_general, squad_set_pieces, squad_national_team, position_tables, output_file)


def read_html_data(file_path):
    """Read HTML data from the specified file."""
    return pd.read_html(file_path, header=0, encoding="utf-8", keep_default_na=False)[0]


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

    # # Use .apply to split each element of the 'Position' column
    # value_split = data["Position"].apply(lambda x: x.split(", "))
    #
    # # Create a DataFrame from the split values
    # split_df = pd.DataFrame(value_split.tolist(), columns=[f'Position{i + 1}' for i in range(value_split.apply(len).max())])
    # # Replace missing values with "No other position"
    # split_df.replace({None: "No other position"}, inplace=True)
    #
    # # Concatenate the new DataFrame with the original DataFrame
    # data = pd.concat([data, split_df], axis=1)

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
        f"Average {divisions[3]} player"
    ]

    msg = np.select(condition_mask, msg_options)

    data["European Status"] = msg
    return data



def generate_html(squad_general, squad_set_pieces, squad_national_team, position_tables, html):
    """Generate HTML with tabs and DataTables for the given dataframes and position tables."""
    table_general_html = squad_general.to_html(classes="table", index=False, table_id="table_general")
    table_set_pieces_html = squad_set_pieces.to_html(classes="table", index=False, table_id="table_set_pieces")
    table_national_team_html = squad_national_team.to_html(classes="table", index=False, table_id="table_national_team")
    position_tables_html = {pos: table.to_html(classes="table", index=False, table_id=f"table_{pos.lower()}") for
                            pos, table in position_tables.items()}

    generated_html = f"""
    <html>
    <head>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <ul class="nav nav-tabs" id="myTabs">
            <li class="nav-item">
                <a class="nav-link active" id="general-tab" data-toggle="tab" href="#general">General Squad</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="set-pieces-tab" data-toggle="tab" href="#set-pieces">Set Pieces</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="national-team-tab" data-toggle="tab" href="#national-team">National Team</a>
            </li>
            {"".join(f'<li class="nav-item"><a class="nav-link" id="{pos.lower()}-tab" data-toggle="tab" href="#{pos.lower()}">{pos}</a></li>' for pos in ALL_POSITIONS)}
        </ul>

        <div class="tab-content">
            <div class="tab-pane fade show active" id="general">
                {table_general_html}
            </div>
            <div class="tab-pane fade" id="set-pieces">
                {table_set_pieces_html}
            </div>
             <div class="tab-pane fade" id="national-team">
                {table_national_team_html}
            </div>
            {"".join(f'<div class="tab-pane fade" id="{pos.lower()}">{position_tables_html[pos]}</div>' for pos in ALL_POSITIONS)}
        </div>

        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
        <script>
            $(document).ready(function() {{
                $('#table_general').DataTable({{ paging: false, order: [[5, 'desc']] }});
                $('#table_set_pieces').DataTable({{ paging: false, order: [[5, 'desc']] }});
                $('#table_national_team').DataTable({{ paging: false, order: [[6, 'desc']] }});
                {"".join(f"$('#table_{pos.lower()}').DataTable({{ paging: false, order: [[7, 'desc']] }});" for pos in ALL_POSITIONS)}

                $('#myTabs a').on('shown.bs.tab', function (e) {{
                    $.fn.dataTable.tables({{ visible: true, api: true }}).columns.adjust();
                }});
            }});
        </script>
    </body>
    </html>
    """
    open(html, "w", encoding="utf-8").write(generated_html)


if __name__ == "__main__":
    main()
