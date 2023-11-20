import pandas as pd

from positions import calculate_value
from settigs import INPUT_FILE, OUTPUT_FILE


def main():
    input_html = INPUT_FILE
    output_html = OUTPUT_FILE

    # Read HTML file exported by FM - in this case an example of an output from the squad page
    # This reads as a list, not a dataframe
    squad_rawdata = pd.read_html(input_html, header=0, encoding="utf-8", keep_default_na=False)[0]

    # Calculate simple speed and workrate scores
    squad_rawdata = calculate_extra_attributes(squad_rawdata)

    # calculates per position
    squad_rawdata = calculate_value("gk", squad_rawdata)
    squad_rawdata = calculate_value("lb/rb", squad_rawdata)
    squad_rawdata = calculate_value("cb", squad_rawdata)
    squad_rawdata = calculate_value("cm-bbm", squad_rawdata)
    squad_rawdata = calculate_value("cm-dlp", squad_rawdata)
    squad_rawdata = calculate_value("lw", squad_rawdata)
    squad_rawdata = calculate_value("rw", squad_rawdata)
    squad_rawdata = calculate_value("st-pf", squad_rawdata)
    squad_rawdata = calculate_value("st-af", squad_rawdata)


    # builds squad dataframe using only columns that will be exported to HTML
    current_squad = squad_rawdata[['Inf','Name','Age','Position', 'Nat', '2nd Nat', 'Transfer Value', 'Spd','Jum','Str','Work','Height','gk','lb_rb', 'cb', 'cm_bbm', 'cm_dlp', 'lw', 'rw', 'st_pf', 'st_af']]
    #shortlist = squad_rawdata[['Inf','Name','Age','Position', 'Club','Transfer Value','Nat','Position','Personality','Left Foot', 'Right Foot','Spd','Jum','Str','Work','Height','gk','lb_rb', 'cb', 'cm_bbm', 'cm_dlp', 'lw', 'rw', 'st_pf', 'st_af']]

    # creates a sortable html export from the dataframe 'squad'
    generate_output(current_squad, output_html)

    # Calculate Position HTML
    for pos in ["gk", "lb", "cb", "rb", "cm", "lw", "rw", "st"]:
        calculate_position(pos)

def calculate_extra_attributes(data):
    data['Spd'] = ( data['Pac'] + data['Acc'] ) / 2
    data['Work'] = ( data['Wor'] + data['Sta'] ) / 2
    data['SetP'] = ( data['Jum'] + data['Bra'] ) / 2

    return data


def calculate_position(position):
    # Calculate Position HTML
    data = pd.read_html(f"input/{position.upper()}.html", header=0, encoding="utf-8", keep_default_na=False)[0]
    data = calculate_extra_attributes(data)

    if position in ["lb", "rb"]:
        data = calculate_value("lb/rb", data)
        squad = data[
            ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', "lb_rb", 'Apps', 'Gls',
             'Ast', 'Av Rat']]

    elif position in ["cm"]:
        data = calculate_value("cm-bbm", data)
        data = calculate_value("cm-dlp", data)
        squad = data[
            ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', "cm_bbm", "cm_dlp", 'Apps', 'Gls',
             'Ast', 'Av Rat']]
    elif position in ["st"]:
        data = calculate_value("st-pf", data)
        data = calculate_value("st-af", data)
        squad = data[
            ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', "st_pf", "st_af", 'Apps',
             'Gls', 'Ast', 'Av Rat']]
    else:
        data = calculate_value(position, data)
        squad = data[
            ['Inf', 'Name', 'Age', 'Position', 'Height', 'Nat', '2nd Nat', 'Transfer Value', position, 'Apps', 'Gls', 'Ast',
             'Av Rat']]
    generate_output(squad, f"output/{position.upper()}.html")

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
                order: [[12, 'desc']],
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    main()