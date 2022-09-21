import pyconll
import sys
from os import (walk, 
                remove)

def get_filenames(directory):
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend([i for i in filenames if '.conllu' in i])
        break
    return sorted(files)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('combine_texts.py <directory> <out>')
        sys.exit(-1)

    directory = sys.argv[1]
    out = sys.argv[2]

    fn = get_filenames(directory)
    with open(directory + '/train.conllu', 'w') as outfile:
        for fname in fn:
            with open(directory + '/' + fname) as infile:
                outfile.write(infile.read())
    train = pyconll.load_from_file(directory + '/train.conllu')
    i = 1
    for sentence in train:
        sentence.id = i
        i += 1
    with open('train.conllu', 'w', encoding='utf-8') as f:
        train.write(f)
    print(f'Combination is completed: {out} has {i} sentences.')
    remove(directory + '/train.conllu')
