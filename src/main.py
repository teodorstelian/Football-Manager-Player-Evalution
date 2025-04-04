from pathlib import Path

import settings
from src.file_operations import run_evaluation, remove_input_file

def main():
    input_folder = Path(__file__).parent.parent / settings.INPUT_FOLDER
    output_folder = Path(__file__).parent.parent / settings.OUTPUT_FOLDER

    for input_file in input_folder.glob("*.html"):
        output_file = output_folder / input_file.name
        run_evaluation(input_file, output_file)
        remove_input_file(input_file)

if __name__ == "__main__":
    main()
