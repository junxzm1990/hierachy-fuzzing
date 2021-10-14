import sys
sys.path.append("usr/local/lib/python2.7/dist-packages/numpy")
import random
import string
import numpy as np
from numpy.random import seed
from numpy.random import rand
import grab_diff_objs as parser
import dict_classifier_disturbance as classifier

def flatten(t):
    return [item for sublist in t for item in sublist]

def prep_matrix (content) :
    for i in content :
        if i == "[" or i == "]" :
            content.remove(i)
    return content
  #  mtx = list()
  #  left = list()
  #  layer_ct_index = list()
  #  nested = False
  #  sp_mtx = list()
  #  is_nested = False
  #  for i in range(0,len(content)) :
  #      if content[i] == "[" :
  #          left.append(i)
  #      elif content[i] == "]" :
  #          pair = (left[-1], i)
  #          layer_ct_index.append(pair)
  #          left.pop(-1)
  #      else :
  #          mtx.append(content[i])
  #  # check if matrix is nested
  #  for t in range(0,len(layer_ct_index)-1) :
  #      if layer_ct_index[t][1] < layer_ct_index[t+1][0] :
  #          continue
  #      else :
  #          is_nested = True
  #  if mtx == [] :
  #      return mtx
  #  else :
  #      for v in layer_ct_index :
  #          if is_nested == True : 
  #              if v[0] != 0 :
  #                  nest_ls = mtx[v[0]-1:v[1]+1]
  #                  del mtx[v[0] - 1 : v[1] + 1]
  #                  if v[0]-1 == len(mtx) :
  #                      mtx.append(nest_ls)
  #                  else :
  #                      mtx[v[0]-1] = nest_ls
  #          else :
  #              nest_ls = mtx[v[0]:v[1]+1]
  #              sp_mtx.append(nest_ls)
  #      num = random.getrandbits(4)
  #      idx = random.randint(0, len(mtx))
  #      sp_idx = random.randint(0, len(sp_mtx))
  #      if is_nested == True :
  #          for i in range(0, num) :
  #              if idx != 0 :
  #                  mtx[idx-1] = rd_in_digit_and_str_mutation(mtx[idx-1], [])
  #              else :
  #                  mtx[idx] = rd_in_digit_and_str_mutation(mtx[idx], [])
  #          return mtx
  #      else :
  #          for i in range(0, num) :
  #              if len(sp_mtx) != 0 : 
  #                  sp_mtx[sp_idx-1] = rd_in_digit_and_str_mutation(mtx[idx-1], [])
  #              else :
  #                  sp_mtx[sp_idx] = rd_in_digit_and_str_mutation("0", [])
  #          return sp_mtx
        
# reference mutation --------------------- 
def rd_in_obj_mutation (content, raw_pool) :
    pool = list()
    for i in raw_pool :
        pool += filter(lambda x: x != "0" and x != "R" and x != "[" and x != "]", i)
    target = [content[0]]
    possible_pool = set(pool).difference(set(target))
    new_content = [random.choice(tuple(possible_pool)) + "0 R"]
    return new_content

# matrix mutation -------------------------
def rd_in_mtrx_mutation (content, raw_pool) :
    # prepare target file's matrix
    target_mtx = prep_matrix(content)
    # prepare raw_pool's matrix
    raw_pool_mtx = list()
    for i in raw_pool :
        #print("i", i)
        one_mtx = prep_matrix(i)
        raw_pool_mtx.append(one_mtx)
    arr = []
    for m in target_mtx :
        target = np.array(m)
        # mutation 1 : tiling
        num = random.getrandbits(12)
        t_target = np.tile(np.asarray(target),num)
        arr = np.concatenate((arr,t_target))
    # mutation 2 : multi-dimension
    num = random.getrandbits(8)
    d_target = np.expand_dims(arr,axis=num)
    # mutation 3 : rotation
    num = random.getrandbits(4)
    r_target = [] 
    for r in range(0, num) :
        r_target = np.rot90(d_target)
    # mutation 4 : flip
    f_target = np.flipud(r_target)
    f_rs = list(f_target)
    return f_rs

