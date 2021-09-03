import sys
import random 

def bool_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        for line in fr :
            
        # type of objects : booleans  
            if "0 obj" in line :
                obj_bool = 1
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif obj_bool == 1 :
                # BOOLEAN :
                if 'true' in line or 'false' in line :
                   # -------------------- in type --------------------------------
                   pool = list(set(class_obj['Boolean']).difference(set(line)))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = pool[nw_idx]
                   [fw_in.write(nw_ln + '\n')]
                   # --------------------- cross type ---------------------------
                   pool_cross = class_obj.keys()
                   pool_cross.remove('Boolean')
		   nw_idx_cross = random.choice(pool_cross)
                   nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                   if type(nw_ln_cross) == str :
                       [fw_cross.write(nw_ln_cross + '\n')]
                   elif type(nw_ln_cross) == list :
                       for i in nw_ln_cross :
                           [fw_cross.write(i + '\n')]
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]

def string_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans / ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif obj_bool == 1 :
                # STRING :
                if '<' in line and '>' in line :
                   pool = list(set(class_obj['String']).difference(set(line[line.index('<'):line.index('>')+1])))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = line[0:line.index('<')] + pool[nw_idx] + line[(line.index('>') + 1) : ]
                   [fw_in.write(nw_ln + '\n')]
                   # --------------------- cross type ---------------------------
                   pool_cross = class_obj.keys()
                   pool_cross.remove('String')
		   nw_idx_cross = random.choice(pool_cross)
                   nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                   if type(nw_ln_cross) == str :
                       [fw_cross.write(nw_ln_cross + '\n')]
                   elif type(nw_ln_cross) == list :
                       for i in nw_ln_cross :
                           [fw_cross.write(i + '\n')]
                                                  
                   
                if '(' in line and ')' in line :
                   pool = list(set(class_obj['String']).difference(set(line[line.index('('):line.index(')')+1])))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = line[0:line.index('(')] + pool[nw_idx] + line[(line.index(')') + 1) : ]
                   [fw_in.write(nw_ln + '\n')]
                   # --------------------- cross type ---------------------------
                   pool_cross = class_obj.keys()
                   pool_cross.remove('String')
		   nw_idx_cross = random.choice(pool_cross)
                   nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                   if type(nw_ln_cross) == str :
                       [fw_cross.write(nw_ln_cross + '\n')]
                   elif type(nw_ln_cross) == list :
                       for i in nw_ln_cross :
                           [fw_cross.write(i + '\n')]
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]

def name_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif obj_bool == 1 :
                # NAME :
                if '/' in line :
                   pool = list(set(class_obj['Name']).difference(set(line)))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = pool[nw_idx]
                   [fw_in.write(nw_ln + '\n')]
                   # --------------------- cross type ---------------------------
                   pool_cross = class_obj.keys()
                   pool_cross.remove('Name')
		   nw_idx_cross = random.choice(pool_cross)
                   nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                   if type(nw_ln_cross) == str :
                       [fw_cross.write(nw_ln_cross + '\n')]
                   elif type(nw_ln_cross) == list :
                       for i in nw_ln_cross :
                           [fw_cross.write(i + '\n')]
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]


def array_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif obj_bool == 1 :
                # ARRAY :
                if '[' in line and ']' in line :
                   pool = list(set(class_obj['Array']).difference(set(line[line.index('['):line.index(']')+1])))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = line[0:line.index('[')] + pool[nw_idx] + line[(line.index(']') + 1) : ]
                   [fw_in.write(nw_ln + '\n')]
                   # --------------------- cross type ---------------------------
                   pool_cross = class_obj.keys()
                   pool_cross.remove('Array')
		   nw_idx_cross = random.choice(pool_cross)
                   nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                   if type(nw_ln_cross) == str :
                       [fw_cross.write(nw_ln_cross + '\n')]
                   elif type(nw_ln_cross) == list :
                       for i in nw_ln_cross :
                           [fw_cross.write(i + '\n')]
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]


