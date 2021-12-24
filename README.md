# overthere

> it's over there

A bit.ly/tinyurl clone-ish that lets you post multiple links on one page and has memorable URLs like "exquisite-cow".

Made with [Python 3](https://www.python.org/), [Flask](https://flask.palletsprojects.com/), and [SQLite](https://sqlite.org/).

---

# Install and Run

You'll need [Python 3](https://www.python.org/)

```
# Clone the repository
git clone https://github.com/NitroGuy10/tuscon

# Create a virtual environment
python3 -m venv venv

# Activate it (Windows)
venv\Scripts\activate.bat

# Activate it (Mac/Linux)
source venv/bin/activate

# Install the requirements
pip3 install -r requirements.txt

# Create a new database
python3 create.py

# Start overthere
python3 app.py
```

---

# Options

If you'd like, you can supply your own lists of adjectives and nouns. Just edit data/unchanging/adjectives.txt and nouns.txt respectively.

The two lists MUST HAVE THE SAME NUMBER OF LINES excluding any linebreaks at the start or end of the files. If you update the lists you MUST make a new database.

overthere already comes with lists of 100 nouns and 100 adjectives so you can skip this step if you want.

---

# Known Quirks

If there is a "backlash backslash n" in a link, an unintentional linebreak will replace it. If you want to fix this, submit a PR :)
