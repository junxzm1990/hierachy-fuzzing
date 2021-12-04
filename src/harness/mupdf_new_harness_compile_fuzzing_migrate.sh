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

#mkdir $OUT_DIR
#
#mkdir $OUT_DIR/pdf_gen/
#
#mkdir $OUT_DIR/harness_bin/

# --------------- .cpp GENERATION -----------------------------------------------------------
for h in $IN_DIR/*
do
	if [[ $h == *.html ]]; then 
        	python2.7 $SRC/src/harness/generator/overall_html_harness_parser.py $h $OUT_DIR $OUT_DIR/pdf_gen/ $foxit_loc $AFLpp_loc
	elif [[ $h == *.pdf ]]; then
                python2.7 $SRC/src/PDF2PDFharness/overall.py $h $OUT_DIR $OUT_DIR/pdf_gen/ $foxit_loc $AFLpp_loc
	fi
done

# checking how many HTML PROCESSED
cnt=`ls $OUT_DIR | grep -v "harness_bin" | grep -v "pdf_gen" | grep -v "tmp_obj_exchange" | wc -l`

# --------------- filtering, compiling, fuzzing, and migration --------------------
if [[ $cnt == 1 ]]
then
        # 1. compile .cpp to harness bin ~~~~~~~~~~
        top_rank=`ls $OUT_DIR/ | grep -v "harness_bin" | grep -v "pdf_gen" | grep -v "rank_list" | grep -v "tmp_obj_exchange"`
        $AFLpp_loc/afl-clang++ -g -O3 -funroll-loops -o $OUT_DIR/harness_bin/$top_rank -Wno-format -Wno-pointer-sign -I. -fpermissive -fPIC $OUT_DIR/$top_rank/html_to_PDF_harness_template.cpp $AFLpp_loc/afl-compiler-rt.o $SRC/src/harness/libfrida-gum.a -ldl -lresolv -pthread -std=c++11

        # 2. run harness mutation fuzzing ~~~~~~~~~~
        mkdir $OUT_DIR/harness$top_rank
        LD_LIBRARY_PATH=$foxit_loc/Libs/ $AFLpp_loc/afl-fuzz -m none -t 1000000+ -i $AFLpp_loc/testcases/others/pdf/ -o $OUT_DIR -- $OUT_DIR/harness_bin/$top_rank @@


elif [[ $cnt == 0  ]]
then
        echo "Please provide another Input dir. No HTML in current dir can be convert to PDF harness"

else
        while true; do
                # harness filtering 
                bash $SRC/src/harness/filter/rm_large_filter_shell.sh -c $CONFIG

                # harness compiling, fuzzing, pdf files migration 
                while [ -s $OUT_DIR/rank_list ]; do

			# 1. best harness is the first line in "rank_list" 
                        top_rank=$(head -n 1 $OUT_DIR/rank_list)
                        echo $top_rank 

                        # 2. compile the best harness to binary
                        $AFLpp_loc/afl-clang++ -g -O3 -funroll-loops -o $OUT_DIR/harness_bin/$top_rank -Wno-format -Wno-pointer-sign -I. -fpermissive -fPIC $OUT_DIR/$top_rank/html_to_PDF_harness_template.cpp $AFLpp_loc/afl-compiler-rt.o $SRC/src/harness/libfrida-gum.a -ldl -lresolv -pthread -std=c++11

                        # remove the best harness from rank_list
                        sed -i 1d $OUT_DIR/rank_list
                        # remove the best harness's .cpp file
        #               rm -rf $OUT_DIR/$top_rank/ 

                        # 3. run harness mutation fuzzing + PDF seeds migration
                        # 3.1 : run harness fuzzing
                        mkdir $OUT_DIR/harness$top_rank$DATE

                        LD_LIBRARY_PATH=$foxit_loc/Libs/ $AFLpp_loc/afl-fuzz -m none -t 1000000+ -i $AFLpp_loc/testcases/others/pdf/ -o $OUT_DIR/harness$top_rank$DATE -- $OUT_DIR/harness_bin/$top_rank @@&
                        
			runtime="$TIME minute"
                        endtime=$(date -ud "$runtime" +%s)

                        if [[ $(date -u +%s) -le $endtime ]]; then
                        	echo "in time"
                        else 
				while read line 
                        	do
                                	if [[ "$line" == *"fuzzer_pid"* ]]; then
                                	        PID=`echo $line | cut -d : -f 2`
                                	        kill $PID
                                	fi
                        	done < $OUT_DIR/harness$top_rank$DATE/default/fuzzer_stats
			fi
                        rm -rf $OUT_DIR/harness$top_rank$DATE

                done
        done
fi

