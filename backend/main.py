import flask
import pandas as pd


def run():
    print("小冰冰传奇助手开始运行")
    data_map = set()
    excel = pd.read_excel("arena_data.xlsx")
    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        for column, value in row.items():
            print(f"{column}: {value}")
            data_map.(value)
    print(data_map)


if __name__ == '__main__':
    run()
