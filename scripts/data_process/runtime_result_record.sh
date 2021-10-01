while getopts r:v:o: option
do
        case "${option}"
        in
        r) RS_PATH=${OPTARG};; #path to the result folder
        v) VS_PATH=${OPTARG};; #path to the vanilla result folder
        o) OUT_PATH=${OPTARG};; #path to the save the output

        esac
done


if [[ $RS_PATH == "" ]]; then
        echo "Please input the result folder path (-r)"
        exit -1
fi

if [[ $VS_PATH == "" ]]; then
        echo "Please input the vanilla result folder path (-v)"
        exit -1
fi

if [[ $OUT_PATH == "" ]]; then
        echo "Please input the output file path (-o)"
        exit -1
fi

hour_cnt=0

while true; do
 
        echo $hour_cnt"h" >> $OUT_PATH/hourly_result

	for i in $RS_PATH/*; do 
		echo $i >> $OUT_PATH/hourly_result
		echo `ls $i/queue|wc -l` >> $OUT_PATH/hourly_result 
		cat $i/fuzzer_stats|grep execs_per >> $OUT_PATH/hourly_result
	done

	echo "harness_execs/sec : " >> $OUT_PATH/hourly_result
 
	cat $OUT_PATH/default/fuzzer_stats | grep execs_per >> $OUT_PATH/hourly_result

	echo "harness seeds picked : " >> $OUT_PATH/hourly_result

	echo `ls $RS_PATH/afl_S_6/queue/|grep harness|wc -l` >> $OUT_PATH/hourly_result

	echo "obj exchange seeds picked : " >> $OUT_PATH/hourly_result

	echo `ls $RS_PATH/afl_S_6/queue/|grep obj_ex|wc -l` >> $OUT_PATH/hourly_result

	echo "obj entry seeds picked " >> $OUT_PATH/hourly_result

	echo `ls $RS_PATH/afl_S_6/queue/|grep obj_en|wc -l` >> $OUT_PATH/hourly_result

	
	for j in $VS_P/*; do 
		echo $j >> $OUT_PATH/hourly_result
		echo `ls $j/queue|wc -l` >> $OUT_PATH/hourly_result
		cat $j/fuzzer_stats|grep execs_per >> $OUT_PATH/hourly_result
	done


        echo "---------------------------------------------------------------------" >>  $OUT_PATH/hourly_result

	sleep 1h
        
	let "hour_cnt=hour_cnt+1"
done
