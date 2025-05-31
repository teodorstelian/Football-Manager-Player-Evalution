import pandas as pd

from src import settings

ALL_POSITIONS = settings.POSITIONS

def generate_html(
    squad_general,
    squad_set_pieces,
    squad_national_team,
    squad_versatility,
    position_tables,
    html
):
    """Generate HTML with tabs and DataTables for the given dataframes and position tables."""
    # Filter players with high potential
    squad_high_potential = squad_general[
        (squad_general['PA'] >= settings.WONDERKID_POTENTIAL_THRESHOLD) &
        (squad_general['Age'] <= settings.WONDERKID_AGE_THRESHOLD)
    ]

    # Filter players with high versatility
    squad_high_versatility = squad_general[
        (squad_general['Vers'] >= settings.VERSATILITY_THRESHOLD)
    ]

    # Convert 'Caps' and 'Youth Apps' to numeric, coercing errors to NaN
    squad_national_team['Caps'] = pd.to_numeric(squad_national_team['Caps'], errors='coerce')
    squad_national_team['Yth Apps'] = pd.to_numeric(squad_national_team['Yth Apps'], errors='coerce')
    squad_national_team['Yth Apps'] = squad_national_team['Yth Apps'].fillna(0).astype(int)

    # Filter for national team
    squad_national_team_filtered = squad_national_team[
        (squad_national_team['Caps'] > 0) | (squad_national_team['Yth Apps'] > 0)
    ]

    # Generate HTML tables
    table_general_html = squad_general.to_html(classes="table", index=False, table_id="table_general")
    table_wonderkids_html = squad_high_potential.to_html(classes="table", index=False, table_id="table_wonderkids")
    table_set_pieces_html = squad_set_pieces.to_html(classes="table", index=False, table_id="table_set_pieces")
    table_national_team_html = squad_national_team_filtered.to_html(classes="table", index=False, table_id="table_national_team")
    table_versatility_html = squad_high_versatility.to_html(classes="table", index=False, table_id="table_versatility")  # New
    position_tables_html = {
        pos: table.to_html(classes="table", index=False, table_id=f"table_{pos.lower()}")
        for pos, table in position_tables.items()
    }

    # Generate HTML structure with tabs
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
                <a class="nav-link" id="wonderkids-tab" data-toggle="tab" href="#wonderkids">Wonderkids</a>
            </li>
            {"".join(f'<li class="nav-item"><a class="nav-link" id="{pos.lower()}-tab" data-toggle="tab" href="#{pos.lower()}">{pos}</a></li>' for pos in ALL_POSITIONS)}
            <li class="nav-item">
                <a class="nav-link" id="set-pieces-tab" data-toggle="tab" href="#set-pieces">Set Pieces</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="national-team-tab" data-toggle="tab" href="#national-team">National Team</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="versatility-tab" data-toggle="tab" href="#versatility">Versatility</a>
            </li>
        </ul>

        <div class="tab-content">
            <div class="tab-pane fade show active" id="general">
                {table_general_html}
            </div>
            <div class="tab-pane fade" id="wonderkids">
                {table_wonderkids_html}
            </div>
            {"".join(f'<div class="tab-pane fade" id="{pos.lower()}">{position_tables_html[pos]}</div>' for pos in ALL_POSITIONS)}
            <div class="tab-pane fade" id="set-pieces">
                {table_set_pieces_html}
            </div>
            <div class="tab-pane fade" id="national-team">
                {table_national_team_html}
            </div>
            <div class="tab-pane fade" id="versatility">
                {table_versatility_html}
            </div>
        </div>

        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js"></script>
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
        <script>
            $(document).ready(function() {{
                $('#table_general').DataTable({{ paging: false, order: [[5, 'desc']] }});
                $('#table_wonderkids').DataTable({{ paging: false, order: [[5, 'desc']] }});
                {"".join(f"$('#table_{pos.lower()}').DataTable({{ paging: false, order: [[7, 'desc']] }});" for pos in ALL_POSITIONS)}
                $('#table_set_pieces').DataTable({{ paging: false, order: [[5, 'desc']] }});
                $('#table_national_team').DataTable({{ paging: false, order: [[6, 'desc']] }});
                $('#table_versatility').DataTable({{ paging: false, order: [[3, 'desc']] }});  // Adjust index based on versatility columns

                $('#myTabs a').on('shown.bs.tab', function (e) {{
                    $.fn.dataTable.tables({{ visible: true, api: true }}).columns.adjust();
                }});
            }});
        </script>
    </body>
    </html>
    """
    open(html, "w", encoding="utf-8").write(generated_html)