# indivisual element mutation ------------------
def rd_in_digit_and_str_mutation (content, raw_pool) :
    num = random.randint(0, 1)
    max_flip_reci_reset = random.randint(0, 3)
    bits = random.randint(1, 64)
    lc = string.ascii_lowercase
    uc = string.ascii_uppercase
    lt = string.ascii_letters
    dg = string.digits
#    pc = string.punctuation
    if num :
        if max_flip_reci_reset == 0 :
            content = 65535 
        elif max_flip_reci_reset == 1 :
            # seed random number generator
            seed(1)
            # generate some random numbers
            content = rand(1)
            content = 0 - content 
        elif max_flip_reci_reset == 2 :
            # seed random number generator
            seed(1)
            # generate some random numbers
            content = rand(1)
            content = float(1) / float(content)
        elif max_flip_reci_reset == 3 : 
            content = 0   
    else :
        content = ''.join(random.choice(lc + uc + lt + dg ) for i in range (bits))
    return content


# stream mutation -------------------------------------
def stream_mutation (stream_all) :
    stream_rs = list()
    seg_num = random.randint(0,len(stream_all)-1)
    exe_times = random.getrandbits(4)
    new_stream = str()
    for num in range(0,exe_times) :  
        for i in stream_all :
            # 4 type of mutation : duplicating, flipping, merging,reset, max
            stratgy_num = random.randint(0, 4)
            if stratgy_num == 0 :
                new_stream = i * exe_times
            elif stratgy_num == 1 : 
                new_stream = i[::-1] 
            elif stratgy_num == 2 :
                new_stream = i + stream_all[seg_num]
            elif stratgy_num == 3 :
                new_stream = 0 
            elif stratgy_num == 4 :
                new_stream = 65535 
            stream_rs.append(new_stream)
    return stream_rs

# entry mutation ------------------------------------
def entry_mutation (obj_num_entries) :
    for i in obj_num_entries : 
        i_or_g = random.randint(0, 1) # 0 : individual; 1 : group
        # Individual Mutation
        if i_or_g == 0 :
            # mutation type 
            m_type = random.randint(0, 3)
            # index of original entry
            e_idx = random.randint(0, len(obj_num_entries[i])-1)
            # key of obj random pick from all objs
            obj_key = random.choice(obj_num_entries.keys())
            # index of target entry for mutation
            te_idx = int()
            if len(obj_num_entries[obj_key]) > 1 :
                te_idx = random.randint(0, len(obj_num_entries[obj_key])-1)
            else :
                te_idx = 0
            # individual_entry mutation 1 : exchange with other obj's entries
            if m_type == 0 :
                if len(obj_num_entries[obj_key]) < 1 :
                    continue
                else :
                    obj_num_entries[i][e_idx] == obj_num_entries[obj_key][te_idx]
            # individual_entry mutation 2 : insert not existance in current obj
            elif m_type == 1 :
                if len(obj_num_entries[obj_key]) < 1 :
                    continue
                else :
                    obj_num_entries[i].append(obj_num_entries[obj_key][te_idx])
            # individual_entry mutation 3 : delete existing obj's entries
            elif m_type == 2 : 
                obj_num_entries[i].pop(e_idx)
            # individual_entry mutation 4 : dupliating existing obj entries
            elif m_type == 3 :
                insert_times = random.getrandbits(2)
                duplica = obj_num_entries[i][e_idx]
                for t in range(0, insert_times) :
                    obj_num_entries[i].insert(e_idx, duplica)
        # Group Mutation 
        elif i_or_g == 1 : 
            g_type = random.randint(0, 4)
            obj_key = random.choice(obj_num_entries.keys())
            s_idx = random.randint(0, len(obj_num_entries[i])-2)
            e_idx = random.randint(s_idx + 1, len(obj_num_entries[i])-1 )
            target_trunk = list()
            if len(obj_num_entries[obj_key]) > 3 :
                ts_idx = random.randint(0, len(obj_num_entries[obj_key]) - 1 )
                te_idx = random.randint(ts_idx, len(obj_num_entries[obj_key])-1)
                target_trunk = obj_num_entries[obj_key][ts_idx : te_idx]
            else : 
                target_trunk = obj_num_entries[obj_key][0:-1]
            # group_entry mutation 1 : reverse
            if g_type == 0 :
                reversed_target = list(reversed(obj_num_entries[obj_key][s_idx : e_idx]))
                obj_num_entries[i][s_idx : e_idx] = reversed_target
            # group_entry mutation 2 : exchange with other group of obj entries
            elif g_type == 1 :
                cnt = 0
                for e in range(s_idx, e_idx) :
                    obj_num_entries[i][s_idx : e_idx] = target_trunk
                    cnt += 1
            # group_entry mutation 3 : insert none  exist group of entries in current objects
            elif g_type == 2 : 
                obj_num_entries[i].append(target_trunk)
            # group_entry mutation 4 : delete exsiting obj's entries
            elif g_type == 3 :
                del obj_num_entries[i][s_idx : e_idx] 
            # group_entry mutation 5 : duplicating existing obj entries
            elif g_type == 4 : 
                insert_times = random.getrandbits(4)
                for t in range(0, insert_times) :
                    for e in obj_num_entries[i][s_idx : e_idx] :
                        obj_num_entries[i].insert(s_idx, e)
    return obj_num_entries

   
