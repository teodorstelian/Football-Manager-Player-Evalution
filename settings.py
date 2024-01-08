INPUT_FILE = "input.html"
OUTPUT_FILE = "output.html"

CURRENT_NATION = "ROM"
# Divisions of the countries, starting with reputation
DIVISIONS = {
    'ITA': ['1', 'Serie A', 'Serie B', 'Serie C', 'Serie D'],
    'FRE': ['1', 'Ligue 1', 'Ligue 2', 'Ligue 3'],
    'ROM': ['2', 'SuperLiga', 'Liga 2', 'Liga 3', 'Liga 4'],
}
DIVISIONS_VALUES ={
    '1': [17, 15.5, 14, 13, 12.5, 12, 11, 10, 9, 8, 0],
    '2': [17, 14, 12.5, 11.5, 11, 10.5 , 9.5, 8.5, 7.5, 7, 0],
}
ATTRIB_TO_KEEP_GENERAL = ['Inf', 'Name', 'Age', 'Position', 'Nat', 'Transfer Value', 'Club', 'GK', 'LB',
                          'CB', 'RB', 'CM', 'LW', 'RW', 'ST', 'Total_Apps', 'Gls', 'Ast', 'Av Rat']
ATTRIB_TO_KEEP_SET_PIECES = ['Inf', 'Name', 'Age', 'Position', 'Nat', 'Transfer Value', 'Fre', 'Pen', 'Cor']
ATTRIB_TO_KEEP_NATIONAL_TEAM = ['Inf', 'Name', 'Age', 'Position', 'Nat', '2nd Nat', 'Caps', 'Goals', 'Yth Apps', 'Yth Gls']

# Positions
POSITIONS = ["GK", "LB", "RB", "CB", "CM", "LW", "RW", "ST"]
GK_REGEX = 'GK'
LB_REGEX = r'D(?!M)/?[^/]*\(.*L.*\)'
CB_REGEX = r'D(?!M)/?[^/]*\(.*C.*\)'
RB_REGEX = r'D(?!M)/?[^/]*\(.*R.*\)'
CM_REGEX = r'(?<!A)M[^)]*\([^)]*C[^)]*\)'
LW_REGEX = r'AM(?!M)/?[^/]*\(.*L.*\)'
RW_REGEX = r'AM(?!M)/?[^/]*\(.*R.*\)'
ST_REGEX = r'ST[^)]*\([^)]*C[^)]*\)'