def number_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        dic_bool = 0
  
        stream_bool = 0

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
            elif obj_bool == 1 :
                # NUMBER :
                nw_ln = line.strip("\n")
                num_bool = 0 
                for i in line.strip("\n").split(" ") :
                    try :
                        float(i)
                        if "R" not in line :
                            # indicating that this is a numeric type
                            num_bool = 1
                            pool = list(set(class_obj['Number']).difference(set(i)))
                            nw_idx = random.randrange(len(pool))
                            nw = pool[nw_idx]
                            nw_ln = nw_ln.replace(i, nw)
                    except :
                        continue
                [fw_in.write(nw_ln + '\n')]
                # --------------------- cross type ---------------------------
                if num_bool == 1 :
                    pool_cross = class_obj.keys()
                    pool_cross.remove('Number')
	            nw_idx_cross = random.choice(pool_cross)
                    nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                    if type(nw_ln_cross) == str :
                        [fw_cross.write(nw_ln_cross + '\n')]
                    elif type(nw_ln_cross) == list :
                        for i in nw_ln_cross :
                            [fw_cross.write(i + '\n')]
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]




def dictionary_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :

        dic_bool = 0

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            # DICTIONARY :
            if "<<" == line.strip() :
                # ---------- in type ----------------------------------
                dic_bool = 1
                pool = class_obj['Dictionary']
                nw_idx = random.randrange(len(pool))
                nw = pool[nw_idx]
                for nw_ln in nw :
                    [fw_in.write(nw_ln + '\n')]
                # ---------- cross type -------------------------------
                pool_cross = class_obj.keys()
                pool_cross.remove('Dictionary')
	        nw_idx_cross = random.choice(pool_cross)
                nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                if type(nw_ln_cross) == str :
                    [fw_cross.write(nw_ln_cross + '\n')]
                elif type(nw_ln_cross) == list :
                    for i in nw_ln_cross :
                        [fw_cross.write(i + '\n')]
            elif ">>" == line.strip() :
                dic_bool = 0
            elif dic_bool == 1 :
                continue
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]
  

def stream_output_to_file(target_path, output_path_in_type, output_path_cross_type, class_obj) :

    fw_in = open (output_path_in_type, 'w')
    fw_cross = open (output_path_cross_type, 'w')

    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        dic_bool = 0
  
        stream_bool = 0

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            # STREAM
            if line.strip() == "stream" :
            #    [fw.write(line + '\n')]
                stream_bool = 1
                pool = class_obj['Stream']
                nw_idx = random.randrange(len(pool))
                nw = pool[nw_idx]
                for nw_ln in nw :
                    [fw_in.write(nw_ln + '\n')]
                # ---------- cross type -------------------------------
                pool_cross = class_obj.keys()
                pool_cross.remove('Stream')
	        nw_idx_cross = random.choice(pool_cross)
                nw_ln_cross = random.choice(class_obj[nw_idx_cross])
                if type(nw_ln_cross) == str :
                    [fw_cross.write(nw_ln_cross + '\n')]
                elif type(nw_ln_cross) == list :
                    for i in nw_ln_cross :
                        [fw_cross.write(i + '\n')]
            elif line.strip() == "endstream" :
                stream_bool = 0 
            #    [fw.write(line + '\n')]
            elif stream_bool == 1 :
                continue
            else :
                [fw_in.write(line + '\n')]
                [fw_cross.write(line + '\n')]



