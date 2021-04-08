# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:22:22 2021

@author: luanp
"""

import pandas as pd


def compare(a,b):   #TODO: renomear função
    a_ = set(a)
    b_ = set(b)
    return len(a_ & b_) != 0

def check_match(df, search_terms, attr):
    """
    Adds column of boolean to DF with matches for each attribute.
    """
    df_ = df.copy()
    df_.loc[df_[attr].apply(lambda x: compare(x, search_terms[attr])), attr+"_match"]=True
    df_.loc[~df_[attr].apply(lambda x: compare(x, search_terms[attr])), attr+"_match"]=False
    return df_


data = {1:[[1,3], 2,3, 4], 2:[[0,0], 9, 4, 6]}
cols = ["Teste", "Meste", "Leste", "Keste"]
df = pd.DataFrame.from_dict(data, orient="index", columns=cols)

search_terms_ = {"Teste":[2,3]}
df_search_ = check_match(df, search_terms_, "Teste")

print(df_search_.query("Teste_match==True").loc[:,df.columns])