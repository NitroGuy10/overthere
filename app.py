from os.path import exists
import random
# import sqlite3
# import flask


def generate_link_name(index):
    """Generate the link name specified by the index"""
    noun_index_offset = index // word_list_length
    if noun_index_offset >= word_list_length:
        raise IndexError("index exceeds the total number of unique word combinations")
    return "{}-{}".format(
        adjectives[index % word_list_length],
        plural_nouns[(index + noun_index_offset) % word_list_length])


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

    # Read the lists of adjectives and plural_nouns from their respective files
    # The two lists must be same length
    # Make sure these lists are finalized before creating the database; do not change them after the database is created
    global adjectives
    global plural_nouns
    global word_list_length
    with open("data/unchanging/adjectives.txt", "r") as adjective_file:
        adjectives = adjective_file.read().split("\n")
    with open("data/unchanging/plural_nouns.txt", "r") as plural_noun_file:
        plural_nouns = plural_noun_file.read().split("\n")
    word_list_length = len(adjectives)

    # Create the non-repeating sequences of random integers for this seed
    # These will be used for generating the URLs
    # Each new entry will use the next index in these lists
    global url_adjective_sequence
    global url_plural_noun_sequence
    url_adjective_sequence = random.sample(range(word_list_length), word_list_length)
    url_plural_noun_sequence = random.sample(range(word_list_length), word_list_length)

    # Set next_entry_index to the... index of the next entry
    if False:  # TODO if database exists
        # TODO set next_index to the NUMBER OF ENTRIES in the database
        pass
    else:
        next_entry_index = 0

    print(generate_link_name(next_entry_index))
