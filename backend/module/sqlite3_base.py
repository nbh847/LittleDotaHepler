import sqlite3


class HeroProfile:
    def __init__(self):
        # 连接到SQLite数据库（如果不存在，将创建一个新的数据库文件）
        self.conn = sqlite3.connect('data/arena.db')
        # 创建一个游标对象，用于执行SQL命令
        self.cursor = self.conn.cursor()

    def execute(self, statement: str):
        """
        执行任意sql语句
        :param statement:
        :return:
        """
        self.cursor.execute(statement)
        self.conn.commit()

    def create_table(self):
        """
        创建新表
        :return:
        """
        statement = '''CREATE TABLE IF NOT EXISTS arena_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attack1 TEXT,
            attack2 TEXT,
            attack3 TEXT,
            attack4 TEXT,
            attack5 TEXT,
            defend1 TEXT,
            defend2 TEXT,
            defend3 TEXT,
            defend4 TEXT,
            defend5 TEXT,
            win_rate REAL
        )'''
        self.execute(statement)

    def drop_table(self, table_name):
        """
        删表
        :param table_name:
        :return:
        """
        self.execute("drop table {};".format(table_name))

    def clear_table(self, table_name):
        """
        清除表里的所有数据
        :param table_name:
        :return:
        """
        self.execute("DELETE FROM {};".format(table_name))

    def get_all(self, table_name):
        # 查询数据
        rows = self.cursor.execute("SELECT * FROM {}".format(table_name)).fetchall()
        for row in rows:
            print(row)

    def match_cracked_lineup(self, statement):
        """
        匹配破解阵容
        :param statement:
        :return:
        """
        res = []
        rows = self.cursor.execute(statement)
        for row in rows:
            res.append(row)
        return res

    def insert(self, data: list):
        statement = """INSERT OR REPLACE INTO arena_data ( 
            attack1, attack2, attack3, attack4, attack5, defend1, defend2, defend3, defend4, defend5, win_rate
        ) VALUES (
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10])
        # 插入一条数据
        self.cursor.execute(statement)
        # 提交更改
        self.conn.commit()

    @classmethod
    def generate_peak_arena_lineup_query(cls, lineup: list):
        """
        生成巅峰竞技场阵容的 sql query 语句
        :param lineup: eg. ["骨王", "", "", "幻刺", "白虎"], ["潮汐", "全能", "", "巫医", ""]
        :return:
        """
        cond_statement = []
        for index, name in enumerate(lineup):
            if name:
                cond_statement.append("defend{}='{}'".format(index + 1, name))
        cond_statement_str = " and ".join(cond_statement)
        statement = "SELECT * FROM arena_data where {}".format(cond_statement_str)
        print("statement", statement)
        return statement

    def __del__(self):
        self.conn.close()
