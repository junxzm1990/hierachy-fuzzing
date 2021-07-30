import sys

class MyList(list):
    def __init__(self, *args):
        super(MyList, self).__init__(args)

    def __sub__(self, other):
        return self.__class__(*[item for item in self if item not in other])


def find_sub_idx(test_list, repl_list, start = 0):
    length = len(repl_list)
    for idx in range(start, len(test_list)):
        if test_list[idx : idx + length] == repl_list:
            return idx, idx + length
  
# helper function to perform final task
def replace_sub(test_list, repl_list, new_list):
    length = len(new_list)
    idx = 0
    for start, end in iter(lambda: find_sub_idx(test_list, repl_list, idx), None):
        test_list[start : end] = new_list
        idx = start + length


#def ranking_time(diff_arg_num, api_arg_rank, harness_time) : 
#    target_harness_time = dict()
#    time_final_result = list()
#    for harness in api_arg_rank : 
#        if api_arg_rank[harness] in diff_arg_num :
#            if api_arg_rank[harness] not in target_harness_time :
#                target_harness_time[api_arg_rank[harness]] = {harness:harness_time[harness]}
#            else :
#                target_harness_time[api_arg_rank[harness]].update({harness:harness_time[harness]})
#    final_result = sorted(api_arg_rank, key=api_arg_rank.get, reverse=True)
#    for num in target_harness_time.values() :
#        replace_trunk = list()
#        for harness in num.keys() : 
#            replace_trunk.append(final_result.index(harness))
#        final_result[min(replace_trunk):max(replace_trunk)+1] = sorted(num, key=num.get)
#    return final_result 
        
        
         

def ranking_arg(harness_api, good_harness, arg_dic, harness_time):
    api_arg_rank = dict()
    for harness in good_harness :
        api_arg_rank[harness] = 0  
        for arg in harness_api[harness] :
            api_arg_rank[harness] += arg_dic[arg]
    final_result = sorted(api_arg_rank, key=api_arg_rank.get, reverse=True)
   # if len(api_arg_rank.values()) != len(set(api_arg_rank.values())) :
   #     ori_list = MyList(api_arg_rank.values())
   #     set_list = MyList(list(set(api_arg_rank.values())))
   #     [diff_arg_num] = set_list - ori_list
   #     return ranking_time(diff_arg_num, api_arg_rank, harness_time)
    return final_result

def ranking_harness(harness_api, api_lst, arg_dic, harness_time) :
    harness_rank = list()
    arg_rank = list()
    while len(api_lst) != 0 : 
        max_len = max(len(v.intersection(api_lst)) for v in harness_api.values())
        good_harness = [k for k,v in harness_api.items() if len(v.intersection(api_lst)) == max_len]
        if len(good_harness) == 1 :
            harness_rank.append(good_harness[0])
            api_lst = api_lst.difference(harness_api[good_harness[0]])
        else :
           # arg_dic_fltd = {k : arg_dic[k] for k in good_harness } 
            arg_rank = ranking_arg(harness_api, good_harness, arg_dic, harness_time)
            harness_rank.extend(arg_rank)
            for i in good_harness :
                api_lst = api_lst.difference(harness_api[i])
    return harness_rank

def rank_output (harness_rank, output_path) :
    with open (output_path, "w") as fw :
        [fw.write(harness + "\n") for harness in harness_rank]
             

def main (argv) :
    api_list = argv[0]
#    time_list = argv[1]
    output_path = argv[1]

    harness_time = dict()

    harness_api = dict()
    raw_lst = dict()
    index_lst = list()
    api_lst = set()
    arg_dic = dict()

#    with open(time_list) as fr :
#        for harness in fr.read().split("@@@@@") :
#            if harness.split() :
#                harness_time[harness.strip().split('/')[-2]] = float(harness.split()[2][harness.split()[2].index("m")+1:-1])

    with open(api_list) as fr :
        for (index,line) in enumerate(fr.readlines()) :
            if "FQL->" in line :
                if "(" and ";" in line :
                    api_name = line.strip()[line.strip().index("FQL->") : line.strip().index("(")]
                    arg_name = line.strip()[line.strip().index("("):line.strip().index(";")]
                    arg_num = arg_name.count(",") + 1

                    arg_dic[api_name] = arg_num

                    raw_lst[index] = api_name 
                    if api_name != "" :
                        api_lst.add(api_name)
            else :
                raw_lst[index] = line.strip()
    for i in raw_lst :
        if ".cpp" in raw_lst[i] :
            index_lst.append(i)
            harness_api[raw_lst[i].split('/')[-2]] = set()
        if "FQL->" in raw_lst[i] :
            harness_api[raw_lst[index_lst[-1]].split('/')[-2]].add(raw_lst[i])

    harness_rank = ranking_harness(harness_api, api_lst, arg_dic, harness_time)

    rank_output(harness_rank, output_path)
    

if __name__ == "__main__" :
    main(sys.argv[1:])
