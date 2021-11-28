while getopts h:p:o: option
do
	case "${option}"
        in 
	h) HARNESS_DIR=${OPTARG};; # dir of harness folders
	p) PDF_DIR=${OPTARG};; # dir of pdf files
        o) OUT_DIR=${OPTARG};; # dir of outputs
        esac
done

if [[ $HARNESS_DIR == "" ]]; then
	echo "provide harness folders' directory as input"
        exit -1
fi

if [[ $PDF_DIR == "" ]]; then
	echo "provide PDF files' directory as input"
	exit -1
fi

if [[ $OUT_DIR == "" ]]; then
	echo "provide the directory as output"
	exit -1
fi

for i in $HARNESS_DIR/*; do 
	a=`echo $i | rev | cut -d "/" -f 1 | rev`; 
	suf="pdf"; 
	foo=${a%"$suf"}; 
	b=`find $PDF_DIR/* -name $foo*`; 
	if [[ $b == '' ]]; then 
		echo "AAAAA : "$a; 
		echo "BBBBB : "$b;
	else 
		cp $b $OUT_DIR
 
	fi; 
done

