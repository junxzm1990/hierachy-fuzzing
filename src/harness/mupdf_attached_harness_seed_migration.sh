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
		
		for harness_gen_seed in $MAIN_GROUP/harness_gen/*;
		do

			if grep -q "$harness_gen_seed" $EVAL_BIN/result/test_run_$DATE/done_harness_list; 
			then
				echo "processed this seed"
			else 
				cp $harness_gen_seed $EVAL_BIN/result/test_run_$DATE/harness_gen/
				echo $harness_gen_seed >> $EVAL_BIN/result/test_run_$DATE/done_harness_list
			fi

		done

		echo ">>>>>>>>>>>>>>>> NOW cp seeds from main_target/obj_exchange/ <<<<<<<<<<<<<<<<<<<<<<<<"
		
		for obj_exchange_seed in $MAIN_GROUP/obj_exchange/*;
		do

			if grep -q "$obj_exchange_seed" $EVAL_BIN/result/test_run_$DATE/done_obj_exchange_list; 
			then
				echo "processed this seed"
			else 
				cp $obj_exchange_seed $EVAL_BIN/result/test_run_$DATE/obj_exchange/
				echo $obj_exchange_seed >> $EVAL_BIN/result/test_run_$DATE/done_obj_exchange_list
			fi

		done

		echo ">>>>>>>>>>>>>>>> NOW cp seeds from main_target/obj_entry_mutation/ <<<<<<<<<<<<<<<<<<<<<<<<"
		
		for obj_entry_seed in $MAIN_GROUP/obj_entry_mutation/*;
		do

			if grep -q "$obj_entry_seed" $EVAL_BIN/result/test_run_$DATE/done_obj_entry_list; 
			then
				echo "processed this seed"
			else 
				cp $obj_entry_seed $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/
				echo $obj_entry_seed >> $EVAL_BIN/result/test_run_$DATE/done_obj_entry_list
			fi

		done

	fi


done
