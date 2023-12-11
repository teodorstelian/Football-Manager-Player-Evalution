INPUT_FILE = "input/Team.html"
OUTPUT_FILE = "output/General_Output.html"
POSITIONS = ["GK", "LB", "RB", "CB", "CM", "LW", "RW", "ST"]
CURRENT_NATION = "ITA"
DIVISIONS = {
    'ITA': ['Serie A', 'Serie B', 'Serie C', 'Serie D'],
    'FRE': ['Ligue 1', 'Ligue 2', 'Ligue 3'],
}
ATTRIB_TO_KEEP_GENERAL = ['Inf', 'Name', 'Age', 'Position', 'Nat', '2nd Nat', 'Transfer Value', 'GK', 'LB',
                             'CB', 'RB', 'CM', 'LW', 'RW', 'ST', 'Total_Apps', 'Gls', 'Ast', 'Av Rat']
ATTRIB_TO_KEEP_SET_PIECES = ['Inf', 'Name', 'Age', 'Position', 'Nat', '2nd Nat', 'Transfer Value', 'Fre', 'Pen', 'Cor']