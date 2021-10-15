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

if [[ $EVAL_BIN == "" ]]; then
                echo "please provide QUEUE path in var.config"
                        exit -1
fi


sleep 3m

while true; do

	if  [ -z "$(ls -A $OUT_DIR/pdf_gen/)" ]; then
	
		echo "NO NEW SEED YET-LET's WAIT"
	
	else
	 
		mkdir $OUT_DIR/entry_gen/
	
	
	        pre_cnt=`ls $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue |wc -l`
	
	        for seed in $OUT_DIR/pdf_gen/*; do
	
	                echo ")))))))))))))))))))))))))))))) processing $seed "
	
	                diff -y -a $EVAL_BIN/bin/init/pdf_org.pdf $seed > $OUT_DIR/org_diff
	
	                python2.7 $SRC/src/OBJ_mutation/OBJ_entry/grammar_reserved_mutation.py $OUT_DIR/org_diff $seed $OUT_DIR/entry_gen/

                        sleep 12m
			
			for i in $OUT_DIR/entry_gen/*; do

				# TRIM PDFs : trim PDFs before renaming
	                        mkdir $OUT_DIR/entry_gen_trim_in/
	                        mkdir $OUT_DIR/entry_gen_trim_out/
	
	                        cp $i $OUT_DIR/entry_gen_trim_in/
	
	                        python3 $SRC/scripts/trim_tool/new_trim_pdf.py -i $OUT_DIR/entry_gen_trim_in/ -b $COMMAND -s $AFLpp_loc/afl-showmap -m none -t 100000 -o $OUT_DIR/entry_gen_trim_out/
	
	                        if [ -z "$(ls -A $OUT_DIR/entry_gen_trim_out/)" ]; then

                                	 # Compare if new trimed seed is less than 0.6M
                               		 max_size=500000
                               		 file_size=$(stat -c%s $i)
			       		 file_size="${file_size//[$'\t\r\n ']}"

                               		 if (( $file_size > $max_size )); then
                               		          # delete the large seed from /entry_gen
                               		          rm -rf $i
                               		          # delete the in and out directories
                               		          rm -rf $OUT_DIR/entry_gen_trim_in/
                               		          rm -rf $OUT_DIR/entry_gen_trim_out/

                               		 else
	                        	          # RENAMing before migrating
	                        	          len=${#pre_cnt}
	                        	          bond=`expr 5 - $len`
	                        	          zero=0
	
	                        	          for z in $(seq $bond)
	                        	          do
	                        	                  zero=$zero"0"
	                        	          done
	                        	          echo $i
	                        	          base=`echo $(basename $i) | cut -d , -f 2`
	
	                        	          name="id:"$zero$pre_cnt","$base
	
	                        	          mv $i $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue/$name
	                        	       	  let "pre_cnt=pre_cnt+1"
			       		fi

	                        else

			       		 # Compare if new trimed seed is less than 0.6M
                               		 max_size=500000
                               		 file_size=$(stat -c%s $OUT_DIR/entry_gen_trim_out/*)
			       		 file_size="${file_size//[$'\t\r\n ']}"

                               		 if (( $file_size > $max_size )); then

                               		          # delete the large seed from /entry_gen
                               		          rm -rf $i
                               		          # delete the in and out directories
                               		          rm -rf $OUT_DIR/entry_gen_trim_in/
                               		          rm -rf $OUT_DIR/entry_gen_trim_out/

                               		 else

	                        	          # Compare trimed and untrimed, which one is smaller
	                        	          I=`wc -c $OUT_DIR/entry_gen_trim_in/* | cut -d ' ' -f 1`
	                        	          O=`wc -c $OUT_DIR/entry_gen_trim_out/* | cut -d ' ' -f 1`
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
	
	                        	                  base=`echo $(basename $i) | cut -d , -f 2`
	
			       		 	  	  name="id:"$zero$pre_cnt","$base
	
	                        	                  mv $OUT_DIR/entry_gen_trim_out/* $EVAL_BIN/result/test_run_$DATE/obj_entry_mutation/queue/$name
	                        			  let "pre_cnt=pre_cnt+1"
                                	                  rm -rf $i

			       			  else
                                	        	  ## 3.2.2 RENAMING : rename reduced size PDFs
                                	        	  len=${#pre_cnt}
                                	        	  bond=`expr 5 - $len`
                                	        	  zero=0
                                	        	  for z in $(seq $bond)
                                	        	  do
                                	        	          zero=$zero"0"
                                	        	  done

                                	        	  base=`echo $(basename $i) | cut -d , -f 2`

                                	        	  name="id:"$zero$pre_cnt","$base

                                	        	  mv $OUT_DIR/entry_gen_trim_in/* $EVAL_BIN/result/test_run_$DATE/obj_entry_gen/queue/$name
	                        			  let "pre_cnt=pre_cnt+1"
			       			  	  rm -rf $i
	                        	         fi
			       		fi
	
	
	
	                        fi
	
	                        rm -rf $OUT_DIR/entry_gen_trim_in/
	                        rm -rf $OUT_DIR/entry_gen_trim_out/
	                done
	
			rm -rf $OUT_DIR/entry_gen/*
	                rm -rf $OUT_DIR/org_diff
	
	        done
	fi	
done
