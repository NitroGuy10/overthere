from os.path import exists
import random
from flask import Flask, request, jsonify, render_template, escape
import sqlite3


app = Flask(__name__)


def generate_link_name(index):
    """Generate the link name specified by the index"""
    noun_index_offset = index // word_list_length
    # Since the list are the same length, the max number of database entries is the list length squared
    # This uh... does the same thing
    if noun_index_offset >= word_list_length:
        raise IndexError("index exceeds the total number of unique word combinations")
    return "{}-{}".format(
        adjectives[url_adjective_sequence[index % word_list_length]],
        nouns[url_noun_sequence[(index + noun_index_offset) % word_list_length]])


@app.route("/")
def serve_index():
    """Serve index.html"""
    return app.send_static_file("index.html")


@app.route("/create", methods=["POST"])
def create_entry():
    """Create an entry in the database"""
    data = request.get_json(silent=True)

    # Ensure data is valid JSON
    if data is None or "string" not in data or type(data["string"]) is not str:
        print("Not valid JSON")
        return jsonify({"invalidLength": True, "url": request.base_url[:-6] + "full-commitment"})

    # Un-escape linebreaks
    # If there is a "backlash backslash n" in a link, an unintentional linebreak will replace it
    # If you want to fix this, submit a PR :)
    data_string = data["string"].replace("\\\\n", "\n")

    # Ensure string is proper length
    if len(data_string) > 1000 or len(data_string) == 0:
        print("Unacceptable string length")
        return jsonify({"invalidLength": True, "url": request.base_url[:-6] + "full-commitment"})

    # Ensure the database is not full
    global next_entry_index
    if next_entry_index // word_list_length >= word_list_length:
        print("The database is full")
        return jsonify({"databaseFull": True})

    # Add entry to the database
    connection = sqlite3.connect("overthere.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO link_pages (url, links) VALUES (?, ?);",
                   (generate_link_name(next_entry_index), data_string))
    connection.commit()

    print("Created new link page:", generate_link_name(next_entry_index))
    next_entry_index += 1
    return jsonify({"url": request.base_url[:-6] + generate_link_name(next_entry_index - 1)})


@app.route("/<link_name>")
def serve_links(link_name):
    """Serve a link page from the database if it exists"""
    connection = sqlite3.connect("overthere.db")
    cursor = connection.cursor()
    links = cursor.execute("SELECT links FROM link_pages WHERE url=?;", (link_name,)).fetchone()
    if links is None:
        return app.send_static_file("nothing.html")
    # Escape any cringe HTML from links
    links_list = []
    for link in links[0].split("\n"):
        links_list.append(escape(link))
    return render_template("overthere.html.jinja", links=links_list, url=link_name)


if __name__ == "__main__":
    print("Hello, overthere!")

    # Retrieve the random seed from last session if it exists
    # Otherwise, create a new random seed
    if exists("data/seed.txt"):
        with open("data/seed.txt", "r") as seed_file:
            seed = int(seed_file.readline())
            random.seed(seed)
        print("The seed from seed.txt will be used:", seed)
    else:
        random.seed()
        new_seed = random.randint(0, 9223372036854775807)
        random.seed(new_seed)
        with open("data/seed.txt", "w") as seed_file:
            seed_file.write(str(new_seed))
        print("A new seed will be used:", new_seed)

    # Read the lists of adjectives and nouns from their respective files
    # The two lists must be same length
    # Make sure these lists are finalized before creating the database; do not change them after the database is created
    global adjectives
    global nouns
    global word_list_length
    with open("data/unchanging/adjectives.txt", "r") as adjective_file:
        adjectives = adjective_file.read().strip("\n").split("\n")
    with open("data/unchanging/nouns.txt", "r") as noun_file:
        nouns = noun_file.read().strip("\n").split("\n")
    word_list_length = len(adjectives)

    # Create the non-repeating sequences of random integers for this seed
    # These will be used for generating the URLs
    # Each new entry will use the next index in these lists
    global url_adjective_sequence
    global url_noun_sequence
    url_adjective_sequence = random.sample(range(word_list_length), word_list_length)
    url_noun_sequence = random.sample(range(word_list_length), word_list_length)

    # Set next_entry_index to the... index of the next entry
    global next_entry_index
    next_entry_index = 0
    if exists("overthere.db"):
        connection = sqlite3.connect("overthere.db")
        cursor = connection.cursor()
        next_entry_index = cursor.execute("SELECT COUNT(url) FROM link_pages;").fetchone()[0]
        print("There are {} entries in the database".format(next_entry_index))
    else:
        raise FileNotFoundError("overthere.db not found; create a new database by running create.py")

    app.run(host="0.0.0.0", port=25565)
