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
v_NUM=`expr $NUM + 1` # running vanilla with 3 more, since harness + obj exchang + entry mutation in our framework
$GO run $MAIN_GO -afl $AFLpp_loc/afl-fuzz -i $EVAL_BIN/bin/vanilla_seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/vanilla_test_run_$DATE -n $v_NUM -- $COMMAND

# ----------------------------------  for multiple harness test experiment , please make following code aviliable --------------------------------------------------
# run MOpt fuzzing 
m_NUM=`expr $NUM + 1` # running 3 more 
$GO run $MAIN_GO -afl $MOpt_loc/afl-fuzz -i $EVAL_BIN/bin/seed_mopt/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/mopt_test_run_$DATE -n $m_NUM -- $M_COMMAND

# run nautilus fuzzing
$GO run $MAIN_GO -afl $AFLpp_loc/afl-fuzz -i $EVAL_BIN/bin/vanilla_seed/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/nautilus_test_run_$DATE -n $NUM -- $COMMAND

# create generated seed container for nautilus(obj_exchange)
mkdir $EVAL_BIN/result/nautilus_test_run_$DATE/obj_nautilus/

mkdir $EVAL_BIN/result/nautilus_test_run_$DATE/obj_nautilus/queue/

# run Learn&Fuzz
$GO run $MAIN_GO -afl $AFLpp_loc/afl-fuzz -i $EVAL_BIN/bin/seed_learn_cmined/ -no-master -name afl -m none -t 100000 -o $EVAL_BIN/result/learnfuzz_test_run_$DATE -n $NUM -- $COMMAND
