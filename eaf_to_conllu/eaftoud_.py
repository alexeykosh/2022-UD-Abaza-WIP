import pympi
import string
import re
from os import (walk,
                system,
                path, 
                remove)
import sys


def open_eaf(eaf):
    '''
    Function that opens the eaf file and return the pympi instance
    '''
    return pympi.Elan.Eaf(file_path=eaf)


def make_text(text):
    '''
    Helper function that converts sentences to desired format
    '''
    textt = text.lower()
    textt = re.sub('\[.*\]', '', textt)
    textt = re.sub(r'[^\w\s]', '', textt)
    textt = textt.replace('i', 'I')
    return textt

def make_gloss(gloss):
    '''
    Convert glosses with lexical items to lists of glosses
    '''
    gloss = re.sub(r'[а-я]|[А-Я]', '', gloss)
    gloss = re.sub(r'-', '|', gloss)
    gloss = re.sub(r'_', '', gloss)
    gloss = re.sub(r'\?', '', gloss)
    gloss = re.sub(r'\(', '', gloss)
    gloss = re.sub(r'\)', '', gloss)
    gloss = re.sub(r'ё', '', gloss)
    gloss = re.sub(r'\[', '', gloss)
    gloss = re.sub(r'\]', '', gloss)
    gloss = re.sub(r'(\|)+', '|', gloss)
    gloss = re.sub(r'-$|^-', '', gloss)
    gloss = re.sub(r'\|$|^\|', '', gloss)
    gloss = re.sub(r'\+', '', gloss)
    return gloss

def format_ud(instance):
    '''
    Function that transforms data from the .eaf file to a conllu-compatible
    format  
    '''
    ud_format = []
    u = 1
    idx = 1

    sent_tier = [i for i in instance.tiers.keys() if 'Orth' in i][0]
    gloss_tier = [i for i in instance.tiers.keys() if 'Gloss' in i][0]
    trans_tier = [i for i in instance.tiers.keys() if 'Words_trans' in i][0]
    morph_tier_ = [i for i in instance.tiers.keys() if 'Morph' in i][0]
    transl_tier = [i for i in instance.tiers.keys() if 'Translation-txt' in i][0]


    sent_full = [j[2] for _, j in instance.tiers[sent_tier][0].items()]
    sent = [j[2].lower().translate(str.maketrans('', '', 
        string.punctuation)).split(' ') for _, j
        in instance.tiers[sent_tier][0].items()]
    gloss = [j[1] for _, j in instance.tiers[gloss_tier][1].items()]
    morph = [i[1] for _, i in instance.tiers[morph_tier_][1].items()]
    transl = [i[1] for _, i in instance.tiers[transl_tier][1].items()]
    trans = [i[1] for _, i in instance.tiers[trans_tier][1].items()]

    k = 0
    for i in range(len(sent)):
        transcription = ' '.join(trans[k:k + len(sent[i])])
        sentence = sent[i]
        glosses = gloss[k:k + len(sent[i])]
        morphology = morph[k:k + len(sent[i])]
        ud_format.append(
            f'\n# sent_id = {idx}'
            f'\n# text_name = {file}'
            f'\n# text_init = {make_text(sent_full[i])}'
            f'\n# text_orth = {" ".join(morphology)}'
            f'\n# text_transcription = {transcription}'
            f'\n# text_rus = {transl[i]}\n')

        idx += 1
        k += len(sent[i])

        num = 1
        for j in range(len(sentence)):
            ud_format.append(f'{num}\t{sentence[j]}\t_'
                f'\t_\t_\t{make_gloss(glosses[j])}\t_\t_'
                f'\t_\tGloss={morphology[j]}\n')
            num += 1
            u += 1        
    return ud_format

def make_conll_file(dir, out):
    '''
    Save the conllu-formatted string as a .conllu file
    '''

    content = format_ud(open_eaf(dir))
    with open(out, "w") as file:
        file.write(''.join(content))

def get_list_of_files(dir):
    '''
    Convert a directory with .eaf files to .conllu
    '''
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend([i for i in filenames if '.eaf' in i])
        break
    
    i = 1
    for file in files:
        make_conll_file(open_eaf(f'ELAN/{file}'), f'conllu_test/out{i}.conllu')
        i += 1

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('EafToUD.py <file> <out> <gloss>');
        sys.exit(-1)

    if not path.isdir('ud-scripts'):
        system('git clone https://github.com/ftyers/ud-scripts')
    
    file = sys.argv[1];
    out = sys.argv[2];
    gloss = sys.argv[3];

    make_conll_file(file, 'out.conllu')
    system(f'cat out.conllu | '
        f'python3 ud-scripts/conllu-feats.py {gloss} > {out}')
    remove('out.conllu')

    clean_out = []
    # Remove output from the previous script:
    with open(f'{out}') as conllu_:
        for line in conllu_.readlines():
            clean_out.append(re.sub(r'(Gloss=(\w|\w-)+)((\|.+)+)', r'\1', line))

    with open(f'{out}', 'w') as conllu_c:
        conllu_c.write(''.join(clean_out))
