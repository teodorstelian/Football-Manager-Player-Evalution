import re
import pandas as pd
import numpy as np

import settings
from positions import calculate_value

# Constants for file paths and column names
INPUT_FILE = settings.INPUT_FILE
OUTPUT_FILE = settings.OUTPUT_FILE
ALL_POSITIONS = settings.POSITIONS
GENERAL_ATTRIBUTES = settings.ATTRIB_TO_KEEP_GENERAL
SET_PIECES_ATTRIBUTES = settings.ATTRIB_TO_KEEP_SET_PIECES


def main():
    # Read raw data from HTML file
    squad_rawdata = read_html_data(INPUT_FILE)

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
    squad_general = squad_rawdata[GENERAL_ATTRIBUTES]
    squad_set_pieces = squad_rawdata[SET_PIECES_ATTRIBUTES]

    # Generate HTML and write to a file containing multiple tables
    generate_html(squad_general, squad_set_pieces, position_tables, OUTPUT_FILE)


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


def calculate_position(position, data):
    """Calculate values and generate HTML for a specific position."""

    data["First_11"], data["Subs"], data["Total_Apps"] = calculate_appearances(data["Apps"])

    data = calculate_value(position, data)
    data = calculate_league_standard(position, data, settings.CURRENT_NATION)

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
        ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', 'Club', position, 'Total_Apps',
         'Gls', 'Ast', 'Av Rat', 'Status']]


def calculate_league_standard(position, data, country):
    """Calculate league standard and assign status."""
    divisions = settings.DIVISIONS.get(country, [])

    value_at_position = data[position]

    condition_mask = [
        value_at_position > 18,
        value_at_position > 16,
        value_at_position > 14.5,
        value_at_position > 13,
        value_at_position > 12.5,
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
        f"{divisions[3]} player"
    ]

    msg = np.select(condition_mask, msg_options)

    data["Status"] = msg
    return data


def generate_html(squad_general, squad_set_pieces, position_tables, html):
    """Generate HTML with tabs and DataTables for the given dataframes and position tables."""
    table_general_html = squad_general.to_html(classes="table", index=False, table_id="table_general")
    table_set_pieces_html = squad_set_pieces.to_html(classes="table", index=False, table_id="table_set_pieces")

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
            {"".join(f'<li class="nav-item"><a class="nav-link" id="{pos.lower()}-tab" data-toggle="tab" href="#{pos.lower()}">{pos}</a></li>' for pos in ALL_POSITIONS)}
        </ul>

        <div class="tab-content">
            <div class="tab-pane fade show active" id="general">
                {table_general_html}
            </div>
            <div class="tab-pane fade" id="set-pieces">
                {table_set_pieces_html}
            </div>
            {"".join(f'<div class="tab-pane fade" id="{pos.lower()}">{position_tables_html[pos]}</div>' for pos in ALL_POSITIONS)}
        </div>

        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
        <script>
            $(document).ready(function() {{
                $('#table_general').DataTable({{ paging: false, order: [[1, 'desc']] }});
                $('#table_set_pieces').DataTable({{ paging: false, order: [[1, 'desc']] }});
                {"".join(f"$('#table_{pos.lower()}').DataTable({{ paging: false, order: [[1, 'desc']] }});" for pos in ALL_POSITIONS)}

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
