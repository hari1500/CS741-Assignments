from utils import *
from collections import defaultdict
import itertools
from tqdm import tqdm



# T = 3
# N = 16
# s = 4

# Sbox = (
#     0x0E, 0x04, 0x0D, 0x01, 
# 	0x02, 0x0F, 0x0B, 0x08, 
# 	0x03, 0x0A, 0x06, 0x0C, 
# 	0x05, 0x09, 0x00, 0x07
# )
# Perm = (
#     0, 4, 8, 12, 
# 	1, 5, 9, 13,
# 	2, 6, 10,14,
# 	3, 7, 11,15
# )

T 	 = 3
N 	 = 9
Perm = [0,3,6,1,4,7,2,5,8]
s 	 = 3
Sbox = [0,2,4,6,3,1,7,5]

# T 	 = 2
# N 	 = 4
# Perm = [0,1,2,3]
# s 	 = 2
# Sbox = [2,1,3,0]

# T = int(input())
# N = int(input())
# Perm = tuple(map(int,input().split()))

# s = int(input())

# Sbox = tuple(map(int,input().split()))
S = 2**s
input_outputs = tuple((inp << s)|Sbox[inp] for inp in range(S))

biasLists = defaultdict(list)
biasMappings = dict()

temp = defaultdict(int)

for input_mask in range(1,S):
    for output_mask in range(1,S):
        mask = (input_mask << s) | output_mask

        count = sum( (XOR_sum(mask & in_out) == 0) for in_out in input_outputs)
        bias = abs(count/S - 1/2)
        biasMappings[mask] = bias
        biasLists[bias].append(mask)

        temp[bias] += 1

# print([bin(b) for b in biasLists[0.5]])
# print(temp)



maxBiasSets = biasLists[max(biasLists)]
sortedBiasesOnInput = dict()

for inp in range(1,S):
    l = []
    for ou in range(1,S):
        b = biasMappings[(inp<<s)| ou]
        if b > 0:
            l.append((b, ou))
    sortedBiasesOnInput[inp] = sorted(l,reverse=True , key=lambda x:x[0])

bestBias = 0
vals = defaultdict(list)
cache = {}

def backtrack(round_in , roundno, p):
    if (round_in , roundno) in cache:
        return cache[(round_in,roundno)]
    if(roundno == T):
        return (1/2 , "")

    sects = [(round_in >> (N-s-sect*s))&(S-1) for sect in range(N//s)]
    outs = [sortedBiasesOnInput[sect_in] if sect_in else [(0.5,0 )] for sect_in in sects]
    # outs = [sortedBiasesOnInput[sect_in] if sect_in else [None]*(S-1) for sect_in in sects]
    # print(outs, list(enumerate(itertools.product(*outs))))
    maxBias = 0
    path_ret = ""
    # for sect , b_out in enumerate(zip(*outs)):
    for b_out in itertools.product(*outs):
        biasmult = 1/2
        temp = 0
        for j in range(N//s):
            if(b_out[j][1] == 0): continue
            # if(b_out[j] == None): continue
            b, s_out = b_out[j]
            for i in range(s):
                if(s_out & (1<<i)):
                    temp |= (1<<(N-1-Perm[s-1-i+j*s]))
            biasmult *= 2*b

        if 2*biasmult*p < bestBias:
            continue
        
        btBias , path = backtrack(temp, roundno+1, 2*biasmult*p)
        
        biasmult *= 2*btBias

        if abs(biasmult) > maxBias:
            maxBias , path_ret = abs(biasmult) , str(temp)+" "+path

    cache[(round_in,roundno)] = (maxBias , path_ret)
    return (maxBias , path_ret)



PATH = ""
PATHS = []
vals = []

for inp in tqdm(range(1,2**N)):
    bias  , path = backtrack(inp,0, 0.5)
    # print(inp , bias , path)
    vals.append((bias,str(inp)+" "+path))
    if abs(bias) > bestBias:
        bestBias = abs(bias)
        PATH = str(inp)+" "+path
        # print(bestBias, PATH)

vals.sort(reverse=True)


def printPATH(path):
    inps = list(map(int,path.strip().split()))
    curr_in = inps[0]
    for i in range(N):
        if curr_in & (1<<(N-1-i)):
            print("P{}".format(i) , end=" ")
    for r in range(T):
        for i in range(N):
            if curr_in & (1<<(N-1-i)):
                print("K{}{}".format(r,i) , end=" ")
        curr_in = inps[r+1]
    for i in range(N):
        if curr_in & (1<<(N-1-i)):
            print("C{}".format(i) , end=" ")
        

for x,v in vals[:5]:
    print("Bias =" , x, " PATH = ",end=" ")   
    printPATH(v)
    print("")
     
        
    
    
     








