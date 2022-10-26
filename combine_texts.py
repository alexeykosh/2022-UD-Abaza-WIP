import pyconll
import sys
from os import walk

def get_filenames(directory):
    files = []
    for (_, _, filenames) in walk(directory):
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

    sentences = []
    i = 1

    for fname in fn:
        for sent in pyconll.iter_from_file(directory + '/' + fname):
            sent.set_meta('sent_id', i)
            sentences.append(sent.conll())
            i += 1
    
    with open(out, 'w', encoding='utf-8') as f:
        for s in sentences:
            f.write(f'\n{s}\n')
    
    print(f'Combination is completed: {out} has {i-1} sentences.')
