import flask
import pandas as pd


excel = pd.read_excel("data/arena_data.xlsx")


def get_hero():
    print("获取最新的英雄数据")
    data_map = set()

    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        for inner_index, values in enumerate(row.items()):
            # inner_index: 0-4 是攻, 5-9 是守，10 是进攻胜率
            print(f"{inner_index}: {values}")
            data_map.add(values[1])
            if inner_index == 9:
                break
    print(data_map)

def run():
    print("小冰冰传奇助手开始运行")
    data_map = set()

    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        for column, value in row.items():
            print(f"{column}: {value}")
            data_map.add(value)
        break
    print(data_map)


if __name__ == '__main__':
    get_hero()
