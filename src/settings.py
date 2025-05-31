INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

CURRENT_NATION = "BEL"

# Divisions of the countries, starting with reputation
DIVISIONS = {
    'ENG': ['1', 'Premier League', 'Championship', 'League One', 'League Two'],
    'ITA': ['1', 'Serie A', 'Serie B', 'Serie C', 'Serie D'],
    'FRA': ['1', 'Ligue 1', 'Ligue 2', 'Championnat National', 'Championnat National 2'],
    'ROM': ['3', 'SuperLiga', 'Liga 2', 'Liga 3', 'Liga 4'],
    'BEL': ['2', 'Belgian Pro League', 'Challenger Pro League', 'Belgian Division 1', 'Belgian Division 2'],
}
DIVISIONS_VALUES ={
    '1': [17, 15.5, 14, 13, 12.5, 12, 11, 10, 9, 8, 0],
    '2': [16, 14.5, 13, 12, 11, 10.5 , 9.5, 8.5, 7.5, 7, 0],
    '3': [15.5, 13.5, 12.5, 11.5, 10.5, 10 , 9, 8, 7, 6.5, 0],
}

EUROPEAN_DIVISIONS = [
    'Champions League', 'Europa League', 'Europa Conference League', 'Not good for Europe'
]

EUROPEAN_VALUES = [17, 16, 15, 14, 13.5, 13, 12.5, 12, 11.5, 10.5, 0]

ATTRIB_TO_KEEP_GENERAL = ['Inf', 'Name', 'Age', 'PA', 'Position', 'Vers', 'Nat', 'Transfer Value', 'Club', 'GK', 'LB',
                          'CB', 'RB', 'CM', 'LW', 'RW', 'ST', 'Total_Apps', 'Gls', 'Ast', 'Av Rat']
ATTRIB_TO_KEEP_SET_PIECES = ['Inf', 'Name', 'Age', 'PA', 'Position', 'Nat', 'Transfer Value', 'Fre', 'Pen', 'Cor']
ATTRIB_TO_KEEP_NATIONAL_TEAM = ['Inf', 'Name', 'Age', 'PA', 'Position', 'Nat', '2nd Nat', 'Caps', 'Goals', 'Yth Apps', 'Yth Gls']
ATTRIB_TO_KEEP_VERSATILITY = ['Inf', 'Name', 'Age', 'PA', 'Position', 'Nat', 'Transfer Value', 'Total_Apps', 'Gls', 'Ast', 'Av Rat', 'Vers']

WONDERKID_POTENTIAL_THRESHOLD = 140
WONDERKID_AGE_THRESHOLD = 23
VERSATILITY_THRESHOLD = 15

# Positions
POSITIONS = ["GK", "LB", "RB", "CB", "CM", "LW", "RW", "ST"]
GK_REGEX = 'GK'
LB_REGEX = r'D(?!M)(?:/[^/]*)*\s?\(.*L.*\)'
CB_REGEX = r'D(?!M)(?:/[^/]*)*\s?\(.*C.*\)'
RB_REGEX = r'D(?!M)(?:/[^/]*)*\s?\(.*R.*\)'
CM_REGEX = r'(?<!A)M[^)]*\([^)]*C[^)]*\)'
LW_REGEX = r'AM(?!M)/?[^/]*\(.*L.*\)'
RW_REGEX = r'AM(?!M)/?[^/]*\(.*R.*\)'
ST_REGEX = r'ST[^)]*\([^)]*C[^)]*\)'
