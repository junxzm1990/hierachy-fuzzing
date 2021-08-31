while getopts c: option
do
        case "${option}"
        in
        c) CONFIG=${OPTARG};;
	esac
done

if [[ $CONFIG == "" ]]; then
        echo "Please provide CONFIG file(-c)"
        exit -1
fi


# load config file
. $CONFIG

# create object exchange mutation queue, parallal with afl_S_X/queue and harness/queue
mkdir $EVAL_BIN/result/test_run_$DATE/obj_exchange/
mkdir $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/

echo ">>>>>>>>>>>>>>>> NOW collecting OBJs from ALL <<<<<<<<<<<<<<<<<<<<<<<<"

# collecting all objects from all PDF files generated from harness
for queue in `find $EVAL_BIN/result/test_run_$DATE -name "queue" | grep -v -e "afl_" -e "obj_"`; do 

	harness_queue_path=`dirname $queue`

	for seed in $harness_queue_path/queue/*; do 

		echo "[+] PROCESSING "$seed

		OBJ_bool=0
                while read line 
                do
                        if [[ "$line" == *"0 obj"* ]]; then
                                OBJ_bool=1
                               # (( cnt++ ))
                                echo $line >> $OUT_DIR/global
                        elif [[ "$line" == "endobj" ]]; then
                                OBJ_bool=0
                                echo $line >> $OUT_DIR/global
                        elif [[ $OBJ_bool == 1 ]]; then
                                echo $line >> $OUT_DIR/global
                        fi
                done < "$seed"
	done
done

pre_cnt=`ls $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/ | wc -l`

for queue in `find $EVAL_BIN/result/test_run_$DATE -name "queue" | grep -v -e "afl_" -e "obj_"`; do

	harness_queue_path=`dirname $queue`

	for seed in $harness_queue_path/queue/*; do 
	
		seed_name=$(basename "$seed")

                mkdir $OUT_DIR/$seed_name

		python2.7 $SRC/src/OBJ_mutation/OBJ_exchange/generator.py $OUT_DIR/global $seed $OUT_DIR/$seed_name/

                # migrate new generated seeds to queue
                for new in $OUT_DIR/$seed_name/*; do
	
			len=${#pre_cnt}
                        bond=`expr 5 - $len`
                        zero=0

                        for z in $(seq $bond)
                        do
                                zero=$zero"0"
                        done

                        base=`echo $(basename $seed_name) | cut -d , -f 2`
 
                        tp=$(basename $new)

			echo "hahahah : "$base","$tp

                        name="id:"$zero$pre_cnt","$base","$tp
                	
			mv $new $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/$name
  	
			echo "[-] OUTPUT "$new

			let "pre_cnt=pre_cnt+1"
 		done

		rm -rf $OUT_DIR/$seed_name
	done

done
                     
rm -rf $OUT_DIR/global

