from pathlib import Path
from datetime import datetime
from distutils.util import strtobool
from typing import List


class BabelFiler:
    PARENT_DIR = "babel_data"

    def __init__(
            self, src_file: str, output_file: str = None,
            trans_lang: str = None):
        self.src_file: str = src_file
        self.output_file: str = output_file
        self.trans_lang: str = trans_lang

    def __str__(self):
        return f"BabelMaker({self.src_file}: 'path_to_input', " \
               f"{self.output_file}: 'path_to_output_file', " \
               f"{self.lang}:'selected language to translate file."

# Instance Methods

    def make_dir(self) -> str:
        parent_dir = self._get_cwd() / str(self.PARENT_DIR)

        try:
            parent_dir.mkdir()
        except FileExistsError as dir_error:
            print(Warning(f"Directory already exists: {dir_error}"))
            return str(parent_dir)
        else:
            print(f"{str(parent_dir)} was created.")
            return str(parent_dir)

    def make_file(self, suffix: str = ".txt") -> str:
        try:
            suffix = suffix.replace(".", "")

        except (ValueError, TypeError, AttributeError) as error:
            new_suffix = "txt"
            print(f"Change file suffix from {suffix} to {new_suffix}\n"
                  f":{error}")
            suffix = new_suffix

        self.output_file = BabelFiler._clean_name(
            file_name = str(self.output_file))

        file_name = str(self._get_cwd() / self.PARENT_DIR /
                        f"{self.output_file}.{suffix}")

        if BabelFiler._filepath_existence(file_name):
            print(f"File exists already to a make new entry in file use the "
                  f"write to file method. Path to existent file is "
                  f"{str(file_name)}")
        else:
            print(file_name)
            with open(str(file_name), "a+") as f:
                almost_now = datetime.now()
                time_stamp = almost_now.strftime("%Y/%m/%d, %H:%M:%S")
                f.write(f"# Creation date:{time_stamp} #\n")
                f.close()

        self.output_file = str(file_name)
        return str(file_name)

    def write_to_file(self, text: str = "# New line #") -> str:

        if not(BabelFiler._filepath_existence(self.output_file)):
            print("Run make_file before adding data to file")

        else:
            write_to_file = Path(self.output_file)
            date = datetime.now()
            timestamp = date.strftime("%Y/%m/%d -- %H:%M:%S")
            write_to_file.open("a+", encoding="utf-8").write(
                f"#New Entry {timestamp} #\n{text}\n##End of Entry##\n\n"
            )

            return f"Text added to\n: {str(write_to_file)}"

    # Static methods.
    @staticmethod
    def interactive_writing():
        lines: List[str] = list()
        text = input("Press <ENTER>- key to exit interactive text mode or "
                     "enter text here:\n ")

        lines.append(text)
        while True:
            try:
                choice = strtobool(input("Do you want enter more text? ["
                                   "Y/N]"))
            except ValueError as error:
                print(f"Valid inputs are yes, y, 1 or no, n, 0.\n\n**User "
                      f"input resulted in the following output:{error}\n\n**")
                continue

            if choice:
                more_text = input()
                lines.append(more_text)
            else:
                return "\n".join(lines)

    @staticmethod
    def _get_cwd() -> object:
        return Path.cwd()

    @staticmethod
    def read_file(src_file: str):
        if not(BabelFiler._filepath_existence(src_file)):
            print(f"File does not exist please create file with make_file "
                  f"method or pick another file. Input file named"
                  f"{src_file}.\n\n")
        else:
            open_file = Path(src_file)
            with open_file.open(mode="r") as f:
                for line in f:
                    yield line.rstrip("\n")

    @staticmethod
    def _filepath_existence(path_to_file: str) -> bool:
        file_test = Path(path_to_file)
        while True:
            try:
                file_test.open("r")

            except (FileNotFoundError, IsADirectoryError) as error:
                print(f"File named called -> {file_test} was not found! File "
                      f"name resulted in: {str(error)} or press <Enter> -key "
                      f"to proceed.")
                new_file = input("Enter an existent file and path to it "
                                 "-->: ")
                file_test = Path(new_file)
                choice = strtobool(input("Do you want to create a new file?: "
                                         "[Y/N] "))
                if choice:
                    return False

                else:
                    continue

            else:
                return file_test.exists()

    @staticmethod
    def _clean_name(file_name: str) -> str:
        path_to_file = Path(file_name).name

        if path_to_file.count("."):
            path_to_file = path_to_file[:path_to_file.find(".")]
        try:
            path_to_file[0]

        except (ValueError, IndexError) as error:
            print(f"Changing values from '{file_name}' to 'untitled' to "
                  f"resolve conflict -> {error}")
            path_to_file = "untitled"
            return path_to_file
        else:
            return path_to_file
