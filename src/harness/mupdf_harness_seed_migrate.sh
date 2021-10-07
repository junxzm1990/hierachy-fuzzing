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

pre_cnt=0

# migrating pdf files from pdf_gen/ to harness queue 
while true
do
        cur_cnt=`ls $OUT_DIR/pdf_gen/ | wc -l`
        increment_bool=`expr $pre_cnt \< $cur_cnt`

        if [[ $increment_bool == 1 ]]; then
                for i in $OUT_DIR/pdf_gen/*
                do
                        if grep -q "$i" $EVAL_BIN/result/test_run_$DATE/harness_gen/done_seeds
                        then
                                echo $i" has been migrated" 
                        else
                                echo "NEW SEED : "$i 
                                ## 2.2.1 TRIM PDF files : before migrating the pdf_gen/XX.pdf to queue/id:000XX, reduce its size

                                mkdir $OUT_DIR/pdf_gen_trim_in/
                                mkdir $OUT_DIR/pdf_gen_trim_out/

                                cp $i $OUT_DIR/pdf_gen_trim_in/

                                python3 $SRC/scripts/trim_tool/new_trim_pdf.py -i $OUT_DIR/pdf_gen_trim_in/ -b $COMMAND -s $AFLpp_loc/afl-showmap -m none -t 100000 -o $OUT_DIR/pdf_gen_trim_out/

                                # Compare if new trimed seed is less than 0.6M
                                max_size=500000
                                file_size=$(stat -c%s $OUT_DIR/pdf_gen_trim_out/*)

                                if [ "$file_size" -gt "$max_size" ] ; then
						
 					 # delete the large seed from /pdf_gen
                                         rm -rf $i
                                         # delete the in and out directories
                               		 rm -rf $OUT_DIR/pdf_gen_trim_in/
                               		 rm -rf $OUT_DIR/pdf_gen_trim_out/

                                else

                               		 # Compare trimed and untrimed, which one is smaller
                               		 I=`wc -c $OUT_DIR/pdf_gen_trim_in/* | cut -d ' ' -f 1`
                               		 O=`wc -c $OUT_DIR/pdf_gen_trim_out/* | cut -d ' ' -f 1`
                               		 if [ "$I" -gt "$O" ]; then
                               		         ## 3.2.2 RENAMING : rename reduced size PDFs
                               		         len=${#pre_cnt}
                               		         bond=`expr 5 - $len`
                               		         zero=0

                               		         for z in $(seq $bond)
                               		         do
                               		                 zero=$zero"0"
                               		         done

                               		         base=`echo $(basename $i) | cut -d . -f 1`

                               		         name="id:"$zero$pre_cnt","$base
			       		 	
                               		         mv $OUT_DIR/pdf_gen_trim_out/* $EVAL_BIN/result/test_run_$DATE/harness_gen/queue/$name
                               		 else 
                               		         ## 3.2.2 RENAMING : rename reduced size PDFs
                               		         len=${#pre_cnt}
                               		         bond=`expr 5 - $len` 
                               		         zero=0 
                               		         for z in $(seq $bond)
                               		         do 
                               		                 zero=$zero"0" 
                               		         done
                
                               		         base=`echo $(basename $i) | cut -d . -f 1` 

                               		         name="id:"$zero$pre_cnt","$base 

                               		         mv $OUT_DIR/pdf_gen_trim_in/* $EVAL_BIN/result/test_run_$DATE/harness_gen/queue/$name

                               		 fi
                               		 rm -rf $OUT_DIR/pdf_gen_trim_in/
                               		 rm -rf $OUT_DIR/pdf_gen_trim_out/

                               		 echo $i >> $EVAL_BIN/result/test_run_$DATE/harness_gen/done_seeds 
                               		 let "pre_cnt=pre_cnt+1" 
                        	fi
                        fi
                done
        fi
done
                  
