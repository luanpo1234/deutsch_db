from sqlalchemy import MetaData, create_engine
from sqlalchemy.sql import select
import pymysql
import itertools
import pandas as pd

EXCEL_PATH = "flask_ddb\Book1.xlsx"
DF = pd.read_excel(EXCEL_PATH)

CONNECT_STR = api.CONNECT_STR
ENGINE = create_engine(CONNECT_STR)
CONN = ENGINE.connect()
META_DATA = MetaData(bind=CONN)
META_DATA.reflect()

def excel_to_dict(excel_path, cols=["URL", "LEVELS", "THEME_KEYWORDS", "GRAMMAR_KEYWORDS"], default="-keine-"):
    df = pd.read_excel(EXCEL_PATH).fillna("-keine-")
    d_df = df.to_dict()
    d_unique = {}
    for col in cols:
        lst = [el.split(",") for el in df[col].unique()]
        if default not in lst:
            lst.append(default)
        lst = list(itertools.chain.from_iterable(lst))
        lst = [el.strip() for el in lst]
        d_unique[col] = lst
    for k0 in d_df:
        if k0 != cols[0]:   #Default doesn't apply to URL
            for k1 in d_df[k0]:
                if default not in d_df[k0][k1]:
                    d_df[k0][k1] += ", " + default
    return d_unique, d_df

def dict_to_sql(dcts, conn, keys={
    "URL":["url","urlval"], "LEVELS":["level","levelval"], "THEME_KEYWORDS":["tkeywords","tval"],
    "GRAMMAR_KEYWORDS":["grammarkeywords","grammarval"]},
    junc_tables = ["url_grammar", "url_level", "url_tkeywords"]):

    d_unique = dcts[0]
    d_df = dcts[1]
    tables = {}
    trans = conn.begin()
    for k, v in keys.items():
        for el in d_unique[k]:
            tables[v[0]] = META_DATA.tables[v[0]]
            stmt = tables[v[0]].insert().prefix_with("IGNORE").values([None, el])
            #conn.execute(f"INSERT IGNORE INTO {v[0]} ({v[1]}) VALUES ('{el}');")
            conn.execute(stmt)
    for k, v in d_df["URL"].items():
        stmt = select([tables["url"].c["UrlId"]]).where(tables["url"].c["UrlVal"] == v)
        url_id = conn.execute(stmt).fetchall()[0][0]
        for gram_kw in d_df["GRAMMAR_KEYWORDS"][k].split(","):
            gram_kw = gram_kw.strip() #TODO: criar um preprocessamento geral
            stmt = select([tables["grammarkeywords"].c["GrammarId"]]).where(tables["grammarkeywords"].c["GrammarVal"] == gram_kw)
            grammar_id = conn.execute(stmt).fetchall()[0][0]
            stmt = META_DATA.tables["url_grammar"].insert().prefix_with("IGNORE").values([url_id, grammar_id])
            conn.execute(stmt)
        for lvl_kw in d_df["LEVELS"][k].split(","):
            lvl_kw = lvl_kw.strip() #TODO: criar um preprocessamento geral
            stmt = select([tables["level"].c["LevelId"]]).where(tables["level"].c["LevelVal"] == lvl_kw)
            lvl_id = conn.execute(stmt).fetchall()[0][0]
            stmt = META_DATA.tables["url_level"].insert().prefix_with("IGNORE").values([url_id, lvl_id])
            conn.execute(stmt)
        for t_kw in d_df["THEME_KEYWORDS"][k].split(","):
            t_kw = t_kw.strip() #TODO: criar um preprocessamento geral
            stmt = select([tables["tkeywords"].c["TId"]]).where(tables["tkeywords"].c["TVal"] == t_kw)
            t_id = conn.execute(stmt).fetchall()[0][0] #aí tem que pegar o primeiro aqui
            stmt = META_DATA.tables["url_tkeywords"].insert().prefix_with("IGNORE").values([url_id, t_id])
            conn.execute(stmt)
    #for url in tables["url"]:
     #  urlid = select([tables["url"].c["UrlId"]])
    trans.commit()
    #stmt = select([tables["grammarkeywords"].c["GrammarId"]]).where(tables["grammarkeywords"].c["GrammarVal"] == "Dativ")
    #stmt = select([tables["url"].c["UrlId"]])
    #res = conn.execute(stmt).fetchall()
    conn.close()
    #print([el[0] for el in res])

dcts = excel_to_dict(EXCEL_PATH)
dict_to_sql(dcts, CONN)