while getopts i:o:t:s:c:p:b:m: option
do 
	case "${option}"
	in
	i) IN_DIR=${OPTARG};;
        o) OUT_DIR=${OPTARG};;
        t) DATE=${OPTARG};;
	s) PY_SCRIPT=${OPTARG};;
        c) COMMAND=${OPTARG};;
        p) PROTO=${OPTARG};;
	b) BIN=${OPTARG};;
	m) OBJ_MUT=${OPTARG};;
        esac
done

if [[ $IN_DIR == "" ]]; then
        echo "Please provide the input directory(-i)"
        exit -1
fi

if [[ $OUT_DIR == "" ]]; then
        echo "Please provide the output directory ---- the harness_queue(-o)"
        exit -1
fi

if [[ $DATE == "" ]]; then
        echo "Please provide the DATE(-t)"
        exit -1
fi

if [[ $PY_SCRIPT == "" ]]; then
        echo "Please provide the PY_SCRIPT(-s)"
        exit -1
fi

if [[ $COMMAND == "" ]]; then
        echo "Please provide the COMMAND(-c)"
        exit -1
fi

if [[ $PROTO == "" ]]; then
        echo "MIAO!Please provide the PROTO(-p)"
        exit -1
fi

if [[ $BIN == "" ]]; then
        echo "Please provide the BIN(-b)"
        exit -1
fi

if [[ $OBJ_MUT == "" ]]; then
        echo "Please provide the OBJ_MUT(-m)"
        exit -1
fi

cnt=0

mkdir $OUT_DIR/OBJ$DATE

mkdir $OUT_DIR/OBJ$DATE/queue

# this the $TARGET folder in mutation bash
mkdir $OUT_DIR/OBJ$DATE/raw_seeds

mkdir $OUT_DIR/OBJ$DATE/output

mkdir $OUT_DIR/OBJ$DATE/map_output


while true; do

	real_time_seed_cnt=`ls $IN_DIR | wc -l`
   
	increment_bool=`expr $cnt \< $real_time_seed_cnt`

	if [[ $increment_bool == 1 ]]; then

		echo "scanning start .................."
		
		for i in $IN_DIR/*
		do
			if  grep -q "$i" $OUT_DIR/OBJ$DATE/processed_seeds
			then

				echo "copied before <<<<<<<<<<  "

			else
 
				echo "NEW SEED >>>>>>>>>>>>" $i

		        	bash $OBJ_MUT -b $BIN -t $OUT_DIR/OBJ$DATE/raw_seeds -o $OUT_DIR/OBJ$DATE/output/ -p $PROTO -c $COMMAND -m $OUT_DIR/OBJ$DATE/map_output/ -s $PY_SCRIPT  -g $i

                        #        echo "KILLED IT%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
 			#	pkill $BIN

                        #       base=`echo $(basename $i) | cut -d . -f 1`
   
                        #       h_name=`echo $IN_DIR | rev | cut -d / -f 3 | rev`

			#	echo $h_name

			#	name=$base",sync:"$h_name
                        #        
 			#	cp $i $OUT_DIR/OBJ$DATE/raw_seeds/$name
				
				echo $i >> $OUT_DIR/OBJ$DATE/processed_seeds

				let "cnt=cnt+1"

        			raw_seed_cnt=`ls $OUT_DIR/OBJ$DATE/raw_seeds | wc -l`

        			inc_bool=`expr $raw_seed_cnt \> 0`


				echo "WAWAWAWAWAWAWAWAW"$raw_seed_cnt","$inc_bool

        			if [[ $inc_bool == 1 ]]; then
					
					for i in $OUT_DIR/OBJ$DATE/raw_seeds/*
					do

						already_have=`ls $OUT_DIR/OBJ$DATE/queue/|wc -l`
        			                len=${#already_have}
						bond=`expr 5 - $len`
						zero=0

						for z in $(seq $bond)
						do
							zero=$zero"0"
						done

						name="id:"$zero$already_have

						mv $i $OUT_DIR/OBJ$DATE/queue/$name
					done
				fi

			fi
		done
	fi


 
done
