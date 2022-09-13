# DIR-BASED FUZZING

## Overview
This project focuses on fuzzing document software or precisely, software that processes document files (e.g., HTML,PDF, and DOCX). Document software typically requires highly-structured inputs, which general-purpose fuzzing cannot handle well. Accordingly, past research has explored generation-based fuzzing, which follows the grammar of the target document format to generate structure-correct testcases for fuzzing document software. More recently, people have enhanced generation-based fuzzing with structure-aware, coverage-guided mutations to better test document software. However, the existing solutions have two major limitations. First, they require creating/summarizing a separate grammar model for each document format, incurring extensive labor costs to handle different types of formats. Second, they run mutations at a single level of the structure (e.g., subtree level or attribute level), failing to sufficiently exploit the potential of mutations.
In this project, we propose two techniques to facilitate fuzzing on document software. First, we design an intermediate document representation, called DIR, for document files. DIR describes a document file in an abstract way that is independent of the underlying format. Reusing common SDKs, a DIR document can be lowered into any desired format without a deep understanding of the grammar of the format. Second, we propose multi-level mutations to directly operate on a DIR document. Our multi-level mutations can more thoroughly explore the searching space than existing single-level mutations. Combining these two techniques, we can reuse the same DIR-based generations and mutations to fuzz any document format, without the need to separately summarize the target grammar and re-engineer the genera-
tion/mutation components.
To validate the utility of our DIR-based fuzzing, we apply the approach to PDF. We show that with minimal efforts in understanding the PDF grammar and structure, we can effectively fuzz PDF software. In a 48-hour evaluation on 6 mainstream PDF applications, we show that our DIR-based fuzzing can cover 33.87% more code than general-purpose mutation-based fuzzing (AFL++), 127.74% more code than purely generation based PDF fuzzing (Learn&Fuzz), and 25.17% more code than structure-aware mutation-based
fuzzing (NAUTILUS).

## Code Organization

```console

|-- Seeds Generator 
	|-- harness mutation            # src/harness/
	|-- OBJ_mutation                # src/OBJ/
		|-- OBJ_level           # src/OBJ/OBJ_exchange/
		|-- Instruction_level   # src/OBJ/OBJ_entry/
|-- Formats Convertor 
	|-- HTML files-> PDF harness    # src/HTML2PDF/
	|-- PDF files -> PDF harness    # src/PDF2PDFharness/
```

## Environment
- Tested on Ubuntu 16.04 64bit, 18.04 64bit and 20.04 64bit
- Access of [ foxit_quick_pdf_library_1811_linux ](https://developers.foxit.com/developer-hub/documents/quick-pdf-library/) is required
- The installation of [ Docker ](https://developers.foxit.com/developer-hub/documents/quick-pdf-library/) is required

## Usage

### Steop 0 : Set-up 

- pull AFL++ docker

```shell
$ docker pull aflplusplus/aflplusplus
$ docker run -ti -v /location/of/your/target:/src aflplusplus/aflplusplus
```

#### inside AFL++ docker needs :

- clang/clang++
- python2.7
- python3.5+
- pip3
- pip2

```shell
$ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
$ python2 get-pip.py
```
- bs4 for python2
```shell
$ pip2 install beautifulsoup4
```
Once bs4 installed, update path of bs4 in src/harness/generator/overall_html_harness_parser.py:2

- lxml
```shell
$ pip2 install lxml
```
- numpy for python2
```shell
$ pip2 install numpy
```
- fitz for python3
```shell
$ pip3 install fitz
```
- frontend for python3
```shell
$ pip3 install frontend
```

### Step 1 : create config file

- Please reference ~/hierarchy_fuzzing/src/sample_var.config (each var with comment following)
- (If you still have question about creating config file, please email ywang291@stevens.edu)

### Step 2 : create commands file

- If no other extensions, you can directly use ~/hierarchy_fuzzing/src/commands as commands file
- If you extended the convertor, make sure you update this commands file before run the fuzzer

### Step 3 : run hierarchy fuzzer 

~~~{.sh}

$ cd hierachy-fuzzing/
$ bash ./src/main.sh -c [ config_file ] -l [ command_file ]

~~~

### Step 4 : remove commands_opt

~~~{.sh}

$ rm -f  ~/hierarchy_fuzzing/src/commands_opt

~~~

## TIPS + TROUBLE SHOOTING

### re-using set-up docker image : 
get the docker id :
```shell 
$ docker ps -a
```
restart the docker :
```shell
$ docker restart <id>
```
re-attach on docker :
```shell
$ docker attach <id>
```
### CPU Core Affinity 
- For example, if we want to combine process of new_generator.sh to core 2 :
```shell
$ pid=`ps -h | grep "new_generator"`
$ pid=`echo $pid |cut -d " " -f 1`
$ taskset -p $pid
$ taskset -pc 1 $pid
$ taskset -p $pid
```
### Trouble Shooting
- trim_py.py ERROR complaining "static/ does not exist"
  This means fitz does not recognize static/ path. The easiest way to fix this is 
```shell
$ pip3 uninstall fitz
$ pip3 install pymupdf
```  
 




