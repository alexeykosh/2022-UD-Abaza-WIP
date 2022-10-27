import re

def main ():

    new_conllu = ""
    
    file1 = open("text6_Retsept_new_format.conllu", "r", encoding="utf8")
    txt_newf = file1.read()
    txt_newf_splitted_to_sent = re.split('\n\n', txt_newf)
    #print(txt_newf_splitted_to_sent[1])

    
    file2 = open("text6_Retsept.conllu", "r", encoding="utf8")
    txt_annot = file2.read()
    txt_annot_splitted_to_sent = re.split('\n\n', txt_annot)
    #print(txt_annot_splitted_to_sent[1])

    for sent_n in range(len(txt_newf_splitted_to_sent)):
        regexp1 = '(#.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n)1'
        res1 = re.search(regexp1, txt_newf_splitted_to_sent[sent_n]).group(1)
        new_conllu += res1
        #print(res1)


        regexp2 = '\n(1\t(?:.|\n)*)'
        res2 = re.search(regexp2, txt_annot_splitted_to_sent[sent_n]).group(1)
        new_conllu += res2 + "\n\n"
        #print(res2)

    print(new_conllu)
    
    path = 'new_format/text6_Retsept.conllu'
    f = open (path, 'w', encoding = 'utf-8')
    f.write (new_conllu)
    f.close

if __name__ == '__main__':
    main ()
