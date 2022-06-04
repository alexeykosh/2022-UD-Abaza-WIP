import pympi
import string
import re
from os import (walk,
                system,
                path)
import itertools
import sys


class EafToUD:
    def __init__(self, directory: str):
        self.ud_temp = []
        self.directory = directory
        # self.sent_tier = sent_tier
        # self.morph_tier = morph_tier
        self.files = self.get_list_of_files()
        self.instances = self.make_pympi_instances()
        self.glosses = []

    def get_list_of_files(self):
        files = []
        for (dirpath, dirnames, filenames) in walk(self.directory):
            files.extend([i for i in filenames if '.eaf' in i])
            break
        return files

    def make_pympi_instances(self):
        instances = []
        for file in self.files:
            if '.eaf' in file:
                print('{}/{}'.format(self.directory, file))
                instances.append(pympi.Elan.Eaf(
                    file_path='{}/{}'.format(self.directory, file)))
        return instances

    def make_gloss(self, gloss):
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
        self.glosses.append(gloss)
        return gloss

    @staticmethod
    def make_text(text):
        textt = text.lower()
        textt = re.sub('\[.*\]', '', textt)
        textt = re.sub(r'[^\w\s]', '', textt)
        textt = textt.replace('i', 'I')
        return textt

    def format_ud(self):
        ud_format = []
        u = 1
        idx = 1
        for instance in self.instances:
            sent_tier = [i for i in instance.tiers.keys() if 'Orth' in i][0]
            morph_tier = [i for i in instance.tiers.keys() if 'Gloss' in i][0]
            sent_full = [j[2] for _, j in
                         instance.tiers[sent_tier][0].items()]
            sent = [j[2].lower().translate(str.
                                           maketrans('', '',
                                                     string.punctuation)).split(
                ' ')
                for _, j in instance.tiers[sent_tier][0].items()]

            gloss = [j[1] for _, j in
                     instance.tiers[morph_tier][1].items()]
            k = 0
            for i in range(len(sent)):
                ud_format.append(
                    '\n# sent_id = {}\n# text_name = {}\n# text = {}\n# '
                    'text_init = {}\n'.
                        format(idx, self.files[u - 1],
                               self.make_text(sent_full[i]),
                               sent_full[i]))
                idx += 1
                sentence = sent[i]
                glosses = gloss[k:k + len(sent[i])]
                k += len(sent[i])

                num = 1
                for j in range(len(sentence)):
                    ud_format.append('{}\t{}\t_\t_\t_\t{}\t_\t_\t_\tGloss={}\n'.
                                     format(num, sentence[j],
                                            self.make_gloss(glosses[j]),
                                            glosses[j]))
                    num += 1
            u += 1
        return ud_format

    def make_conll_file(self, filename):
        content = self.format_ud()
        with open(filename, "w") as file:
            file.write(''.join(content))

    def make_gloss_file(self, filename):
        lines = []
        unique = set(itertools.chain(*[i.split('|') for
                                       i in self.glosses]))
        for gloss in sorted(unique):
            if len(gloss) > 1:
                lines.append('_\t_\t{}\t_\t_\t_\t_\t_\n'.format(gloss))
        with open(filename, "w") as file:
            file.write(''.join(lines))


if __name__ == '__main__':
    if len(sys.argv) != 4: #{
        print('EafToUD.py <directory> <out> <gloss>');
        sys.exit(-1);
    # }

    if not path.isdir('ud-scripts'):
        system('git clone https://github.com/ftyers/ud-scripts')
    
    directory = sys.argv[1];
    out = sys.argv[2];
    gloss = sys.argv[3];
    a = eaf_transformer = EafToUD(directory=directory)
    a.make_conll_file(out)
    a.make_gloss_file('abazaXPOS_temp.udx')
    system('cat {} | python3 ud-scripts/conllu-feats.py {} > trial-XPOS.conllu'.format(out, gloss))
