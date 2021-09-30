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


# filtering harnesses ~~~~~~~~~~~~
for i in `ls $OUT_DIR | grep -v "harness_bin" | grep -v "pdf_gen" | grep -v "tmp_obj_exchange"`
do 
	harness_size=`wc -l $OUT_DIR"/"$i"/"html_to_PDF_harness_template.cpp` 	
	if [[ $harness_size -lt 60000 ]]; then
		# collecting APIs from each harness.cpp file
	        echo $OUT_DIR"/"$i"/html_to_PDF_harness_template.cpp" >> $OUT_DIR/api_list
		cat -b $OUT_DIR/$i/html_to_PDF_harness_template.cpp | grep "FQL->" >> $OUT_DIR/api_list
	else
		echo $i
	fi
done

# ranking harnesses by # of API and # of Args ~~~~~~~~~~~~
python2.7 $SRC/src/harness/filter/ranking_harness_without_time.py $OUT_DIR/api_list $OUT_DIR/rank_list
rm -rf $OUT_DIR/api_list        

