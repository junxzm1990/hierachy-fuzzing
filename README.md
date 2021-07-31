# hierachy-fuzzing

Overiew of the src code :
```console

|-- harness mutation		# src/harness
|-- OBJ_mutation		# src/OBJ

```

## Environment Set Up

- pull AFL++ docker
inside AFL++ docker needs : 
- python2.7
- pip2
- bs4 for python2 : pip2 install beautifulsoup4 (then, update path of bs4 in src/harness/generator/overall_html_harness_parser.py:2) 
- lxml: pip2 install lxml
- numpy for python2

## Run Harness

  [update paths in src/var.config]

  bash hierarchy_fuzzing/src/main.sh -i [INPUT] -o [OUTPUT] -d [DATE] -s [SRC] -q [QUEUE] -t [TIME]

- INPUT(-i) : dir of HTMLs
- OUTPUT(-o) : dir of harness generator outputs 
- DATE(-d)
- SRC(-s) : dir of hierarchy_fuzzing/
- QUEUE(-q) : dir where you want to migrate the generated PDF files
- TIME(-t) : how long you want to run on each harness fuzzing in minute(Only apply on more than ONE HTML INPUT) 

## Testcases

- testcases/HTML_testcases : 10 random picked HTMLs for testing harness part
- testcases/ONE_HTML : for testing harness part of only one HTML provided
