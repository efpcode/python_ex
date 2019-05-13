#!/usr/bin/env python
import argparse
from datetime import datetime
from pathlib import Path


class Journal(object):
    """The Journal object formats the daily journal entries."""

    def make_markdown(self, header=str(), source_file=str()):
        log_file = Path(source_file)
        log_file = self._is_file(log_file)

        with open(f"{log_file.stem}.md", "a") as f, open(
            f"{log_file.absolute()}", "r"
        ) as r:

            f.write(f"\n# {header}\n### {self._create_date()}\n\n")
            for line in r.readlines():
                f.write(line)
            f.write("\n -- End of the day --")

    def _create_date(self):
        """Returns users local-date .i.e. users computer date.
        """
        return datetime.now().strftime("%Y-%m-%d")

    def _is_file(self, filepath):
        try:
            if not filepath.exists():
                raise FileNotFoundError

        except FileNotFoundError as error:
            text = f"File is not found in system.\n{filepath} --> {error}"
            raise FileNotFoundError(text)
        else:
            return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "header",
        help="The header of the journal entry.",
        type=str)

    parser.add_argument(
        "filename",
        help="The relative path to source/text material.",
        type=str)

    parser_args = parser.parse_args()

    my_file = Journal()
    my_file.make_markdown(header=parser_args.header, source_file=parser_args.filename)

