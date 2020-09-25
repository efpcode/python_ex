from pathlib import Path
from datetime import datetime
from distutils.util import strtobool
from typing import List


class BabelFiler:
    parentdir = "babel_data"

    def __init__(
            self, src_file: str, output_file: str = None, 
            trans_lang: str = None):
        self.src_file: str = src_file
        self.output_file: str = output_file
        self.lang: str = trans_lang

    def __str__(self):
        return f"BabelMaker({self.src_file}: 'path_to_input', " \
               f"{self.output_file}: 'path_to_output_file', " \
               f"{self.lang}:'selected language to translate file."

# Instance Methods

    def make_dir(self) -> str:
        parent_dir = self._get_cwd() / str(self.parentdir)

        try:
            parent_dir.mkdir()
        except FileExistsError as direrror:
            print(f"Directory already exists: {direrror}")
            return str(parent_dir)
        else:
            print(f"{str(parent_dir)} was created.")
            return str(parent_dir)

    def make_file(self, suffix: str =".txt") -> str:
        try:
            suffix = suffix.replace(".", "")

        except (ValueError, TypeError, AttributeError) as error:
            new_suffix = "txt"
            print(f"Change file suffix from {suffix} to {new_suffix}\n"
                  f":{error}")
            suffix = new_suffix

        if not self.output_file:
            flag = f"{str(self.src_file)}_translated_to_{str(self.lang)}." \
                   f"{suffix}"
        else:
            flag = f"{str(self.output_file)}_translated_to" \
                   f"_{str(self.lang)}.{suffix}"

        file_name = self._get_cwd()/self.parentdir/flag
        try:
            if file_name.exists():
                raise FileExistsError
        except FileExistsError:
            print(f"File exists already to a make new entry in file use the "
                  f"write to file method. Path to existent file is "
                  f"{str(file_name)}")
        else:
            with open(str(file_name), "w") as f:
                almost_now = datetime.now()
                time_stamp = almost_now.strftime("%Y/%m/%d, %H:%M:%S")
                f.write(f"# Creation date:{time_stamp} #\n")
                f.close()

        self.output_file = str(file_name)
        return str(file_name)

    def write_to_file(self, text: str = "# New line #") -> str:
        write_to_file = Path(self.output_file)

        try:
            if not(write_to_file.exists()):
                raise FileNotFoundError
        except FileNotFoundError:
            return "Run make_file before adding text."
        else:
            write_to_file.open("a+", encoding="utf-8").write(
                f"#New Entry#\n{text}\n##End of Entry##\n\n")
        return f"Text added to\n: {str(write_to_file)}"


    # Static methods.
    @staticmethod
    def interactive_writing():
        lines: List[str] = list()
        text = input("Press <ENTER>- key to exit interactive text mode,"
                     "else enter characters here:\n ")

        lines.append(text)
        while True:
            try:
                choice = strtobool(input("Do you want enter more text? ["
                                   "Y//N]"))
            except ValueError as error:
                print(f"Valid inputs are yes, y, 1 or no, n, 0.\n\n**User "
                      f"input resulted in the following output:{error}\n\n**")
                continue

            if choice:
                more_text = input()
                lines.append(more_text)
            else:
                return "".join(lines)

    @staticmethod
    def _get_cwd() -> object:
        return Path.cwd()

    @staticmethod
    def read_file(target_name):
        open_file = Path(target_name)
        with open_file.open(mode="r") as f:
            return f.readlines()

