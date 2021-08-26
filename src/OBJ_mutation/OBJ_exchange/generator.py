import sys
import random 


def bool_output_to_file(target_path, output_path, class_obj) :
    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw.write(line + '\n')]
            elif obj_bool == 1 :
                # BOOLEAN :
                if 'true' in line or 'false' in line :
                   pool = list(set(class_obj['Boolean']).difference(set(line)))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = pool[nw_idx]
                   [fw.write(nw_ln + '\n')]
            else :
                [fw.write(line + '\n')]

def string_output_to_file(target_path, output_path, class_obj) :
    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw.write(line + '\n')]
            elif obj_bool == 1 :
                # STRING :
                if '<' in line and '>' in line :
                   pool = list(set(class_obj['String']).difference(set(line[line.index('<'):line.index('>')+1])))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = line[0:line.index('<')] + pool[nw_idx] + line[(line.index('>') + 1) : ]
                   [fw.write(nw_ln + '\n')]
                if '(' in line and ')' in line :
                   pool = list(set(class_obj['String']).difference(set(line[line.index('('):line.index(')')+1])))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = line[0:line.index('(')] + pool[nw_idx] + line[(line.index(')') + 1) : ]
                   [fw.write(nw_ln + '\n')]
            else :
                [fw.write(line + '\n')]

def name_output_to_file(target_path, output_path, class_obj) :
    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw.write(line + '\n')]
            elif obj_bool == 1 :
                # NAME :
                if '/' in line :
                   pool = list(set(class_obj['Name']).difference(set(line)))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = pool[nw_idx]
                   [fw.write(nw_ln + '\n')]
            else :
                [fw.write(line + '\n')]


def array_output_to_file(target_path, output_path, class_obj) :
    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw.write(line + '\n')]
            elif obj_bool == 1 :
                # ARRAY :
                if '[' in line and ']' in line :
                   pool = list(set(class_obj['Array']).difference(set(line[line.index('['):line.index(']')+1])))
                   nw_idx = random.randrange(len(pool))
                   nw_ln = line[0:line.index('[')] + pool[nw_idx] + line[(line.index(']') + 1) : ]
                   [fw.write(nw_ln + '\n')]
            else :
                [fw.write(line + '\n')]


def number_output_to_file(target_path, output_path, class_obj) :
    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :
   
        obj_bool = 0 

        dic_bool = 0
  
        stream_bool = 0

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            if "0 obj" in line :
                obj_bool = 1
                [fw.write(line + '\n')]
            elif "endobj" in line :
                obj_bool = 0
                [fw.write(line + '\n')]
            elif obj_bool == 1 :
                # NUMBER :
                nw_ln = line.strip("\n")
                for i in line.strip("\n").split(" ") :
                    try :
                        float(i)
                        if "R" not in line :
                            pool = list(set(class_obj['Number']).difference(set(i)))
                            nw_idx = random.randrange(len(pool))
                            nw = pool[nw_idx]
                            nw_ln = nw_ln.replace(i, nw)
                    except :
                        continue
                [fw.write(nw_ln + '\n')]
            else :
                [fw.write(line + '\n')]




def dictionary_output_to_file(target_path, output_path, class_obj) :

    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :

        dic_bool = 0

        for line in fr :
            
        # 8 basic types of objects : booleans /ints and real nums / strings / names / arrays / dictionaries(handle in other func) / streams (handle in other func) / 
            # DICTIONARY :
            if "<<" == line.strip() :
            #    [fw.write(line + '\n')]
                dic_bool = 1
                pool = class_obj['Dictionary']
                nw_idx = random.randrange(len(pool))
                nw = pool[nw_idx]
                for nw_ln in nw :
                    [fw.write(nw_ln + '\n')]
            elif ">>" == line.strip() :
                dic_bool = 0
            #    [fw.write(line + '\n')]
            elif dic_bool == 1 :
                continue
            else :
                [fw.write(line + '\n')]
  

def stream_output_to_file(target_path, output_path, class_obj) :

    fw = open (output_path, 'w')
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
                    [fw.write(nw_ln + '\n')]
            elif line.strip() == "endstream" :
                stream_bool = 0 
            #    [fw.write(line + '\n')]
            elif stream_bool == 1 :
                continue
            else :
                [fw.write(line + '\n')]



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
    # file name and individual file's objects number 
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
        bool_output_to_file(target_path, output_path+'bool', class_obj)
    # output String object exchanged 
    if 'String' in class_obj :
        string_output_to_file(target_path, output_path+'string', class_obj)
    # output Array object exchanged 
    if 'Array' in class_obj :
        array_output_to_file(target_path, output_path+'array', class_obj)
    # output Number object exchanged 
    if 'Number' in class_obj :
        number_output_to_file(target_path, output_path+'number', class_obj)
    # output Name object exchanged 
    if 'Name' in class_obj :
        name_output_to_file(target_path, output_path+'name', class_obj)
    # output Dictionary object exchanged 
    if 'Dictionary' in class_obj :
        dictionary_output_to_file(target_path, output_path+'dictionary', class_obj)
    # output Stream object exchanged 
    if 'Stream' in class_obj :
        stream_output_to_file(target_path, output_path+'stream', class_obj)
   # if 'Null' in class_obj :
   #     null_output_to_file(target_path, output_path+'null', class_obj)
        

 #   # exchanging each obj in pdf file with same type obj 
 #   final_rs = exchange_obj(target_parse_rs, class_obj)


if __name__ == "__main__" :
    main(sys.argv[1:])
