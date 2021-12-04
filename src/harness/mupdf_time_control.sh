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

runtime="$TIME minute"
endtime=$(date -ud "$runtime" +%s)

sleep 10m

while true; 
do
 
	while [[ $(date -u +%s) -le $endtime ]]; 
	do
	        echo "in time"
        done
	while read line; 
	do
	        if [[ "$line" == *"fuzzer_pid"* ]]; then
	                PID=`echo $line | cut -d : -f 2`
	                kill $PID
	        fi
	done < $OUT_DIR/harness$top_rank$DATE/default/fuzzer_stats
	rm -rf $OUT_DIR/harness$top_rank$DATE

done
