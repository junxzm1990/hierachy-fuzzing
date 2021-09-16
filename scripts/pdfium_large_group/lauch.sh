while getopts m:f:i:o:e:c:b:d: option
do
        case "${option}"
        in
        m) MAIN_GO=${OPTARG};;
        f) FUZZER=${OPTARG};;
        i) INPUT=${OPTARG};;
        o) OUTPUT=${OPTARG};;
        e) DATE=${OPTARG};;
        c) COMMAND=${OPTARG};;
        b) BIN_PATH=${OPTARG};;
        d) DICT=${OPTARG};;
        esac

done

if [[ $MAIN_GO == "" ]]; then
        echo "Please provide main.go directory(-m)"
        exit -1
fi

if [[ $FUZZER == "" ]]; then
        echo "Please provide afl-fuzz directory(-f)"
        exit -1
fi

if [[ $INPUT == "" ]]; then
        echo "Please provide seed directory(-i)"
        exit -1
fi

if [[ $OUTPUT == "" ]]; then
        echo "Please provide output directory(-o)"
        exit -1
fi

if [[ $DATE == "" ]]; then
        echo "Please provide instances date(-e)"
        exit -1
fi

if [[ $COMMAND == "" ]]; then
        echo "Please provide target command line with qoute(-c)"
        exit -1
fi

if [[ $BIN_PATH == "" ]]; then
        echo "Please provide bin path(-b)"
        exit -1
fi

if [[ $DICT == "" ]]; then
        echo "Please provide dict(-d)"
        exit -1
fi

/archive/go/bin/go run $MAIN_GO -afl $FUZZER -i $INPUT -no-master -name afl -m none -x $DICT -o $OUTPUT/group1_with_split_16_$DATE -n 16 -- $COMMAND

/archive/go/bin/go run $MAIN_GO -afl $FUZZER -i $INPUT -no-master -name afl -m none -x $DICT -o $OUTPUT/group2_with_split_16_$DATE -n 16 -- $COMMAND

/archive/go/bin/go run $MAIN_GO -afl $FUZZER -i $INPUT -no-master -name afl -m none -x $DICT -o $OUTPUT/group3_with_split_16_$DATE -n 16 -- $COMMAND

