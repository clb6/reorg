import datetime as dt
from reorg import page


def test_create_page_name():
    dir_curr_crawl = "/home/dawd13r/Documents/MyKnowledgeBase/PersonalInformationManagement"
    assert page.create_page_name(dir_curr_crawl) == "PersonalInformationManagement.md"

EXPECTED_TEXT = """
## Notes

### Some thought

**2020-02-22-10:00**

Foo foo

### Important

Look here

**2020-02-21-09:00**

baz baz

### Another thought

**2020-02-20-08:00**

Bar bar

### Final thought

**2020-02-19-07:00**

Hello hello
"""

def test_textify_grouped_notes():
    grouped_notes = {
            'Some thought':
                [('Foo foo\n\n### Important\n\nLook here', dt.datetime(2020, 2, 22, 10, 0)),
                    ('baz baz', dt.datetime(2020, 2, 21, 9, 0))],
            'Another thought': [('Bar bar', dt.datetime(2020, 2, 20, 8, 0))],
            'Final thought': [('Hello hello', dt.datetime(2020, 2, 19, 7, 0))]
            }
    text = page.textify_grouped_notes(grouped_notes)
    print(text)
    assert text.strip() == EXPECTED_TEXT.strip()

def test_group_notes():
    grouped_notes = {"Some thought": ["Foo foo\n\n### Important\n\nLook here"], "Another thought": ["Bar bar"]}
    new_note = {"Some thought": ["baz baz"], "Final thought": ["Hello hello"]}
    grouped_notes = page.group_notes(grouped_notes, new_note)
    print(grouped_notes)
    assert grouped_notes == {'Some thought': ['Foo foo\n\n### Important\n\nLook here', 'baz baz'],
            'Another thought': ['Bar bar'], 'Final thought': ['Hello hello']}

def test_when_note_created():
    created = page.when_note_created("_2020-02-13-2000.md")
    print(created)
    assert created.year == 2020 and created.month == 2 and created.day == 13
    assert created.hour == 20

def test_get_title_level():
    assert page.get_title_level("# Foo") == 1
    assert page.get_title_level("##### Foo") == 5
    assert page.get_title_level("#Foo") == 0
    assert page.get_title_level("Foo") == 0
    assert page.get_title_level("") == 0
    assert page.get_title_level("   ") == 0

def adjust_title_level():
    assert page.adjust_title_level("# Foo", 2) == "## Foo"
    assert page.adjust_title_level("## Foo", 1) == "# Foo"
    assert page.adjust_title_level("## Foo", 0) == "Foo"

SOME_NOTE = """
## Some thought

Some thought was made.

### Sub sub thought

Here is where sub sub thought done.

## Another thought

Another thought was made.

## Some thought

More thoughts on some thought.

Another paragraph here.
"""

def test_find_title_levels_distribution():
    text_split = SOME_NOTE.split("\n")
    counter = page.find_title_levels_distribution(text_split)
    print(counter)
    assert counter.most_common() == [(2,3), (3,1)]

def test_get_title_level_biggest():
    from collections import Counter
    assert page.get_title_level_biggest(Counter([2,2,2,3])) == 2
    assert page.get_title_level_biggest(Counter([4,4,2,2,2,3])) == 2
    assert page.get_title_level_biggest(Counter([])) == 0

def test_parse_note():
    from datetime import datetime, timezone
    created = datetime(2020, 2, 19, hour=4, minute=5, tzinfo=timezone.utc)
    result = page.parse_note(SOME_NOTE, created)
    print(result)
    assert result == {
            'Some thought': [('Some thought was made.\n\n#### Sub sub thought\n\nHere is where sub sub thought done.\n\n\nMore thoughts on some thought.\n\nAnother paragraph here.',
                created)],
            'Another thought': [('Another thought was made.',
                created)]
            }
