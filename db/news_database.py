import os
import sqlite3


class NewsDB:
    def __init__(self):
        self.cursor = None
        self.conn = None
        pass

    def open_db(self, path=""):
        if path:
            os.path.join(path, "db.sqlite")
            self.conn = sqlite3.connect(
                os.path.join(path, "db.sqlite"), check_same_thread=False
            )
        else:
            self.conn = sqlite3.connect(
                os.path.dirname(__file__) + "/info_database.sqlite",
                check_same_thread=False,
            )
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def get_cursor(self):
        return self.cursor

    def get_conn(self):
        return self.conn

    # 插入新闻
    def insert_news(self, title, time, content, source, url, cls):

        stm = """insert OR IGNORE into news(title, date ,content, source, url, cls) values(
              ?,?,?,?,?,?)"""
        self.cursor.execute(stm, (title, time, content, source, url, cls))
        docId = self.cursor.lastrowid
        self.conn.commit()
        return docId

    # 查询全部文档
    def query_all_docs(self):

        result = self.cursor.execute("select * from news")
        self.conn.commit()
        return result.fetchall()

    # 根据doc_id的列表，源和日期进行查询
    def query_specific(self, doc_ids, date_begin, date_end, source, cls):
        ids_str = ",".join(str(doc_id) for doc_id in doc_ids)
        sql = "select * from news where id in (" + ids_str + ")"
        cls.append("")
        if cls:
            sql += " and cls in ('{}')".format("','".join(cls))
        if source:
            sql += " and source in ('{}')".format("','".join(source))
        if date_begin and date_end:
            sql += " and date>= '{}' and date<= '{}'".format(date_begin, date_end)
        print(sql)
        results = self.cursor.execute(sql)
        all_news = results.fetchall()
        self.conn.commit()
        return all_news

    # 查询全部doc_id
    def query_doc_ids(self):
        sql = "select id from news"
        # 执行语句
        results = self.cursor.execute(sql)

        # 遍历打印输出
        doc_ids = results.fetchall()
        self.conn.commit()

        return set([item[0] for item in doc_ids])

    # 从倒排索引中根据word进行查询
    def query_doc_ids_by_word(self, word):

        sql = "select doc_id from inverted_index where word= ?"
        # 执行语句
        results = self.cursor.execute(sql, (word,))

        # 遍历打印输出
        doc_id = results.fetchone()
        self.conn.commit()
        if not doc_id:
            return set()
        return set(map(int, doc_id[0].split(",")))

    # 插入倒排索引
    def insert_inverted_index(self, inverted_index):
        stm = """REPLACE INTO inverted_index(word, doc_id) values(
              ?,?)"""
        self.cursor.executemany(stm, inverted_index)
        self.conn.commit()
        return

    """
    doc= {“title”: “xxx”, “time”: “xxx”, “content”: “xxx”, “source”: “xxx” , “url”: “xxx”}
    """

    # 重新初始化两个表
    def create_news_table(self):

        drop_statement = """
        DROP TABLE IF EXISTS `news`;
        """
        self.cursor.execute(drop_statement)

        self.conn.commit()

        create_statement = """create table if not exists news(
                id integer primary key autoincrement,
                title text unique,
                content text,
                source text,
                date DATE ,
                url text,
                cls text
            )"""

        self.cursor.execute(create_statement)
        self.conn.commit()

    def create_index_table(self):
        drop_statement = """
        DROP TABLE IF EXISTS `inverted_index`;
        """
        self.cursor.execute(drop_statement)

        self.conn.commit()

        create_statement = """create table if not exists inverted_index(
                id integer primary key autoincrement,
                word varchar unique,
                doc_id text
            )"""

        self.cursor.execute(create_statement)
        self.conn.commit()
