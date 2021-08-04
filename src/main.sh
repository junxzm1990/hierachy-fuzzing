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

if [[ $QUEUE == "" ]]; then
        echo "please provide QUEUE path in var.config"
        exit -1
fi

# handling harness generating, filtering, compiling, fuzzing and output migration
bash $SRC/src/harness/harness_compile_fuzzing_migrate.sh -c $CONFIG
		
