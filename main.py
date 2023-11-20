import pandas as pd

from positions import calculate_value
from settigs import INPUT_FILE, OUTPUT_FILE


def main():
    input_html = INPUT_FILE
    output_html = OUTPUT_FILE

    # Read HTML file exported by FM - in this case an example of an output from the squad page
    # This reads as a list, not a dataframe
    squad_rawdata_list = pd.read_html(input_html, header=0, encoding="utf-8", keep_default_na=False)

    # turn the list into a dataframe
    squad_rawdata = squad_rawdata_list[0]

    # Calculate simple speed and workrate scores
    squad_rawdata['Spd'] = ( squad_rawdata['Pac'] + squad_rawdata['Acc'] ) / 2
    squad_rawdata['Work'] = ( squad_rawdata['Wor'] + squad_rawdata['Sta'] ) / 2
    squad_rawdata['SetP'] = ( squad_rawdata['Jum'] + squad_rawdata['Bra'] ) / 2

    # calculates gk score
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
    html = generate_html(current_squad)
    open(output_html, "w", encoding="utf-8").write(html)

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