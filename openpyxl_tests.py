# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 20:25:28 2021

@author: luanp
"""
import math
import random

PATH = "C:/Users/luanp/OneDrive/PYTHON/"
KAFKA_PATH = PATH + "schloss_kafka.txt"

with open(KAFKA_PATH, "r+", encoding="utf-8") as file:
    schloss_str = file.read()


TERM_LEN = 5
ks = schloss_str.replace("\n", "")
ks = schloss_str.split(",")
ks = [el for el in ks if len(el.split()) == 5 and len(el) <= 35 and len(el) < 45] #Trying to limit lenght of sentence
ks_rhymes = sorted(ks, key = lambda x: x[-TERM_LEN:])

rhymes = []
temp = []

for i, el in enumerate(ks_rhymes):
    if i+1 < len(ks_rhymes):
        if ks_rhymes[i+1][-TERM_LEN:] == el[-TERM_LEN:]:
            if el not in temp:
                temp.append(el)
            temp.append(ks_rhymes[i+1])
        else:
            rhymes.append(temp)
            temp = []

rhymes = sorted(rhymes, key = lambda x: len(x), reverse=True)
res = ""
for n in range(2,15):
    for i in range(1, 5):
        res += rhymes[n + (-1)**i][i] + "\n"
    res += "\n\n"

with open(PATH+"teste.txt", "w+", encoding="utf-8") as file:
    file.write(res)
    
def toss(n, k):
    f = math.factorial
    return (f(n)/(f(k)*f(n-k)))*2**(-n)

# print(toss(10,2))

def geom_reih(q, n=1000):
    r_sum = 0
    for i in range(0, n):
        r_sum += q**i
    return r_sum, 1/(1-q)


def bose_einstein():
    N = [[],[],[],[],[]]
    n = 3

    pos_res = 0
    for i in range(100000):
        while n > 0:
            spot = random.randint(0, len(N)-1)
            N[spot].append(1)
            n -= 1
        if len([el for el in N if len(el) != 0]) == 3:
            pos_res += 1
        N = [[],[],[],[],[]]
        n = 3
    
    print(pos_res)
    

# import openpyxl
# import itertools

# FILE_PATH = "C:/Users/luanp/OneDrive/PYTHON/Deutsch_DB/"

# # load excel with its path
# wrkbk = openpyxl.load_workbook(FILE_PATH + "Book1_1.xlsx")
  
# sh = wrkbk.active
  
# test_list = []

# # iterate through excel and display data
# for row in sh.iter_rows(min_row=2, min_col=1, max_row=3, max_col=4):
#     test_list.append([cell.value for cell in row])

# #print(test_list)

# for i in [el[1] for el in test_list]:
#     print(i)

# import pandas as pd

# df = pd.read_excel(FILE_PATH + "Book1_1.xlsx")
# x = [el.split(",") for el in df["GRAMMAR KEYWORDS"].unique()]
# x = list(itertools.chain.from_iterable(x))
# x = [el.strip() for el in x]
# print(x)
