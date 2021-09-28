while getopts c: option 
do
        case "${option}"
        in
        c) CONFIG=${OPTARG};;
        esac
done

. $CONFIG

# run  harness AFL++ fuzzing
$GO run $MAIN_GO -afl $AFL/afl-fuzz -i $EVAL_BIN/bin/seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/test_run_$DATE -n $NUM -- $COMMAND

# run villnia AFL++ fuzzing
v_NUM=`expr $NUM + 3` # running vanilla with 3 more, since harness
$GO run $MAIN_GO -afl $AFL/afl-fuzz -i $EVAL_BIN/bin/vanilla_seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/vanilla_test_run_$DATE -n $v_NUM -- $COMMAND

