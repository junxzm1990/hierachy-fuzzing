while getopts c: option 
do
        case "${option}"
        in
        c) CONFIG=${OPTARG};;
        esac
done

. $CONFIG

# run  harness AFL++ fuzzing
$GO run $MAIN_GO -afl $AFLpp_loc/afl-fuzz -i $EVAL_BIN/bin/seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/test_run_$DATE -n $NUM -- $COMMAND

# these two dir has to be created there no move
mkdir $EVAL_BIN/result/test_run_$DATE/harness_gen/

mkdir $EVAL_BIN/result/test_run_$DATE/harness_gen/queue/

mkdir $EVAL_BIN/result/test_run_$DATE/obj_exchange/

mkdir $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/

mkdir $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/

mkdir $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue

# run villnia AFL++ fuzzing
v_NUM=`expr $NUM + 3` # running vanilla with 3 more, since harness
$GO run $MAIN_GO -afl $AFLpp_loc/afl-fuzz -i $EVAL_BIN/bin/vanilla_seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/vanilla_test_run_$DATE -n $v_NUM -- $COMMAND
