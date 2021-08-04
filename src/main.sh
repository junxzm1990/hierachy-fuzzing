while getopts c: option 
do 
	case "${option}"
	in
	c) CONFIG=${OPTARG};;
	esac
done

if [[ $CONFIG == "" ]]; then
        echo "Please provide CONFIG file (-c)"
        exit -1
fi


# load config file
. $CONFIG

echo $foxit_loc $AFLpp_loc


mkdir $OUT_DIR/pdf_gen/

mkdir $OUT_DIR/harness_bin/


# --------------- .cpp GENERATION -----------------------------------------------------------
for h in $IN_DIR/*
do
	python2 $SRC/src/harness/generator/overall_html_harness_parser.py $h $OUT_DIR $OUT_DIR/pdf_gen/ $foxit_loc $AFLpp_loc
done

# checking how many HTML PROCESSED
cnt=`ls $OUT_DIR | grep -v "harness_bin" | grep -v "pdf_gen" | wc -l`


if [[ $cnt == 0 ]] 
then
	echo "Please provide another Input dir. No HTML in current dir can be convert to PDF harness"


# -------------- SCENTARIO C : 1+ HTML PROVIDED ---------------------------------------------------------
else
       
	bash $SRC/src/harness/filter/filter_shell.sh -c $CONFIG 
        

	# harness compile, fuzzing, pdf files migration	
	while [ -s $OUT_DIR/rank_list ]; do

		bash $SRC/src/harness/harness_compile_fuzzing_migrate.sh -c $CONFIG -n $cnt
		
	done

fi
