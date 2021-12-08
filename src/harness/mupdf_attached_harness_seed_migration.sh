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


while true; do

	if [ -z "$(ls -A $MAIN_GROUP/result/test_run_$DATE/harness_gen/)" ]; then
		
		echo "NO NEW HARNESS SEEDS YET - LET's WAIT"

		sleep 1m

	else 

		echo ">>>>>>>>>>>>>>>> NOW cp seeds from main_target/harness_gen/ <<<<<<<<<<<<<<<<<<<<<<<<"
		
		for harness_gen_seed in $MAIN_GROUP/result/test_run_$DATE/harness_gen/queue/*;
		do

			if grep -q "$harness_gen_seed" $EVAL_BIN/result/test_run_$DATE/harness_gen/done_harness_list; 
			then
				echo "processed this seed"
			else 
				cp $harness_gen_seed $EVAL_BIN/result/test_run_$DATE/harness_gen/queue/
				echo $harness_gen_seed >> $EVAL_BIN/result/test_run_$DATE/harness_gen/done_harness_list
			fi

		done

		echo ">>>>>>>>>>>>>>>> NOW cp seeds from main_target/obj_exchange/ <<<<<<<<<<<<<<<<<<<<<<<<"
		
		for obj_exchange_seed in $MAIN_GROUP/result/test_run_$DATE/obj_exchange/queue/*;
		do

			if grep -q "$obj_exchange_seed" $EVAL_BIN/result/test_run_$DATE/obj_exchange/done_obj_exchange_list; 
			then
				echo "processed this seed"
			else 
				cp $obj_exchange_seed $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/
				echo $obj_exchange_seed >> $EVAL_BIN/result/test_run_$DATE/obj_exchange/done_obj_exchange_list
			fi

		done

		echo ">>>>>>>>>>>>>>>> NOW cp seeds from main_target/obj_entry_mutation/ <<<<<<<<<<<<<<<<<<<<<<<<"
		
		for obj_entry_seed in $MAIN_GROUP/result/test_run_$DATE/obj_entry_mutation/queue/*;
		do

			if grep -q "$obj_entry_seed" $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/done_obj_entry_list; 
			then
				echo "processed this seed"
			else 
				cp $obj_entry_seed $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue/
				echo $obj_entry_seed >> $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/done_obj_entry_list
			fi

		done

	fi


done
