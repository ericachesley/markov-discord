"""Generate Markov text from text files."""

from random import choice
import sys
import discord
import os
import emoji

client = discord.Client()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here
    return open(file_path).read()


def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    text_list = text_string.split()

    chains = {}

    for i in range(n):
        if text_list[i][0].isupper():
            starters = chains.get('START', [])
            starters.append(text_list[i:i+n])
            chains['START'] = starters

    # your code goes here
    for i in range(len(text_list)-n):
        n_gram = tuple(text_list[i:i+n])

        #bigram = (text_list[i], text_list[i+1])

        followers = chains.get(n_gram, [])
        followers.append(text_list[i+n])

        if n_gram[-1][-1] in {'.', '?', '!'}:
            followers.append('EOF')

        chains[n_gram] = followers

        if text_list[i+n][0].isupper():
            starters = chains.get('START', [])
            starters.append(text_list[i+n:i+(2*n)])
            chains['START'] = starters

    return chains

def combine_dicts(dict1, dict2):
    new_dict = {}

    for key in dict1.keys():
        values = dict1[key]
        more_values = dict2.get(key, [])
        values.extend(more_values)

        new_dict[key] = values

    for key in dict2.keys():
        if key not in dict1:
            new_dict[key] = dict2[key]

    return new_dict    


def make_text(chains):
    """Return text from chains."""

    # your code goes here
    n_gram = tuple(choice(chains['START']))
    words = [word for word in n_gram]

    while n_gram in chains:

        next_word = choice(chains[n_gram])
        if next_word == 'EOF':
            break
        words.append(next_word)

        n_gram = list(n_gram)[1:]
        n_gram.append(next_word)
        n_gram = tuple(n_gram)
    
    return " ".join(words)


input_files = sys.argv[2:]

combined_chains = {}

for file in input_files:
    # Open the file and turn it into one long string
    input_text = open_and_read_file(file)
    # Get a Markov chain
    new_chains = make_chains(input_text, int(sys.argv[1]))
    combined_chains = combine_dicts(combined_chains, new_chains)




#print(random_text)

@client.event
async def on_message(message):
    #print(message.contents)
    if message.author == client.user:
        return

    if message.content.startswith(emoji.emojize(":thumbs_up:")) or message.content.startswith(emoji.emojize(":thumbs_up:")) or message.content.startswith("Write"):
        # Produce random text
        random_text = make_text(combined_chains)
        await message.channel.send(random_text)

client.run(DISCORD_TOKEN)

