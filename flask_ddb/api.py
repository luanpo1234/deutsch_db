# -*- coding: utf-8 -*-
"""
Set-ExecutionPolicy Unrestricted -Scope Process
venv/Scripts/activate.ps1
"""
import pandas as pd
import requests
from requests.exceptions import ConnectionError
import json
import re
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.sql import select
import pymysql
from fuzzywuzzy import fuzz

JSON_PATH = "flask_ddb\json.json"
KEYWORDS = ["schule", "arbeit", "haushalt", "none"]
GRAM_KEYWORDS = ["dativ", "akkusativ", "prĂ¤positionen", "konjugation", "verben"]
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
CONNECT_STR = "mariadb+mariadbconnector://admin:PASSWORD@deutsch-db.cuno5ecnfsgi.eu-central-1.rds.amazonaws.com:3306/deutsch-db"

def get_json(json_path):
    with open(JSON_PATH) as json_file:
        json_dict = json.load(json_file)
    return json_dict

def get_sql_data(sql_path):
    pass

def check_entry(entry, atts=["link", "keywords", "level", "grammar"]):
    """
    entry: checks if a json entry is valid
    """
    errors = False
    msg = ""
    # Check for broken link
    try:
        requests.get(entry[atts[0]])
        msg += "Link OK. <br />"
        print("Link OK.")
    except ConnectionError:
        msg += "!!! Broken link {}".format(entry[atts[0]]) + "<br />"
        print("!!! Broken link {}".format(entry[atts[0]])) #TODO: Raise error
        errors=True

    # Check if keywords are valid
    """ not checking keywords-grammar for now
    for kw in entry[atts[1]]:
        if kw.lower() not in KEYWORDS:
            msg += "!!! Invalid keyword {}.".format(kw) + "<br />"
            print("!!! Invalid keyword {}.".format(kw)) #TODO: Raise error
            errors=True
        else:
            msg += "Keyword OK." + "<br />"
            print("Keyword OK.")
            
    # Check if gram_keywords are valid 
    for kw in entry[atts[3]]:
        if kw.lower() not in GRAM_KEYWORDS:
            msg += "!!! Invalid keyword {}.".format(kw) + "<br />"
            print("!!! Invalid keyword {}.".format(kw)) #TODO: Raise error
            errors=True
        else:
            msg += "Grammar keyword OK." + "<br />"
            print("Grammar keyword OK.")
    """
    
    # Check if level is valid
    """
    if entry[atts[2]] not in LEVELS:
        msg += "!!! Invalid level {}.".format(entry[atts[2]]) + "<br />"
        print("!!! Invalid level {}.".format(entry[atts[2]])) #TODO: Raise error
        errors=True
    else:
        msg += "Levels OK. <br />"
        print("Levels OK.")
    """
    if errors == False:
        msg += "No problems found." + "<br />"
        print("No problems found.")
    return not errors, msg

def exclude_empty_str(lst):
    """
    Returns list without empty strings.
    """
    return [el for el in lst if el.strip() != ""]

def create_df_from_sql():
    engine = create_engine(CONNECT_STR)
    #engine = create_engine("mariadb+mariadbconnector://testUser@127.0.0.1:3306/test")
    conn = engine.connect()
    query = "call concat_select"
    df = pd.read_sql_query(query, conn)
    df['level'] = df['level'].apply(lambda x: x.split(","))
    df['keywords'] = df['keywords'].apply(lambda x: x.split(","))
    df['grammar'] = df['grammar'].apply(lambda x: x.split(","))
    print(df["level"])
    return df

def create_df(json_dict, validate_entries=False):
    """
    Creates pandas DataFrame with the json entries that don't have errors.
    Returns pandas DF and list of error indexes.
    """
    japproved = {}
    error_indexes = []
    for key in json_dict:
        if validate_entries:
            if not check_entry(json_dict[key])[0]:
                print("ERROR in entry {}".format(key)) #TODO: Raise error
                error_indexes.append(key)
            # If there is no error, add entry to jtested
            else:
                japproved[key] = json_dict[key]
        else:
            japproved[key] = json_dict[key]
    df = pd.DataFrame(japproved)
    df = df.transpose() #TODO: deve ter um jeito melhor de resolver isso
    #Making sure there are no empty strings:
    df['level'] = df['level'].apply(lambda l: exclude_empty_str(l))
    df['keywords'] = df['keywords'].apply(lambda l: exclude_empty_str(l))
    df['grammar'] = df['grammar'].apply(lambda l: exclude_empty_str(l))
    return df, error_indexes

def add_entry_sql(db_conn, entry):
    pass

