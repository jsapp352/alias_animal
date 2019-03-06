import requests
import json
import random
import time
import string

from collections import defaultdict

def getWordJSON(domain, lex_category, prefix, app_id, app_key):
    language = 'en'

    domain_query = '' if domain == None else 'domains={0};'.format(domain)

    prefix_query = '' if prefix == None else '?prefix={0}'.format(prefix)

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/wordlist/' + language

    url += '/{0}lexicalCategory={1}{2}'.format(domain_query, lex_category, prefix_query)

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    print(url)

    if r.status_code != 200:
        print('Wordlist request "{1}{2}" status: {0}'.format(r.status_code, domain, prefix))
        return None;

    return r.json()

def main():
    # API App ID and Key are stored in a separate text file.
    # App ID is on the first line, and App Key is on the second line.
    # Free keys are available to students at https://developer.oxforddictionaries.com/

    with open('oxford_api_credentials.txt', 'r') as f:
        app_id = f.readline().strip()
        app_key = f.readline().strip()

    adjective_lex = defaultdict(list)

    for prefix in string.ascii_lowercase:
        adjective_json = getWordJSON(None, 'adjective', prefix, app_id, app_key)

        print('Getting adjectives starting with: ' + prefix)
        if adjective_json == None:
            print("Problem with dictionary wordlist request for '{0}'...".format(prefix))

        results = adjective_json['results']

        adjective_lex[prefix] = [a['word'] for a in results]

        time.sleep(12)

    with open('adjective_lex.json', 'w') as f:
        json.dump(adjective_lex, f)

    animal_domains = ['mammal', 'reptile', 'bird', 'fish']
    animal_lex = defaultdict(list)

    for domain in animal_domains:
        animal_json = getWordJSON(domain, 'noun', None, app_id, app_key)
        if animal_json == None:
            print("Problem with dictionary wordlist request for '{0}'...".format(domain))

        results = animal_json['results']

        for animal in animal_json['results']:
            word = animal['word']
            animal_lex[word[0]].append(word)

        time.sleep(12)

    with open('animal_lex.json', 'w') as f:
        json.dump(animal_lex, f)


if __name__ == '__main__':
    main()
