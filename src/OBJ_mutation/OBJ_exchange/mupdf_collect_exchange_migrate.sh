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


while true; do

	if  [ -z "$(ls -A $OUT_DIR/pdf_gen/)" ]; then
	
		echo "NO NEW SEEDS YET-LET's WAIT"
	
	else 

        	echo ">>>>>>>>>>>>>>>> NOW collecting OBJs from ALL <<<<<<<<<<<<<<<<<<<<<<<<"
        	pre_cnt=`ls $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/ | wc -l`
                if [ ! -d "$OUT_DIR/tmp_obj_exchange/" ]
		then
        		mkdir $OUT_DIR/tmp_obj_exchange/
		fi

        	python2.7 $SRC/src/OBJ_mutation/OBJ_exchange/new_generator.py $SRC/src/OBJ_mutation/OBJ_exchange/class_obj.json $OUT_DIR/pdf_gen/ $OUT_DIR/tmp_obj_exchange/ 15
		
	fi 
done
