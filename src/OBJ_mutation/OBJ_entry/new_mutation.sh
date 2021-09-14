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

if [[ $foxit_loc == "" ]]; then
	        echo "please provide foxit_loc path in var.config"
		        exit -1
fi

if [[ $AFLpp_loc == "" ]]; then
	        echo "please provide AFLpp_loc path in var.config"
		        exit -1
fi

if [[ $IN_DIR == "" ]]; then
	        echo "please provide IN_DIR path in var.config"
		        exit -1
fi

if [[ $OUT_DIR == "" ]]; then
	        echo "please provide OUT_DIR path in var.config"
		        exit -1
fi

if [[ $SRC == "" ]]; then
	        echo "please provide SRC path in var.config"
		        exit -1
fi

if [[ $EVAL_BIN == "" ]]; then
	        echo "please provide QUEUE path in var.config"
		        exit -1
fi

mkdir $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/
mkdir $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue
mkdir $OUT_DIR/entry_gen/
while true; do 
	pre_cnt=`ls $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue |wc -l`
	for queue in `find $EVAL_BIN/result/test_run_$DATE/ -name "queue" | grep -v -e "afl_" -e "obj_"`; do 
	
		harness_queue_path=`dirname $queue`
	
		for seed in $harness_queue_path/queue/*; do

                        echo ")))))))))))))))))))))))))))))) processing $seed "
	
			diff -y -a $EVAL_BIN/bin/init/pdf_org.pdf $seed > $OUT_DIR/org_diff
	
			python2.7 $SRC/src/OBJ_mutation/OBJ_entry/grammar_reserved_mutation.py $OUT_DIR/org_diff $seed $OUT_DIR/entry_gen/
			for i in $OUT_DIR/entry_gen/*; do
                                # TRIM PDFs : trim PDFs before renaming
                                mkdir $OUT_DIR/entry_gen/trim/

                                mv $i $OUT_DIR/entry_gen/trim/

                                python3.5 $SRC/scripts/trim_tool/new_trim_pdf.py -i $OUT_DIR/entry_gen/trim/ -b $COMMAND -s $AFL/afl-showmap -m none -t 100000 -o $OUT_DIR/entry_gen/
                                rm -rf $OUT_DIR/entry_gen/trim/
                                
                                # RENAMing : renaming 
				len=${#pre_cnt}
				bond=`expr 5 - $len`
				zero=0
	
	                        for z in $(seq $bond)
				do
					zero=$zero"0"
				done
	
				base=`echo $(basename $seed) | cut -d , -f 2`
	
				tp=$(basename $i)
	
				name="id:"$zero$pre_cnt","$base","$tp
	
				mv $i $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue/$name
				let "pre_cnt=pre_cnt+1"
			done
	
			rm -rf $OUT_DIR/org_diff
	
			rm -rf $OUT_DIR/entry_gen/*
	
		done
	done
done	
