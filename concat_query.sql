        SELECT url.urlval as "link", group_concat(DISTINCT(level.levelval) separator ",") as "level", group_concat(DISTINCT(grammarkeywords.grammarval) separator ",") as "grammar", group_concat(DISTINCT(tkeywords.tval) separator ",") as "keywords" FROM url
        inner join url_grammar on url.urlid = url_grammar.urlid
        inner join url_level on url.urlid = url_level.urlid
        inner join url_tkeywords on url.urlid = url_tkeywords.urlid
        inner join grammarkeywords on grammarkeywords.grammarid = url_grammar.grammarid
        inner join tkeywords on tkeywords.tid = url_tkeywords.tid
        inner join level on level.levelid = url_level.levelid
        group by url.urlid;