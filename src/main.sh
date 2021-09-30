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

if [[ $TIME == "" ]]; then
        echo "please provide how long you want to run on each harness in var.config"
        exit -1
fi

if [[ $DATE == "" ]]; then
        echo "please provide today's date in var.config"
        exit -1
fi

if [[ $NUM == "" ]]; then
        echo "please provide how many AFL++ instance you want to run in var.config"
        exit -1
fi

if [[ $MAIN_GO == "" ]]; then
        echo "please provide main.go path in var.config"
        exit -1
fi

if [[ $COMMAND == "" ]]; then
        echo "please provide COMMAND you want to run in AFL++ fuzzing in var.config"
        exit -1
fi

if [[ $GO == "" ]]; then
        echo "please provide path of go in var.config"
        exit -1
fi

while IFS= read -r line; do 
	echo "$line -c $CONFIG" >> $SRC/src/commands_opt
done < $SRC/src/commands

parallel -j0 < $SRC/src/commands_opt


## run  harness AFL++ fuzzing
#$GO run $MAIN_GO -afl $AFL/afl-fuzz -i $EVAL_BIN/bin/seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/test_run_$DATE -n $NUM -- $COMMAND
#
## run villnia AFL++ fuzzing
#v_NUM=`expr $NUM + 3` # running vanilla with 3 more, since harness
#$GO run $MAIN_GO -afl $AFL/afl-fuzz -i $EVAL_BIN/bin/vanilla_seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/vanilla_test_run_$DATE -n $v_NUM -- $COMMAND
#
# handling harness generating, filtering, compiling, fuzzing and output migration
#bash $SRC/src/harness/mupdf_new_harness_compile_fuzzing_migrate.sh -c $CONFIG

# handling objects exhanging based on object types
#bash $SRC/src/OBJ_mutation/OBJ_exchang/collect_exchange_migrate.sh -c $CONFIG