def output_to_file(target_path, output_path, op_rs) :
    fw = open (output_path, 'w')
    with open (target_path, 'r') as fr :
        stream_bool = False
        obj_bool = False
        for line in fr:
            if  len(op_rs.keys()) > 0 :
                # stream output
                if "stream" in op_rs :
                    idx = int()
                    if len(op_rs["stream"]) <= 1 :
                        idx = 0
                    else : 
                        idx = random.randint(0, len(op_rs["stream"])-1) 
                    if "stream" in line and "end" not in line : 
                        [fw.write("stream \n")]
                        stream_bool = True
                    elif "endstream" in line :
                        [fw.write("endstream \n")]
                        stream_bool = False
                    elif stream_bool == True :
                        if len(op_rs["stream"]) < 1 :
                            output = ""
                        else :
                            output = "" + str(op_rs["stream"][idx])
                        [fw.write(output + " \n")]
                    else :
                        [fw.write(line)]
                # obj rules output
                elif "0 obj" in op_rs.keys()[0] :
                    if "0 obj" in line.strip() :
                        obj_bool = True
                        obj_num = line.strip().split(' ')[0]
                        [fw.write(line)]
                        [fw.write("<< \n")]
                    elif "endobj" in line.strip() :
                        obj_bool = False
                        [fw.write(line)]
                        [fw.write(">> \n")]
                    elif obj_bool == True :
                        if "0 obj" in op_rs.keys()[0] : 
                            for i in op_rs :
                                rs_num = i[0]
                                if obj_num == rs_num :
                                    for j in op_rs[i] :
                                        if type(j) == str:
                                            [fw.write(j + "\n")]
                                        elif type(j) == list :
                                            for f_j in j:
                                                [fw.write(f_j + "\n")]
                                        
                    else :
                        [fw.write(line)]
                # type based mutation output                
                else :
                    tag = line.strip().split(' ')[0]
                    if tag in op_rs.keys() :
                        idx = random.randint(0, len(op_rs[tag])) 
                        if idx == 0 : 
                            [fw.write(tag + ' ' + str(op_rs[tag][idx]) + "\n")]
                        else :
                            [fw.write(tag + ' ' + str(op_rs[tag][idx-1]) + "\n")]
                    else :
                        [fw.write(line)]
                
    fw.close()


            
