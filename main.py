import re

import pandas as pd

from positions import calculate_value
from settings import *


def main():
    input_html = INPUT_FILE
    output_general_html = OUTPUT_GENERAL_FILE
    output_setpieces_html = OUTPUT_SETPIECES_FILE
    all_positions = ALL_POSITIONS

    # Read HTML file exported by FM - in this case an example of an output from the squad page
    # This reads as a list, not a dataframe
    squad_rawdata = pd.read_html(input_html, header=0, encoding="utf-8", keep_default_na=False)[0]

    # Calculate simple speed and workrate scores
    squad_rawdata = calculate_extra_attributes(squad_rawdata)

    # calculates per position
    for pos in all_positions:
        squad_rawdata = calculate_value(pos, squad_rawdata)

    squad_rawdata["First_11"], squad_rawdata["Subs"], squad_rawdata["Total_Apps"] = calculate_appereances(
        squad_rawdata["Apps"])
    # builds squad dataframe using only columns that will be exported to HTML
    squad_general = squad_rawdata[
        ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', 'GK', 'LB', 'CB', 'RB', 'CM',
         'LW', 'RW', 'ST', 'Total_Apps', 'Gls', 'Ast', 'Av Rat']]

    squad_set_pieces = squad_rawdata[
        ['Name', 'Age', 'Position', 'Nat', '2nd Nat', 'Transfer Value', 'Fre', 'Pen', 'Cor']]

    # creates a sortable html export from the dataframe 'squad'
    generate_output(squad_general, output_general_html)
    generate_output(squad_set_pieces, output_setpieces_html)

    # Calculate Position HTML
    for pos in all_positions:
        calculate_position(pos)


def calculate_extra_attributes(data):
    data['Spd'] = (data['Pac'] + data['Acc']) / 2
    data['Work'] = (data['Wor'] + data['Sta']) / 2
    data['SetP'] = (data['Jum'] + data['Bra']) / 2

    return data


def calculate_appereances(apps):
    first_11, sub, total_apps = [], [], []
    values = list(apps)

    # Process each match and append values to the lists
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


def calculate_position(position):
    # Calculate Position HTML
    data = pd.read_html(f"input/{position}.html", header=0, encoding="utf-8", keep_default_na=False)[0]
    data = calculate_extra_attributes(data)

    data["First_11"], data["Subs"], data["Total_Apps"] = calculate_appereances(data["Apps"])

    data = calculate_value(position, data)
    squad = data[
            ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', 'Club', position,
             'Total_Apps', 'Gls', 'Ast', 'Av Rat']]
    generate_output(squad, f"output/{position}.html")


def generate_output(squad, html):
    generated_html = generate_html(squad)
    open(html, "w", encoding="utf-8").write(generated_html)


# taken from here: https://www.thepythoncode.com/article/convert-pandas-dataframe-to-html-table-python
# creates a function to make a sortable html export

def generate_html(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
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
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    main()
