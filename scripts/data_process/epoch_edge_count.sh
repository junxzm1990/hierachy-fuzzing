while getopts b:s:p:e:n:o:t: option
do

	case "${option}"
        in
	b) BIN_PATH=${OPTARG};; #path to the binary
        p) TARGET_PATH=${OPTARG};; #path to the target directory of queues
	s) SHOWMAP_PATH=${OPTARG};; #path to the showmap
	o) OPTION=${OPTARG};; #target bin option
	t) START=${OPTARG};; #start time
	n) INST_NUM=${OPTARG};; # how many instances
	d) DEV=${OPTARG};; # if /dev/null needed 
	esac
done


if [[ $BIN_PATH == "" ]]; then
        echo "Please input the binary path (-b)"
        exit -1
fi

if [[ $SHOWMAP_PATH == "" ]]; then
        echo "Please input the showmap path (-s)"
        exit -1
fi

if [[ $TARGET_PATH == "" ]]; then
        echo "Please input the none split folder path (-p)"
        exit -1
fi

if [[ $START == "" ]]; then
        echo "Please input start time (-t)"
        exit -1
fi

if [[ $INST_NUM == "" ]]; then
        echo "Please instance number (-n)"
        exit -1
fi

{ echo 0 & echo 0; } > $TARGET_PATH/edge_count.txt

hour_cnt=1

edge_cnt=0

start_time=$START

while true; do 

	if [ $hour_cnt -lt 25 ]; then

		start=$(date -d @$start_time +'%Y-%m-%d %H:%M:%S')

		echo "AAAAAAAAAAAA"$start
		let "start_time=start_time+3600"

		end=$(date -d @$start_time +'%Y-%m-%d %H:%M:%S')

		echo "BBBBBBBBBBB"$end

		for queue in `find $TARGET_PATH -name "queue" | grep -v "harness" | grep -v "obj_" | grep -v "html"`; do
			echo "[+] NOW PROCESSING "$queue

			find $queue -newermt "$start" ! -newermt "$end"  > $TARGET_PATH/all_seeds.txt
			echo "CCCCCCCCCCCCCCC"`wc -l $TARGET_PATH/all_seeds.txt`

			cat $TARGET_PATH/all_seeds.txt | while read line; do

				$SHOWMAP_PATH -m none -t 100000  -o $TARGET_PATH/tmp.txt -q -- $BIN_PATH $OPTION $line $DEV
				cat $TARGET_PATH/tmp.txt >> $TARGET_PATH/uniq_edge.txt
				sort -u $TARGET_PATH/uniq_edge.txt -o $TARGET_PATH/uniq_edge.txt  
			done 

			rm -rf $TARGET_PATH/all_seeds.txt
			rm -rf $TARGET_PATH/tmp.txt
		done

		echo $hour_cnt >> $TARGET_PATH/edge_count.txt

		cur_uniq_edge=`sort $TARGET_PATH/uniq_edge.txt | uniq | wc -l`

		echo "FFFFFFFFFFFFFFFFFFF"$cur_uniq_edge

		cur_uniq_edge=`expr $cur_uniq_edge \/ $INST_NUM`

		echo "EEEEEEEEEEEEEEEEEE"$cur_uniq_edge

                # edge_cnt=`expr $edge_cnt + $cur_uniq_edge`

		echo $cur_uniq_edge >> $TARGET_PATH/edge_count.txt

		#rm -rf $TARGET_PATH/uniq_edge.txt

		date

		let "hour_cnt=hour_cnt+1"


	fi

done