def obj_classify (all_OBJ) :
    
    class_obj = dict()

    with open (all_OBJ) as fr :
        obj_bool = 0
        dic_bool = 0
        stream_bool = 0
        dic_ls = list()
        stream_ls = list()
        for line in fr :
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
            elif "endobj" in line :
                obj_bool = 0
            elif obj_bool == 1 :
                # BOOLEAN :
                if 'true' in line or 'false' in line :
                    if 'Bool' not in class_obj :
                        class_obj.update({'Bool' : [line]})
                    else :
                        class_obj['Bool'].append(line)
                # STRING :
                if '<' in line and '>' in line :
                    if 'String' not in class_obj :
                        class_obj.update({'String' : [line[line.index('<'):line.index('>')+1]]})
                    else :
                        class_obj['String'].append(line[line.index('<'):line.index('>')+1])
                if '(' in line and ')' in line :
                    if 'String' not in class_obj :
                        class_obj.update({'String' : [line[line.index('('):line.index(')')+1]]})
                    else :
                        class_obj['String'].append(line[line.index('('):line.index(')')+1])
                # NAME :
                if '/' in line :
                    if 'Name' not in class_obj :
                        class_obj.update({'Name' : [line]})
                    else :
                        class_obj['Name'].append(line)
                # ARRAY :
                if '[' in line and ']' in line :
                    if 'Array' not in class_obj :
                        class_obj.update({'Array' : [line[line.index('['):line.index(']')+1]]})
                    else :
                        class_obj['Array'].append(line[line.index('['):line.index(']')+1])
                # NULL :
                if 'null' in line :
                    if 'Null' not in class_obj :
                        class_obj.update({'Null' : [line]})
                    else :
                        class_obj['Null'].append(line)
                # NUMBER :
                for i in line.strip("\n").split(" ") :
                    try :
                        float(i)
                        if "R" not in line :
                            if 'Number' not in class_obj :
                                class_obj.update({'Number' : [i]})
                            else :
                                class_obj['Number'].append(i)
                    except :
                        continue
            # DICTIONARY :
            if "<<" == line.strip() :
                dic_ls.append([line])
                dic_bool = 1
            elif ">>" == line.strip() :
                dic_bool = 0
                dic_ls[-1].append(line)
            elif dic_bool == 1 :
                dic_ls[-1].append(line)
            class_obj['Dictionary'] = dic_ls
            
            # STREAM
            if line.strip() == "stream" :
                stream_bool = 1
                stream_ls.append([line]) 
            elif line.strip() == "endstream" :
                stream_bool = 0 
                stream_ls[-1].append(line)
            elif stream_bool == 1 :
                stream_ls[-1].append(line)
            class_obj['Stream'] = stream_ls
    #print (class_obj['Stream'])
    return class_obj    

  
def main (argv) :
    # global objects collected from shell
    all_OBJ = argv[0]
    # target pdf file path 
    target_path = argv[1]
    # where to output the files 
    output_path =argv[2]
  
    # all overall objs classify in 8 types
    class_obj = obj_classify(all_OBJ)
    
    # parsing target pdf file 
   # target_parse_rs = target_parse(target_path, output_path, class_obj)

    # write to file :
    # output Boolean object exchanged 
    if 'Boolean' in class_obj :
        bool_output_to_file(target_path, output_path+'bool_in', output_path+'bool_cross', class_obj)
    # output String object exchanged 
    if 'String' in class_obj :
        string_output_to_file(target_path, output_path+'string_in', output_path+'string_cross',class_obj)
    # output Array object exchanged 
    if 'Array' in class_obj :
        array_output_to_file(target_path, output_path+'array_in', output_path+'array_cross', class_obj)
    # output Number object exchanged 
    if 'Number' in class_obj :
        number_output_to_file(target_path, output_path+'number_in', output_path+'number_cross', class_obj)
    # output Name object exchanged 
    if 'Name' in class_obj :
        name_output_to_file(target_path, output_path+'name_in', output_path+'name_cross', class_obj)
    # output Dictionary object exchanged 
    if 'Dictionary' in class_obj :
        dictionary_output_to_file(target_path, output_path+'dictionary_in',output_path+'dictionary_cross',  class_obj)
    # output Stream object exchanged 
    if 'Stream' in class_obj :
        stream_output_to_file(target_path, output_path+'stream_in',output_path+'stream_cross',  class_obj)
   # if 'Null' in class_obj :
   #     null_output_to_file(target_path, output_path+'null', class_obj)
        

 #   # exchanging each obj in pdf file with same type obj 
 #   final_rs = exchange_obj(target_parse_rs, class_obj)


if __name__ == "__main__" :
    main(sys.argv[1:])
