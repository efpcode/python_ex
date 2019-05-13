#!/usr/bin/env python

from datetime import datetime
class Journal(object):
    """The Journal formats the daily journal entries."""
    def __init__(self, header=str(), file_source=str()):
        super(Journal, self).__init__()
        self.header = header
        self.file_source = file_source

    def make_markdown(self):
        with open(f"{self.file_source}.md", "a") as f,
        open(f"{self.file_source}", "r" as r):
            f.write(self._create_date())
            f.write(f"#{self.header}\n")
            for line in r.readlines():
                f.write(line)


    def _create_date(self):
        return datatime.now().strftime("%Y-%m-%d")



