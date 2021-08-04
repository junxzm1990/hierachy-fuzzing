while getopts c:n: option 
do 
	case "${option}"
	in
	c) CONFIG=${OPTARG};;
        n) NUM=${OPTARG};;
	esac
done

if [[ $CONFIG == "" ]]; then
        echo "Please provide CONFIG file (-c)"
        exit -1
fi

if [[ $NUM == "" ]]; then
        echo "Please provide NUM of HTMLs (-n)"
        exit -1
fi

# load config file
. $CONFIG


if [[ $NUM == 1 ]]
then

        # 1. compile .cpp to harness bin ~~~~~~~~~~
        top_rank=`ls $OUT_DIR/ | grep -v "harness_bin" | grep -v "pdf_gen" | grep -v "rank_list"`
        $AFLpp_loc/afl-clang++ -g -O3 -funroll-loops -o $OUT_DIR/harness_bin/$top_rank -Wno-format -Wno-pointer-sign -I. -fpermissive -fPIC $OUT_DIR/$top_rank/html_to_PDF_text_harness_template.cpp $AFLpp_loc/afl-compiler-rt.o $SRC/src/harness/libfrida-gum.a -ldl -lresolv -pthread -std=c++11


        # 2. run harness mutation fuzzing ~~~~~~~~~~
        mkdir $OUT_DIR/harness$top_rank$DATE
        LD_LIBRARY_PATH=$foxit_loc/Libs/ $AFLpp_loc/afl-fuzz -m none -t 1000000+ -i $AFLpp_loc/testcases/others/pdf/ -o $OUT_DIR -- $OUT_DIR/harness_bin/$top_rank @@ &

        pre_cnt=0
        mkdir $QUEUE/$top_rank$DATE/
        mkdir $QUEUE/$top_rank$DATE/queue/


        # migrating pdf files from pdf_gen/ to harness queue 
        while true
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

else 

	# 1. best harness is the first line in "rank_list" 
	top_rank=$(head -n 1 $OUT_DIR/rank_list)
	echo $top_rank
	
	# 2. compile the best harness to binary
	$AFLpp_loc/afl-clang++ -g -O3 -funroll-loops -o $OUT_DIR/harness_bin/$top_rank -Wno-format -Wno-pointer-sign -I. -fpermissive -fPIC $OUT_DIR/$top_rank/html_to_PDF_text_harness_template.cpp $AFLpp_loc/afl-compiler-rt.o $SRC/src/harness/libfrida-gum.a -ldl -lresolv -pthread -std=c++11
	
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

fi
