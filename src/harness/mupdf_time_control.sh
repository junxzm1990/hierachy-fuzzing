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


#sleep 10m

runtime="$TIME minute"
endtime=$(date -ud "$runtime" +%s)

while true; 
do
	top_rank=$(head -n 1 $OUT_DIR/rank_list)
        echo $top_rank
        if [ -f $OUT_DIR/harness$top_rank$DATE/default/fuzzer_stats ];
	then 
                echo $endtime
		if  [[ $(date -u +%s) -ge $endtime ]]; 
		then

			echo "I AM HERE"
                        sed -i 1d $OUT_DIR/rank_list
			while read line; 
			do
			        if [[ "$line" == *"fuzzer_pid"* ]]; then
			                PID=`echo $line | cut -d : -f 2`
			                kill $PID
			        fi
			done < $OUT_DIR/harness$top_rank$DATE/default/fuzzer_stats
			rm -rf $OUT_DIR/harness$top_rank$DATE
			# remove the best harness from rank_list
			runtime="$TIME minute"
			endtime=$(date -ud "$runtime" +%s)

        	fi
	fi

done
