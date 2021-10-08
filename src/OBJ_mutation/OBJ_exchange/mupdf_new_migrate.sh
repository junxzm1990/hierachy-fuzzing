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

#sleep 7m
while true; do

	if [ -z "$(ls -A $OUT_DIR/tmp_obj_exchange/)" ]; then
	
		echo "NO NEW SEEDS YET-BE PATIENT"
	
	else 
	
	        pre_cnt=`ls $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/ | wc -l`


	                for new in $OUT_DIR/tmp_obj_exchange/*; do

                                if [ "$(( $(date +"%s") - $(stat -c "%Y" $new) ))" -gt "1000" ]; then

	                        	mkdir $OUT_DIR/tmp_obj_exchange_trim_in/
	                        	mkdir $OUT_DIR/tmp_obj_exchange_trim_out/
	                        	cp $new $OUT_DIR/tmp_obj_exchange_trim_in/
	                        	# TRIM PDFs ------------------------------------
	                        	python3 $SRC/scripts/trim_tool/new_trim_pdf.py -i $OUT_DIR/tmp_obj_exchange_trim_in/ -b $COMMAND -s $AFLpp_loc/afl-showmap -m none -t 100000 -o $OUT_DIR/tmp_obj_exchange_trim_out/
	                        	if [ -z "$(ls -A $OUT_DIR/tmp_obj_exchange_trim_out/)" ]; then
						 # Compare if new trimed seed is less than 0.5M
                               			 max_size=500000
                               			 file_size=$(stat -c%s $new)
                                	         file_size="${file_size//[$'\t\r\n ']}"

                               			 if (( $file_size > $max_size )); then

                               			          # delete the large seed from /tmp_obj_exchange
                               			          rm -rf $new
                               			          # delete the in and out directories
                               			          rm -rf $OUT_DIR/tmp_obj_exchange_trim_in/ 
                               			          rm -rf $OUT_DIR/tmp_obj_exchange_trim_out/

                               			 else

	                        	               	  # RENAMing before migrating
	                        	               	  len=${#pre_cnt}
	                        	               	  bond=`expr 5 - $len`
	                        	               	  zero=0
	
	                        	               	  for z in $(seq $bond)
	                        	               	  do
	                        	               	          zero=$zero"0"
	                        	               	  done
	                        	               	  base=`echo $(basename $new) | cut -d , -f 2`
	
	                        	               	  name="id:"$zero$pre_cnt","$base
	
	                        	               	  mv $new $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/$name
	                        			  let "pre_cnt=pre_cnt+1"
	                                	          rm -rf $new
						fi
	                        	else

						 # Compare if new trimed seed is less than 0.5M
                               			 max_size=500000
                               			 file_size=$(stat -c%s $OUT_DIR/tmp_obj_exchange_trim_out/*)
                                	         file_size="${file_size//[$'\t\r\n ']}"

                               			 if (( $file_size > $max_size )); then
                               			          # delete the large seed from /tmp_obj_exchange
                               			          rm -rf $new
                               			          # delete the in and out directories
                               			          rm -rf $OUT_DIR/tmp_obj_exchange_trim_in/ 
                               			          rm -rf $OUT_DIR/tmp_obj_exchange_trim_out/

                               			 else
	                        	        	  # Compare trimed and untrimed, which one is smaller
	                        	        	  I=`wc -c $OUT_DIR/tmp_obj_exchange_trim_in/* | cut -d ' ' -f 1`
	                        	        	  O=`wc -c $OUT_DIR/tmp_obj_exchange_trim_out/* | cut -d ' ' -f 1`

						          I="${I//[$'\t\r\n ']}"
                                	                  O="${O//[$'\t\r\n ']}"		
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
	
	                        	        	          mv $OUT_DIR/tmp_obj_exchange_trim_out/* $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/$name
	                        				  let "pre_cnt=pre_cnt+1"
	                                			  rm -rf $new
	                        	        	  else
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
	
	                        	        	          mv $OUT_DIR/tmp_obj_exchange_trim_in/* $EVAL_BIN/result/test_run_$DATE/obj_exchange/queue/$name
	                                			  rm -rf $new
	                        				  let "pre_cnt=pre_cnt+1"
	
	                        	        	  fi
                                		fi
	
	
	                        	fi
	                        	rm -rf $OUT_DIR/tmp_obj_exchange_trim_in/
	                        	rm -rf $OUT_DIR/tmp_obj_exchange_trim_out/
	

                                 fi
	                done
	
	fi
 
done
