#while getopts i:o:t: option
#do
#        case "${option}"
#        in
#        i) IN_DIR=${OPTARG};;
#        o) OUT_DIR=${OPTARG};;
#        t) DATE=${OPTARG};;
#	esac
#done

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

for queue in `find $QUEUE -name "queue"` | grep -v "afl_"; do 

	harness_queue_path=`dirname $queue`

	for seed in $harness_queue_path/*; do 

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

for queue in `find $QUEUE -name "queue"` | grep -v "afl_"; do

	harness_queue_path=`dirname $queue`

	for seed in $harness_queue_path/*; do 

		python $SRC/src/OBJ_mutation/OBJ_exchange/generator.py $OUT_DIR/global $seed $OUTPUT/OBJ_LEV_GEN/




# ------------------------------------

