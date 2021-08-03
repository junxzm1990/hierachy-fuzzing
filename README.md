# hierachy-fuzzing

Overiew of the src code :
```console

|-- harness mutation		# src/harness
|-- OBJ_mutation		# src/OBJ

```

## Environment Set Up

- pull AFL++ docker

#### inside AFL++ docker needs :
 
- python2.7
- pip2
- bs4 for python2 : pip2 install beautifulsoup4 (Once bs4 installed, update path of bs4 in src/harness/generator/overall_html_harness_parser.py:2) 
- lxml: pip2 install lxml
- numpy for python2

## Run Harness

  Following the comments of each variable, updating paths locally in src/var.config

```console

	cd ~/hierachy-fuzzing/

  	bash ./src/main.sh

```

## Testcases

- testcases/HTML_testcases : 10 random picked HTMLs for testing harness part
- testcases/ONE_HTML : for testing harness part of only one HTML provided
