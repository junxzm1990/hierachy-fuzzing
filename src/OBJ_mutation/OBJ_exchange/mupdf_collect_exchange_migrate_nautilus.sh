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


#mkdir $EVAL_BIN/result/nautilus_test_run_$DATE/obj_nautilus/
#mkdir $EVAL_BIN/result/nautilus_test_run_$DATE/obj_nautilus/queue/

while true; do

	if  [ -z "$(ls -A $EVAL_BIN/result/nautilus_test_run_$DATE/afl_S_0/queue/)" ]; then
	
		echo "NO NEW SEEDS YET-LET's WAIT"
	
	else 

        	echo ">>>>>>>>>>>>>>>> NOW collecting OBJs from ALL <<<<<<<<<<<<<<<<<<<<<<<<"
        	python2.7 $SRC/src/OBJ_mutation/OBJ_exchange/new_generator.py $SRC/src/OBJ_mutation/OBJ_exchange/class_obj_hongbin.json $EVAL_BIN/result/nautilus_test_run_$DATE/afl_S_0/queue/ $EVAL_BIN/result/nautilus_test_run_$DATE/obj_nautilus/queue/ 25
		
		
	fi 
done
