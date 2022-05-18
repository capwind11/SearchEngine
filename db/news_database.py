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

    def insert_news(self, title, time, content, source, url, cls):
        stm = """insert OR IGNORE into news(title, date ,content, source, url, cls) values(
              ?,?,?,?,?,?)"""
        self.cursor.execute(stm, (title, time, content, source, url, cls))
        docId = self.cursor.lastrowid
        self.conn.commit()
        return docId

    def query_all_docs(self):

        result = self.cursor.execute("select * from news")
        self.conn.commit()
        return result.fetchall()

    def query_by_doc_id(self, doc_ids):
        sql = (
            "select id,title,url from news where id in ("
            + ",".join(str(doc_id) for doc_id in doc_ids)
            + ")"
        )

        # 执行语句
        results = self.cursor.execute(sql)

        # 遍历打印输出
        all_news = results.fetchall()
        self.conn.commit()
        return all_news

    def query_by_specific_info(self, news_date, source):
        sql = """select id,title,url from news where date= ? and source = ?"""

        # 执行语句
        results = self.cursor.execute(sql, (news_date, source))

        # 遍历打印输出
        all_news = results.fetchall()
        self.conn.commit()
        return all_news

    def query_doc_ids_by_word(self, word):
        sql = "select doc_id from inverted_index where word= ?"
        # 执行语句
        results = self.cursor.execute(sql, (word,))

        # 遍历打印输出
        doc_id = results.fetchone()
        self.conn.commit()
        return set(map(int, doc_id[0].split(",")))

    def insert_inverted_index(self, inverted_index):
        stm = """insert OR IGNORE into inverted_index(word, doc_id) values(
              ?,?)"""
        self.cursor.executemany(stm, inverted_index)
        self.conn.commit()
        return

    """
    doc= {“title”: “xxx”, “time”: “xxx”, “content”: “xxx”, “source”: “xxx” , “url”: “xxx”}
    """

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
