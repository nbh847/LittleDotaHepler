import json
import os

import flask
import pandas as pd


def get_hero():
    """
    获取最新的英雄数据
    :return:
    """
    print("获取最新的英雄数据")
    data_map = set()
    excel = pd.read_excel("data/arena_data.xlsx")

    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        for inner_index, values in enumerate(row.items()):
            # inner_index: 0-4 是攻, 5-9 是守，10 是进攻胜率
            data_map.add(values[1])
            if inner_index == 9:
                break
    print(data_map)
    print(len(data_map))


def get_hero_profiles() -> dict:
    """
    获取所有英雄的各项数据
    :return:
    """
    result = []
    try:
        with open("data/hero_profile.json", "r") as file:
            res = file.read()
        result = json.loads(res)
    except Exception as e:
        print("获取所有英雄的各项数据 error:{}".format(e.args[0]))
    return result


def guess_lineup(my_hero_pool: list, line1: list, line2: list, line3: list):
    """
    猜巅峰竞技场的阵容，返回自己英雄池存在的破解阵容
    :param my_hero_pool: 自己的英雄池
    :param line1: 第一队
    :param line2: 第二队
    :param line3: 第三队
    :return:
    """
    profiles = get_hero_profiles()
    print(profiles)


def generate_latest_attack_lineup() -> list:
    """
    根据最新的竞技场对阵数据Excel生成攻击方的阵容(防守方的破解阵容)
    :return: [["1", "2", "3", "4", "5"], ["23", "24", "25", "26", "27"], ["23", "24", "75", "26", "17"]]
    """
    data_map = set()
    excel = pd.read_excel("data/arena_data.xlsx")

    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        attack_lineup = set()
        defend_lineup = set()
        for inner_index, values in enumerate(row.items()):
            # inner_index: 0-4 是攻, 5-9 是守，10 是进攻胜率
            print("values", values)
            if inner_index <= 4:
                attack_lineup.add(values[1])
            elif inner_index <= 9:
                defend_lineup.add(values[1])
            elif inner_index == 10:
                winning_rate = float(values[1])
                if winning_rate >= 0.5:
                    # 胜率大于 50%
                    saved_res = {defend_lineup: attack_lineup}
        break
    print(data_map)
    print(len(data_map))


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

    guess_lineup([], [], [], [])


if __name__ == '__main__':
    generate_latest_attack_lineup()