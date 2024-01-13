import json
import os

import flask
import pandas as pd


excel = pd.read_excel("data/arena_data.xlsx")


def get_hero():
    """
    获取最新的英雄数据
    :return:
    """
    print("")
    data_map = set()

    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        for inner_index, values in enumerate(row.items()):
            # inner_index: 0-4 是攻, 5-9 是守，10 是进攻胜率
            data_map.add(values[1])
            if inner_index == 9:
                break
    print(data_map)
    print(len(data_map))


def guess_lineup(line1=""):
    """
    猜巅峰竞技场的阵容
    :return:
    """
    pass


def run():
    print("小冰冰传奇助手开始运行")

    with open("data/heros.json", "r") as file:
        heros = json.loads(file.read())
    # 前中后排英雄
    front_hero = heros[0]
    middle_hero = heros[1]
    back_hero = heros[2]
    print("front_hero:{}".format(front_hero))
    print("middle_hero:{}".format(middle_hero))
    print("back_hero:{}".format(back_hero))
    print("英雄总数:{}".format(len(back_hero) + len(middle_hero) + len(front_hero)))

    # data_map = set()
    #
    # for index, row in excel.iterrows():
    #     print(f"第{index + 1}行数据：")
    #     for column, value in row.items():
    #         print(f"{column}: {value}")
    #         data_map.add(value)
    #     break
    # print(data_map)


if __name__ == '__main__':
    run()
