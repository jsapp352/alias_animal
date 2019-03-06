import argparse
import json
import random

argparser = argparse.ArgumentParser()

argparser.add_argument(
	'first_initial',
	help='a single initial or the beginning letters of your first name',
	nargs='?',
	type=str,
	default=''
)

argparser.add_argument(
	'last_initial',
	help='a single initial or the beginning letters of your last name',
	nargs='?',
	type=str,
	default=''
)

argparser.add_argument(
	'max_result_count',
	help='the maximum number of desired results',
	nargs='?',
	type=int,
	default='-1'
)

args = argparser.parse_args()

def getWordList(prefix, filename):
    with open(filename, 'r') as f:
        lexicon = json.loads(f.read())

	lexicon = lexicon[prefix[0]]

    wordlist = [word for word in lexicon if word.startswith(prefix)]

    return wordlist

def main():
    result_count = 10

    adjective_lex_json = "adjective_lex.json"
    animal_lex_json = "animal_lex.json"

    if args.first_initial == '':
        first_initial = raw_input('Enter first initial: ')
    else:
        first_initial = args.first_initial

    if args.last_initial == '':
        last_initial = raw_input('Enter last initial: ')
    else:
        last_initial = args.last_initial

    if args.max_result_count <= 0:
        max_result_count = int(raw_input('Enter max number of results: '))
    else:
        max_result_count = args.max_result_count

    if max_result_count < 0:
        max_result_count = 1

    adjectives = getWordList(first_initial, adjective_lex_json)
    animals = getWordList(last_initial, animal_lex_json)

    if  adjectives == None or animals == None:
        print("Problem loading dictionary wordlists... exiting program :(")
        return

    result_count = min(max_result_count, len(adjectives), len(animals))

    adjective_sample = random.sample(adjectives, result_count)
    animal_sample = random.sample(animals, result_count)

    print('\nYour names are:')

    for adjective, animal in zip(adjective_sample, animal_sample):
        try:
            print('{0} {1}'.format(adjective.title(), animal.title()))
        except:
            pass

if __name__ == '__main__':
    main()
