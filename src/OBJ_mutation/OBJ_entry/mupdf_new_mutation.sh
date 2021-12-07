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


#sleep 3m

while true; do

	if  [ -z "$(ls -A $OUT_DIR/pdf_gen/)" ]; then
	
		echo "NO NEW SEED YET-LET's WAIT"
	
	else
	
		if [ ! -d "$OUT_DIR/entry_gen/" ]
                then
			mkdir $OUT_DIR/entry_gen/
                fi
	 
	
	
	        pre_cnt=`ls $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue |wc -l`
	
	        for seed in $OUT_DIR/pdf_gen/*; do
	
	                echo ")))))))))))))))))))))))))))))) processing $seed "
	
	                diff -y -a $EVAL_BIN/bin/init/pdf_org.pdf $seed > $OUT_DIR/org_diff
	
	                python2.7 $SRC/src/OBJ_mutation/OBJ_entry/grammar_reserved_mutation.py $OUT_DIR/org_diff $seed $OUT_DIR/entry_gen/

	
	        done
	fi	
done
