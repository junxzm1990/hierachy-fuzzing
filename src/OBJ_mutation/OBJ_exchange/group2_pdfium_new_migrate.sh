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


# load config file
. $CONFIG

# create object exchange mutation queue, parallal with afl_S_X/queue and harness/queue

while true; do 
	echo ">>>>>>>>>>>>>>>> SCANNING TMP dir <<<<<<<<<<<<<<<<<<<<<<<<"
	
	pre_cnt=`ls $EVAL_BIN/result/group2_with_split_16_$DATE/obj_exchange/queue/ | wc -l`
	# migrate new generated seeds to queue
        if [ -z "$(ls -A $OUT_DIR/tmp_obj_exchange/)" ]; then 
                echo "Current TMP dir is empty, waiting new seeds ... "
        else 
	        for new in $OUT_DIR/tmp_obj_exchange/*; do
                        mkdir $OUT_DIR/tmp_obj_exchange_trim_in/
                        mkdir $OUT_DIR/tmp_obj_exchange_trim_out/
                        cp $new $OUT_DIR/tmp_obj_exchange_trim_in/
                        # TRIM PDFs ------------------------------------
                        python3 $SRC/scripts/trim_tool/new_trim_pdf.py -i $OUT_DIR/tmp_obj_exchange_trim_in/ -b $COMMAND -s $AFL/afl-showmap -m none -t 100000 -o $OUT_DIR/tmp_obj_exchange_trim_out/
                        if [ -z "$(ls -A $OUT_DIR/tmp_obj_exchange_trim_out/)" ]; then
                        	# RENAMing before migrating
				len=${#pre_cnt}
	                	bond=`expr 5 - $len`
	                	zero=0
	
	                	for z in $(seq $bond)
	                	do
	                	        zero=$zero"0"
	                	done
	                	echo $new
	                	base=`echo $(basename $new) | cut -d , -f 2`
	
	                	name="id:"$zero$pre_cnt","$base
	        		
				mv $new $EVAL_BIN/result/group2_with_split_16_$DATE/obj_exchange/queue/$name
         		else
				# Compare trimed and untrimed, which one is smaller
                                I=`wc -c $OUT_DIR/tmp_obj_exchange_trim_in/* | cut -d ' ' -f 1`
                                O=`wc -c $OUT_DIR/tmp_obj_exchange_trim_out/* | cut -d ' ' -f 1`
                                if [ "$I" -gt "$O" ]; then
                                        ## 3.2.2 RENAMING : rename reduced size PDFs
                                        len=${#pre_cnt}
                                        bond=`expr 5 - $len` 
                                        zero=0 
                                        
                                        for z in $(seq $bond)
                                        do 
                                                zero=$zero"0" 
                                        done
                        
                                        base=`echo $(basename $new) | cut -d , -f 2` 
        
                                        name="id:"$zero$pre_cnt","$base 

                                        mv $OUT_DIR/tmp_obj_exchange_trim_out/* $EVAL_BIN/result/group2_with_split_16_$DATE/obj_exchange/queue/$name
                                else 
                                        ## 3.2.2 RENAMING : rename reduced size PDFs
                                        len=${#pre_cnt}
                                        bond=`expr 5 - $len` 
                                        zero=0 
                                        
                                        for z in $(seq $bond)
                                        do 
                                                zero=$zero"0" 
                                        done
                        
                                        base=`echo $(basename $new) | cut -d . -f 1` 
        
                                        name="id:"$zero$pre_cnt","$base 

                                        mv $OUT_DIR/tmp_obj_exchange_trim_in/* $EVAL_BIN/result/group2_with_split_16_$DATE/obj_exchange/queue/$name

                                fi


 
			fi
                        rm -rf $OUT_DIR/tmp_obj_exchange_trim_in/
                        rm -rf $OUT_DIR/tmp_obj_exchange_trim_out/
	
			echo "[-] OUTPUT "$new
	
			let "pre_cnt=pre_cnt+1"
		done

                rm -rf $OUT_DIR/tmp_obj_exchange/*

	fi
	                     
done	