def mutation_main (obj_num_entries, class_token_dict) :
    ref_op_rs = dict()
    mtrx_op_rs = dict()
    numstr_op_rs = dict()
    for i in obj_num_entries :
        tag = str()
        content = list()
        for j in obj_num_entries[i] :
            if j[0] == "/" :
                tag = j.strip().split(' ')[0]
                content = j.strip().split(' ')[1:]
            else :
                if "<<" not in j and ">>" not in j :
                    content += j.strip().split(' ')
            if len(obj_num_entries[i]) - 1 >  obj_num_entries[i].index(j) : 
                if obj_num_entries[i][obj_num_entries[i].index(j)+1][0] == "/" :
                    for cls,tkn in class_token_dict.items() :
                        if tag in tkn.keys() :
                            if cls == 'rd_in_obj_token' :
                                new_content = rd_in_obj_mutation(content, class_token_dict[cls].values())
                                if tag in ref_op_rs :
                                    ref_op_rs[tag].append(new_content)         
                                else :
                                    ref_op_rs[tag] = [new_content] 
                                #  output new_content of matrix 
                            elif cls == 'rd_in_mtrx_token' :
                                if "[" in content or "]" in content :
                                    new_content = rd_in_mtrx_mutation(content, class_token_dict[cls].values())
                                    # print (tag, content)
                                    if tag in mtrx_op_rs :
                                        mtrx_op_rs[tag].append(new_content) 
                                    else :
                                        mtrx_op_rs[tag] = [new_content] 
                                    # output new_content string and number
                            if cls == 'rd_in_digit_token' or cls == 'rd_in_str_token' :
                                new_content = rd_in_digit_and_str_mutation(content, class_token_dict[cls].values())   
                                if tag in numstr_op_rs :
                                    numstr_op_rs[tag].append(new_content)         
                                else :
                                    numstr_op_rs[tag] = [new_content] 
                             
                    tag = str()
                    content = str()
    return [ref_op_rs, mtrx_op_rs,numstr_op_rs]

def one_file_parse (target_path) :
    obj_num_entries = dict()
    obj_num = str()
    stream_all = list()
    # parse object entries
    with open (target_path) as fr :
        objs = False
        streams = False
        for line in fr :
            if " 0 obj" in line.strip() :
                objs = True
                obj_num = line.strip()
                continue
            elif "endobj" in line.strip() :
                objs = False
                continue
            elif objs == True : # and line.strip() != "<<" and line.strip() != ">>" :
                if "stream" in line.strip() and "end" not in line.strip():
                    streams = True
                elif "endstream" in line.strip() :
                    streams = False
                elif streams == False :
                    if obj_num in obj_num_entries :
                        obj_num_entries[obj_num].append(line.strip())
                    else :
                        obj_num_entries[obj_num] = list(line.strip())
                elif streams == True :
                    stream_all.append(line.strip())
    # TODO : parse stream
    return [obj_num_entries, stream_all]

def main (argv) : 
    # Overall diff doc path 
    overall_diff_path = argv[0]
    # target one seed pdf file path
    target_path = argv[1]
    # where the mutated file outputs
    output_path = argv[2]
    # parsing overall entries 
    overall_entries = parser.main(overall_diff_path)
    overall_objs = overall_entries[0]
    overall_streams = overall_entries[1]
    # get entries classified 
    class_token_dict = classifier.token_classifer(overall_objs)

    # parsing target one seed pdf file
    parsing_rs =  one_file_parse(target_path)
    # result of parsing object number and their entries
    obj_num_entries = parsing_rs[0]
    # parsing target's stream 
    stream_all = parsing_rs[1]
    # mutation on each obj's entries
    op_rs = mutation_main(obj_num_entries, class_token_dict)
    # mutation on each stream piece
    stream_rs = stream_mutation(stream_all)
    # mutation on obj entries(one entry as an mutation unit)
    ety_rs = entry_mutation(obj_num_entries)
    # stream result join into op_rs
    op_rs.append({"stream" : stream_rs})
    # obj entry result join into op_rs
    op_rs.append(ety_rs) 

    # wirte to file :
    # output ref mutation
    output_to_file(target_path, output_path+"ref", op_rs[0]) 
    # output mtrx mutation
    output_to_file(target_path, output_path+"mtrx", op_rs[1]) 
    # output numstr mutation
    output_to_file(target_path, output_path+"numstr", op_rs[2])
    # output stream mutation
    output_to_file(target_path, output_path+"stream", op_rs[3])
    # output obj entry mutation
    output_to_file(target_path, output_path+"entry", op_rs[4])

if __name__ == "__main__" :
    main(sys.argv[1:])
