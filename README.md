## Abaza Universal Dependencies treebank

Repository for the work in progress version of the Abaza UD treebank. 

### Usefull commands:

If you want to process an .eaf file for annotation, do:

```console
eaftoud_.py <eaf. file> <conllu. out file> <XPOS file>
```

If you want to combine eaf files into the final corpus, do: 

```console
combine_texts.py <directory with .eaf files> <.conllu out>
```