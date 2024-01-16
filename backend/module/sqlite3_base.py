import sqlite3


class HeroProfile:
    def __init__(self):
        # 连接到SQLite数据库（如果不存在，将创建一个新的数据库文件）
        self.conn = sqlite3.connect('data/arena.db')
        # 创建一个游标对象，用于执行SQL命令
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        创建新表
        :return:
        """
        # 创建一个新表
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hero (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            type TEXT,
            position TEXT,
            location INTEGER,
            img TEXT
        )''')
        self.conn.commit()

    def execute(self, statement: str):
        """
        执行任意sql语句
        :param statement:
        :return:
        """
        self.cursor.execute(statement)
        self.conn.commit()

    def get(self, statement=""):
        # 查询数据
        rows = self.cursor.execute("SELECT * FROM hero").fetchall()
        for row in rows:
            print(row)

    def insert(self, statement=""):
        statement = "INSERT OR REPLACE INTO hero (name, type, position, location, img) VALUES ('尸王', '力量', '前排', 1070, 'img')"
        # 插入一条数据
        self.cursor.execute(statement)
        # 提交更改
        self.conn.commit()

    def __del__(self):
        self.conn.close()