def add_entry(json_dict, entry): #, df):
    """
    Adds dict entry to JSON dict.
    Returns modified JSON.
    """
    check, error_msg = check_entry(entry)
    if not check:
        return json_dict, error_msg
    json_key_idx = [int(i) for i in json_dict.keys()]
    new_key = str(max(json_key_idx)+1)
    json_dict[new_key] = entry
    #entry["index"] = int(new_key)
    #df.append(pd.DataFrame(entry).set_index("index"))
    #NĂ£o tĂ¡ atualizando o df, nĂ£o sei pq
    with open(JSON_PATH, 'w') as outfile:
        json.dump(json_dict, outfile)
    return json_dict, error_msg#, df

def search(df, search_terms):
    """
    Parameters
    ----------
    df : pandas DataFrame
        Containing course data.
    search_terms : dict
        Containing search terms by category.

    Returns
    -------
    DataFrame with matches.
    """
    #TODO: busca com AND ou OR?
    
    #Helper function to check for intersection between list of search terms and terms in columns with lists.
    def compare(a,b):   #TODO: renomear funĂ§Ă£o
        a_ = set(a)
        b_ = set(b)
        return len(a_ & b_) != 0
    
    def check_match(df, search_terms, attrs):
        """
        Adds column of boolean to DF with matches for each attribute.
        Case insensitive.
        """
        df_ = df.copy()
        for attr in attrs:
            df_.loc[df_[attr].apply(lambda x: compare([el.lower() for el in x], [s.lower() for s in search_terms[attr]])), attr+"_match"]=True
            df_.loc[~df_[attr].apply(lambda x: compare([el.lower() for el in x], [s.lower() for s in search_terms[attr]])), attr+"_match"]=False
        return df_

    def build_query(df_search, attrs=["level", "keywords", "grammar"], conns=['&','|']):
        query = ""
        #TODO: placeholder, depois faz o mĂ©todo pra montar os queries
        query = "(" + attrs[0] + '_match==True) & (' + attrs[1] + '_match==True) & (' + attrs[2] + '_match==True)'
        print(query)
        return query

    search_terms_ = search_terms.copy()
    print(search_terms_)
    df_search_ = check_match(df, search_terms_, ["level", "keywords", "grammar"])
    query = build_query(df_search_)
    res_df = df_search_.query(query).loc[:, df.columns]
    #res_df = df.loc[(df["level"]==search_terms["level"]) & ((df["grammar"].apply(lambda x: compare(x, search_terms["grammar"]))) | (df["keywords"].apply(lambda x: compare(x, search_terms["keywords"]))))]
    return res_df

def df_to_html_pretty(df, to_replace=["-keine-,", "-keine-", "]", "[", "]"]):
    """
    DF to HTML. Replaces strings in to_replace with empty string.
    Capitalizes table header.
    """
    df_out = df.to_html(render_links=True, index=False)
    for el in to_replace:
        df_out = df_out.replace(el, "")
    
    for el in re.findall(r'<th>(.*?)</th>', df_out):
        df_out = df_out.replace(el, el.capitalize())
    return df_out

def check_empty(lst, default="-keine-"):
    """
    Replaces empty values in list with default string.
    """
    checked_lst = [el for el in lst if el != ""]
    if len (checked_lst) == 0:
        return [default]
    return checked_lst

def preprocess_query(proc, q, min_ratio=80, db=CONNECT_STR):
    """
    q: query str
    min_ratio: min ratio float
    db: str with address of sql db
    proc: stored procedure in db

    Cleans query string, searches for closest match in sql db. If there is no match with min_ratio, 
    returns q, else returns match.
    """
    engine = create_engine(db)
    conn = engine.connect()
    query = "call {}".format(proc)
    res = conn.execute(text(query))
    res_lst = res.fetchall()
    term_lst = [el[0] for el in res_lst]
    for term in term_lst:
        if fuzz.ratio(q.lower(), term.lower()) > min_ratio: #TODO: aqui ele pega o primeiro >75, nĂ£o o melhor match
            return term
    return q

#print(preprocess_query("select_all_grammar", "pretaeritum"))

#res_df = df.loc[(df["level"]==search_terms_["level"]) & (search_terms_["grammar"][0] in df["grammar"].iloc[1])]
# res_df = df.loc[(df["level"]==search_terms["level"]) & (len(df["grammar"].apply(lambda x: compare(x, search_terms["grammar"]))))]

#test_search = {"level": "A1", "grammar": ["dativ"], "keywords":["arbeit"]}
#df2 = search(df, test_search)

#test_search = {"level": "A1", "grammar": ["konjugation"], "keywords":[]}
#df2 = search(df, test_search)
#print(df2)

#jtemp = get_json(JSON_PATH)
#df2, e = create_df(jtemp)
#df = create_df_from_sql()
#print(df)
#print(df2)

#query = "call {}(:queryVal)".format(proc)
    #res = conn.execute(text(query), queryVal=q)
    #term = res.fetchall()[0][0]