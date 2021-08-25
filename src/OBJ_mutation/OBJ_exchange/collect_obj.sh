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

#if [[ $IN_DIR == "" ]]; then
#        echo "Please provide the input directory(-i)"
#        exit -1
#fi
#
#if [[ $OUT_DIR == "" ]]; then
#        echo "Please provide the output directory ---- the harness_queue(-o)"
#        exit -1
#fi
#
#if [[ $DATE == "" ]]; then
#        echo "Please provide the DATE(-t)"
#        exit -1
#fi

# load config file
. $CONFIG

for i in 


# ------------------------------------

for i in $IN_DIR/* 
do 
	OBJ_bool=0
        cnt=0
        file=$i
	while read line 
	do
		if [[ "$line" == *"0 obj"* ]]; then
	                OBJ_bool=1
                        (( cnt++ ))
			echo $line >> $OUT_DIR/global
	        elif [[ "$line" == "endobj" ]]; then
	                OBJ_bool=0
			echo $line >> $OUT_DIR/global
	        elif [[ $OBJ_bool == 1 ]]; then
			echo $line >> $OUT_DIR/global
		fi
	done < "$file"
	echo $i >> $OUT_DIR/seed_cnt
	echo $cnt >> $OUT_DIR/seed_cnt
done

python xxxx $OUT_DIR/global $OUT_DIR/seed_cnt $OUTPUT/OBJ_LEV_GEN/
