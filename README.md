# hierachy-fuzzing

Overiew of the src code :
```console

|-- harness mutation		# src/harness
|-- OBJ_mutation		# src/OBJ

```

## Environment Set Up

- pull AFL++ docker 
```shell
docker pull aflplusplus/aflplusplus
docker run -ti -v /location/of/your/target:/src aflplusplus/aflplusplus
```

#### inside AFL++ docker needs :
 
- python2.7
- pip2
- bs4 for python2 
```shell
pip2 install beautifulsoup4 
```
Once bs4 installed, update path of bs4 in src/harness/generator/overall_html_harness_parser.py:2
- lxml 
```shell
pip2 install lxml
```
- numpy for python2

#### re-using set-up docker image : 
get the docker id :
```shell 
docker ps -a
```
restart the docker : 
```shell
docker restart <id>
```
re-attach on docker :
```shell
docker attach <id>
```


## Run Harness

  1. Followsng the comments of each variable, updating paths locally in src/var.config (example : src/sample_var.config)
  2. Run following command line

```shell
cd hierachy-fuzzing/
bash ./src/main.sh -c ./src/var.config
```

## Testcases

- testcases/HTML_testcases : 10 random picked HTMLs for testing harness part
- testcases/ONE_HTML : for testing harness part of only one HTML provided
