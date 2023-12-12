INPUT_FILE = "input.html"
OUTPUT_FILE = "output.html"

CURRENT_NATION = "ITA"
DIVISIONS = {
    'ITA': ['Serie A', 'Serie B', 'Serie C', 'Serie D'],
    'FRE': ['Ligue 1', 'Ligue 2', 'Ligue 3'],
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
