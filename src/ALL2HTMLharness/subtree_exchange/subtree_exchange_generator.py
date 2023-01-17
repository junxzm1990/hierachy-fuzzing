import os
import json
import sys
import random 
from multiprocessing import Process
from time import sleep

def findTag (code, code_len, idx) :
    tag = None
    tag_len = 0

    for i in range(idx, code_len) :
        if code[i] == ">" :
            tag = code[ (idx + 1) : i ]
            tag_len = i - (idx + 1)
            break
    return tag, tag_len

def html_to_tree (inner_html_str) : 
    tag, tag_len = findTag(inner_html_str, len(inner_html_str), 0)
    stack = [(tag,0)]
    subTrees = []
    i = tag_len + 2
    while i < len(inner_html_str) :
        if inner_html_str[i] == "<" :
            tag, tag_len = findTag(inner_html_str, len(inner_html_str), i)
            i += tag_len + 1
            if tag[0] == "/" :
                subTrees.append(inner_html_str[stack[-1][1]:i+1])
                stack.pop()
            else :
                stack.append((tag,i-tag_len-1))
        i += 1
    return subTrees

def exchange_rules (treeA, treeB) :
    A_idx_l = random.randint(0, len(treeA)-2)
    A_idx_r = random.randint(A_idx_l+1, len(treeA)-1)
    B_idx_l = random.randint(0, len(treeB)-2)
    B_idx_r = random.randint(B_idx_l+1, len(treeB)-1)
    return treeA[A_idx_l:A_idx_r], treeB[B_idx_l : B_idx_r]

def mutation_rules (swap_A, swap_B) :
    new_swap_A =  

    
def main (argv) : 
    f_in_A = argv[0] # the testcase file you want to mutate
    d_in_path = argv[1] # all testcases' directory
    d_out_path = argv[2] # output directory for newly mutated testcase
    f_in_B = d_in_path + random.choice(os.listdir(d_in_path))
    
    with open(f_in_A, 'r') as file:
            inner_html_str_A = file.read().replace('\n', '')
    with open(f_in_B, 'r') as file:
            inner_html_str_B = file.read().replace('\n', '')
    
    # Step 1 : parse two inner HTMLs as two tree structures
    subTrees_A = html_to_tree(inner_html_str_A)
    subTrees_B = html_to_tree(inner_html_str_B)
    
    # Step 2 : exchange subtrees between tree A and tree B
    swaped = exchange_rules(subTrees_A, sbuTrees_B)
    mutated = mutation_rules(swaped)

    # Step 3 : recover the mutated tree to the inner HTMLs

if __name__ == "__main__" :
    main(sys.argv[1:])
