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

# 1. wget the webside to one directory as outer HTML;
# 2. check current running harness, run google-chrome headless and save the output to one directory as inner HTML;
# 3. merge inner HTML + outer HTML; 
# 4. rename it; 
# 5. migrate to the queue.
pre_cnt=0 
while true; do 
	wget http://0.0.0.0:9090 -P $HARNESS_OUT

	google-chrome-stable --headless --dump-dom  http://0.0.0.0:9090

	head -n -2 $HARNESS_OUT/index.html > $HARNESS_OUT/tmp.html
	cat $HARNESS_OUT/innher_HTML >> $HARNESS_OUT/tmp.html
	echo "</body>" >> $HARNESS_OUT/tmp.html
	echo "</html>" >> $HARNESS_OUT/tmp.html

	rm -rf $HARNESS_OUT/index.html
	rm -rf $HARNESS_OUT/innher_HTML

	len=${#pre_cnt}
	bond=`expr 5 - $len`
	zero=0
	for z in $(seq $bond)
	do
		zero=$zero"0"
	done

	base=`echo $RANDOM | md5sum | head -c 10`

	name="id:"$zero$pre_cnt","$base

	mv $HARNESS_OUT/tmp.html $HARNESS_OUT/queue/$name

	let "pre_cnt++"

	sleep 1s
done
