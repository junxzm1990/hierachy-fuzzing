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

- clang/clang++ 
- python2.7
- python3.5+
- pip3
- pip2

```shell
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python2 get-pip.py
```
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
```shell
pip2 install numpy
```
- fitz for python3
```shell
pip3 install fitz
```
- frontend for python3
```shell
pip3 install frontend
```

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
## Run OBJ_Mutation(obj_exchange)
```shell
```

## Run OBJ_Mutation(obj_entry_mutation)
```shell
```

## CPU Core Affinity 
- For example, if we want to combine process of new_generator.sh to core 2 :
```shell
pid=`ps -h | grep "new_generator"`
pid=`echo $pid |cut -d " " -f 1`
taskset -p $pid
taskset -pc 1 $pid
taskset -p $pid
```


## Testcases

- testcases/HTML_testcases : 10 random picked HTMLs for testing harness part
- testcases/ONE_HTML : for testing harness part of only one HTML provided


## Trouble Shooting
- trim_py.py ERROR complaining "static/ does not exist"
  This means fitz does not recognize static/ path. The easiest way to fix this is 
```shell
pip3 uninstall fitz
pip3 install pymupdf
```  
