"""Generate page for context"""
import os, re
from datetime import datetime as dt
from collections import Counter


def create_page_name(dir_curr_crawl):
    return "{0}.md".format(os.path.basename(dir_curr_crawl))

def textify_grouped_notes(grouped_notes):
    def textify_created(created):
        return "**{0}**".format(created.strftime("%Y-%m-%d-%H:%M"))

    full_text = "## Notes\n\n"

    for title, notes in grouped_notes.items():
        # Sort the list first
        text = ["\n\n".join([textify_created(note[1]), note[0]]) for note in notes]
        text = "\n\n".join(text)
        full_text += "### {0}\n\n{1}\n\n".format(title, text)

    return full_text

def group_notes(grouped_notes, new_note):
    for k,v in new_note.items():
        # TODO: Support case insensitive titles
        notes = grouped_notes.get(k, [])
        grouped_notes[k] = notes + v
    return grouped_notes


def when_note_created(name_note):
    return dt.strptime(name_note.replace(".md", ""), "_%Y-%m-%d-%H%M")

def get_title_level(line):
    """Determines whether line is a title and returns the level otherwise zero"""
    if line:
        m = re.match("^[#]+$", line.split(" ")[0])
        if m:
            return len(m.group(0))
    return 0

def adjust_title_level(line, new_level):
    ls = line.split(" ")
    ls[0] = "#"*new_level
    return " ".join(ls)

def find_title_levels_distribution(text_split):
    """Return Counter object that has title level (e.g. ## is 2) to frequency"""
    title_levels = [ get_title_level(line) for line in text_split ]
    return Counter(filter(lambda tl: tl != 0, title_levels))

def get_title_level_biggest(title_levels):
    """Return the biggest title level given a Counter object of the distribution"""
    stl = sorted(list(title_levels))
    return stl[0] if stl else 0


def parse_note(note_text, created):
    # Split by \n and group sequential text by header "##"
    note_text_split = note_text.split("\n")
    title_levels = find_title_levels_distribution(note_text_split)
    biggest_level = get_title_level_biggest(title_levels)

    store = {}
    last_group = None

    for line in note_text_split:
        title_level = get_title_level(line)

        # TODO: Need to handle when a line looks like a title but its in a code
        # block
        if title_level == biggest_level:
            last_group = line.replace("#"*biggest_level, "").strip()
            continue
        elif title_level > 0:
            # Note groups start at 3 - yes hardcoded
            line = adjust_title_level(line, 3 + (title_level - biggest_level))
        else:
            if not last_group:
                last_group = "Dot dot dot"

        lines = store.get(last_group, [])
        lines.append(line)
        store[last_group] = lines

    # Join the lines by \n
    # The filter is there to strip out entries (specifically for "NOSPECIFIC"
    # case that has a single line that is actually empty
    # NOTE: Stripping white spaces for each note entry to force entries to be
    # consistent in form
    # MAYBE CHANGE STRUCTURE FOR MORE CONTRON OVER TITLE?  DICTATE HOW TITLE IS
    # SHOWN?
    result = { k: [("\n".join(v).strip(), created)] for k,v in store.items() if not(len(v) == 0
        or (len(v) == 1 and len(v[0]) == 0))}

    return result

def create_page(step, order_latest_first=True):
    dir_curr, dir_names, file_names = step

    with open(os.path.join(dir_curr, "_index.md"), "r+") as f:
        main = f.read()

    dir_notes = os.path.join(dir_curr, "_notes")
    grouped_notes = {}
    reversed_maybe = lambda n: reversed(n) if order_latest_first else n

    for name_note in reversed_maybe(sorted(os.listdir(dir_notes))):
        path_note = os.path.join(dir_notes, name_note)

        with open(path_note, "r+") as f:
            created = when_note_created(name_note)
            new_note = parse_note(f.read(), created)
            grouped_notes = group_notes(grouped_notes, new_note)

    return "\n".join([main, textify_grouped_notes(grouped_notes)])
