import requests
import json
import random
import time
import string

def getWordList(domain, lex_category, prefix, app_id, app_key):
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

def getWords(wordlist):
    return [x['word']+'\n'.encode('utf-8') for x in wordlist['results']]



def main():
    # API App ID and Key are stored in a separate text file.
    # App ID is on the first line, and App Key is on the second line.
    # Free keys are available to students at https://developer.oxforddictionaries.com/

    with open('oxford_api_credentials.txt', 'r') as f:
        app_id = f.readline().strip()
        app_key = f.readline().strip()

    adjective_lex = {}

    for prefix in string.ascii_lowercase:
        adjective_json = getWordList(None, 'adjective', prefix, app_id, app_key)

        print('Getting adjectives starting with: ' + prefix)
        if adjective_json == None:
            print("Problem with dictionary wordlist request for '{0}'...".format(prefix))

        for a in adjective_json['results']:
            adjective_lex[a['id']] = {'word': a['word']}

        time.sleep(12)

    with open('adjective_lex.json', 'w') as f:
        json.dump(adjective_lex, f)

    animal_domains = ['mammal', 'reptile', 'bird', 'fish']

    animal_lex = {}

    for domain in animal_domains:
        animal_json = getWordList(domain, 'noun', None, app_id, app_key)
        if animal_json == None:
            print("Problem with dictionary wordlist request for '{0}'...".format(domain))

        for a in animal_json['results']:
            animal_lex[a['id']] = {'word': a['word']}

        time.sleep(15)

    with open('animal_lex.json', 'w') as f:
        json.dump(animal_lex, f)


if __name__ == '__main__':
    main()
