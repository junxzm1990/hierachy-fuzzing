while getopts b:t:o:p:c:m:s:g: option
do 
	case "${option}"
	in
	b) BIN=${OPTARG};;
	t) TARGET=${OPTARG};;
        o) OUTPUT=${OPTARG};;
        p) PROTO=${OPTARG};;
        c) COMMAND=${OPTARG};; 
        m) MAP_OUTPUT=${OPTARG};;
        s) PY_SCRIPT=${OPTARG};;
        g) ORG_LOC=${OPTARG};;
        esac
done

if [[ $BIN == '' ]]; then
	echo 'please provide BIN(-b)'
	exit -1
fi

if [[ $TARGET == '' ]]; then
	echo 'please provide TARGET(-t)'
	exit -1
fi

if [[ $OUTPUT == '' ]]; then
	echo 'please provide OUTPUT(-o)'
	exit -1
fi

if [[ $PROTO == '' ]]; then
	echo 'please provide PROTO(-p)'
	exit -1
fi

if [[ $COMMAND == '' ]]; then
	echo 'NOTICE : NOT PROVIDING OPTION(-c)'
fi

if [[ $MAP_OUTPUT == '' ]]; then
	echo 'please provide MAP_OUTPUT(-m)'
	exit -1
fi

if [[ $ORG_LOC == '' ]]; then
	echo 'please provide original seed location(-g)'
	exit -1
fi

mkdir $TARGET

mkdir $MAP_OUTPUT

mkdir $OUTPUT

cp $ORG_LOC $TARGET/init.pdf

# obtain the difference part between target file and prototype file for later mutation 
sdiff -w 160 $PROTO $TARGET/init.pdf > $MAP_OUTPUT/org_diff

# prepare the initial map before mutation
$BIN $COMMAND $TARGET/init.pdf > $MAP_OUTPUT/pre_map

sort $MAP_OUTPUT/pre_map | uniq > $MAP_OUTPUT/uni_pre_map

rm -rf $MAP_OUTPUT/pre_map

# mutation and generate for new seeds(3 new seeds will be outputing) 
python $PY_SCRIPT $MAP_OUTPUT/org_diff $TARGET/init.pdf $OUTPUT

#rd_cnt=0

cnt=0

mkdir $OUTPUT/buff

while true; do
    # process generated new seeds
    for i in `ls $OUTPUT/* | grep -v "buff"`; do
       
        echo $i 

        echo "now processing "$i"-------------------------------------"    
 
        # 0 : copy seed to $TARGET
        cp $i $TARGET/$(basename $i)
    
        # 1 : calculate the new generated seed map
        $BIN $COMMAND $i > $MAP_OUTPUT/raw_map
        
        sort $MAP_OUTPUT/raw_map | uniq > $MAP_OUTPUT/uni_cur_map
     
        sort -u -o $MAP_OUTPUT/uni_cur_map $MAP_OUTPUT/uni_cur_map
    
        rm -rf $MAP_OUTPUT/raw_map
    
        # 2 : compare cur seed map with previous map
        diff -y -a $MAP_OUTPUT/uni_pre_map $MAP_OUTPUT/uni_cur_map > $MAP_OUTPUT/p_c_diff

        # after compare cur and pre map, cat the cur map into pre map and sort with uniq ones
        cat $MAP_OUTPUT/uni_cur_map >> $MAP_OUTPUT/uni_pre_map

        rm -rf $MAP_OUTPUT/uni_cur_map

        sort -u -o $MAP_OUTPUT/uni_pre_map  $MAP_OUTPUT/uni_pre_map
 
        # check if they have different edges
        diff_cnt_1=`grep -o -c "   >" $MAP_OUTPUT/p_c_diff`
    
        diff_cnt_2=`grep -o -c "   |" $MAP_OUTPUT/p_c_diff`
    
        new_edge=`expr $diff_cnt_1 + $diff_cnt_2`
    
        increment_bool=`expr $new_edge \> 0`
      
        echo $increment_bool
    
        # 3 : mutate seeds triggered new edges
        if [[ $increment_bool == 1 ]]; then
    
            echo $i" triggers new edges, now Processing it  &&&&&&&&&&&&&&&"

            diff -y -a $PROTO $i > $MAP_OUTPUT/org_diff
    
            python $PY_SCRIPT $MAP_OUTPUT/org_diff $i $OUTPUT/buff/$cnt

            rm -rf $i
    
        else :
            # 3 : delete seed if it didn't trigger new edge (all seed has been coped to $TARGET dir)
            echo $i" did not trigger new edge, deleting it"
           
            rm -rf $i
        
        fi
 
        let "cnt=cnt+1"
     
        
    done

    echo "THIS IS CNT "$cnt

    if ! (( $cnt % 5 )); then
        
        for j in $OUTPUT/buff/*; do :

            mv $j $OUTPUT/$(basename $j)$i

       # let "rd_cnt=rd_cnt+1"
        done
    fi 
   
done

    

   
       
           




















