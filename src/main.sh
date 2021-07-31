while getopts i:o:d:q:s:t: option
do 
	case "${option}"
	in
	i) IN_DIR=${OPTARG};;
	o) OUT_DIR=${OPTARG};;
	d) DATE=${OPTARG};;
	s) SRC=${OPTARG};;
	q) QUEUE=${OPTARG};;
	t) TIME=${OPTARG};;
	esac
done

if [[ $IN_DIR == "" ]]; then
        echo "Please provide the dir where stores HTMLs (-i)"
        exit -1
fi

if [[ $OUT_DIR == "" ]]; then
        echo "Please provide the directory where you want to output harness.cpp file(-o)"
        exit -1
fi

if [[ $DATE == "" ]]; then
        echo "Please provide the DATE(-d)"
        exit -1
fi

if [[ $SRC == "" ]]; then
        echo "Please provide the dir of hierarchy_fuzzing(-s)"
        exit -1
fi

if [[ $QUEUE == "" ]]; then
        echo "Please provide AFL++ instances dir (for example, XXXXXX/afl_S_0, provide XXXXXX path here) (-q)"
        exit -1
fi

# load config file
. $SRC/src/var.config

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


# -------------- SCENARIO A : ONLY ONE HTML PROVIDED ----------------------------------------------------
if [[ $cnt == 1 ]] 
then
	echo "ONLY ONE HTML"
	# 1. compile .cpp to harness bin ~~~~~~~~~~
        for i in `ls $OUT_DIR | grep -v "harness_bin" | grep -v "pdf_gen"`
        do 
        	$AFLpp_loc/afl-clang++ -g -O3 -funroll-loops -o $OUT_DIR/harness_bin/$i -Wno-format -Wno-pointer-sign -I. -fpermissive -fPIC $OUT_DIR/$i/html_to_PDF_text_harness_template.cpp $AFLpp_loc/afl-compiler-rt.o $AFLpp_loc/utils/afl_frida/libfrida-gum.a -ldl -lresolv -pthread -std=c++11
        	
        done

	# 2. run harness mutation fuzzing ~~~~~~~~~~
	top_rank=`ls $OUT_DIR/harness_bin/`
	mkdir $OUT_DIR/harness$top_rank$DATE
	LD_LIBRARY_PATH=$foxit_loc/Libs/ $AFLpp_loc/afl-fuzz -m none -t 1000000+ -i $AFLpp_loc/testcases/others/pdf/ -o $OUT_DIR -- $OUT_DIR/harness_bin/* @@



# -------------- SCENTARIO B : NONE HTML PROVIDED --------------------------------------------------------
elif [[ $cnt == 0 ]] 
then
	echo "Please provide another Input dir. No HTML in current dir can be convert to PDF harness"


# -------------- SCENTARIO C : 1+ HTML PROVIDED ---------------------------------------------------------
else
        echo "processing mutiple HTMLs"
        
	# filtering harnesses ~~~~~~~~~~~~
        for i in `ls $OUT_DIR | grep -v "harness_bin" | grep -v "pdf_gen"`
        do 
		
		# collecting APIs from each harness.cpp file
                echo $OUT_DIR"/"$i"/html_to_PDF_text_harness_template.cpp" >> $OUT_DIR/api_list
		cat -b $OUT_DIR/$i/html_to_PDF_text_harness_template.cpp | grep "FQL->" >> $OUT_DIR/api_list
        done
        
	# ranking harnesses by # of API and # of Args ~~~~~~~~~~~~
	python2 $SRC/src/harness/filter/ranking_harness_without_time.py $OUT_DIR/api_list $OUT_DIR/rank_list
	rm -rf $OUT_DIR/api_list
        

	# fuzzing harness ~~~~~~~~~~~~~~	
	while [ -s $OUT_DIR/rank_list ]; do

		# 1. best harness is the first line in "rank_list" 
		top_rank=$(head -n 1 $OUT_DIR/rank_list)
	        echo $top_rank

		# 2. compile the best harness to binary
	        $AFLpp_loc/afl-clang++ -g -O3 -funroll-loops -o $OUT_DIR/harness_bin/$top_rank -Wno-format -Wno-pointer-sign -I. -fpermissive -fPIC $OUT_DIR/$top_rank/html_to_PDF_text_harness_template.cpp $AFLpp_loc/afl-compiler-rt.o $AFLpp_loc/utils/afl_frida/libfrida-gum.a -ldl -lresolv -pthread -std=c++11
	        
		# remove the best harness from rank_list
		sed -i 1d $OUT_DIR/rank_list
		# remove the best harness's .cpp file
		rm -rf $OUT_DIR/$top_rank/
		
		# 3. run harness mutation fuzzing + PDF seeds migration
		# 3.1 : run harness fuzzing
		mkdir $OUT_DIR/harness$top_rank$DATE
		LD_LIBRARY_PATH=$foxit_loc/Libs/ $AFLpp_loc/afl-fuzz -m none -t 1000000+ -i $AFLpp_loc/testcases/others/pdf/ -o $OUT_DIR/harness$top_rank$DATE -- $OUT_DIR/harness_bin/$top_rank @@ &

		# 3.2 : while harness is being fuzzing, migrating pdf_gen/XX.pdf to queue/id:0000XX
		mkdir $QUEUE/$top_rank$DATE/
		mkdir $QUEUE/$top_rank$DATE/queue/
		# fuzzing running for 5m, 10m, 15m ...
		runtime="$TIME minute"
		endtime=$(date -ud "$runtime" +%s)
		pre_cnt=0
		# this loop keep running in next 5 mins
		while [[ $(date -u +%s) -le $endtime ]]
		do
			cur_cnt=`ls $OUT_DIR/pdf_gen/ | wc -l`
			increment_bool=`expr $pre_cnt \< $cur_cnt`
			
			if [[ $increment_bool == 1 ]]; then
				for i in $OUT_DIR/pdf_gen/*
				do 
					if grep -q "$i" $QUEUE/$top_rank$DATE/done_seeds
					then
						echo $i" has been migrated"
					else
						echo "NEW SEED : "$i
						len=${#pre_cnt}
						bond=`expr 5 - $len`
						zero=0
						
						for z in $(seq $bond)
						do 
							zero=$zero"0"
						done

						base=`echo $(basename $i) | cut -d . -f 1`
						
						name="id:"$zero$pre_cnt","$base
						mv $i $QUEUE/$top_rank$DATE/queue/$name
						echo $i >> $QUEUE/$top_rank$DATE/done_seeds
						let "pre=pre+1"
					fi
				done
			fi
		done
					
   
		# 4. kill current harness fuzzing by PID after running a while(5m, 10m, 15m ...)
		while read line 
		do 
			if [[ "$line" == *"fuzzer_pid"* ]]; then
		        	PID=`echo $line | cut -d : -f 2`
				kill $PID
			fi
		done < $OUT_DIR/harness$top_rank$DATE/default/fuzzer_stats
		
	done

fi
