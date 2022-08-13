"""
Extract release notes from docs/change_log.rst.

Write notes to file:
./release_notes.txt

command line argument:
version number
"""
import argparse
import re
import sys


parser = argparse.ArgumentParser()
parser.add_argument("version_number")
args = parser.parse_args()
version_number = args.version_number
# version_components = version_number.split(".")

with open("./docs/change_log.rst", "r", encoding="utf-8") as file:
    # pass
    all_release_note_lines = file.readlines()

re_version_pattern = version_number.replace(".", "\.")

release_note_start_line = None

i = 0
for line in all_release_note_lines:
    # if re.match(f"^{re_version_pattern}$", line) is not None:
    if line.find(version_number) != -1:
        release_note_start_line = i
        break
    else:
        i += 1

if release_note_start_line is None:
    sys.exit(1)

next_release_note_start_line = None
# release_note_line_count = None

j = 0
# for line in all_release_note_lines[release_note_start_line + 1:]:
for line in all_release_note_lines:
    if j <= release_note_start_line:
        j += 1
        continue
    elif re.match("^[0-9]{1,}\.[0-9]{1,}.*", line) is not None:
        next_release_note_start_line = j
        break
    else:
        j += 1

release_note_lines = all_release_note_lines[
    release_note_start_line:next_release_note_start_line
]

with open("./release_notes.txt", "w", encoding="utf-8") as f:
    for line in release_note_lines:
        f.write(line)

sys.exit(0)
