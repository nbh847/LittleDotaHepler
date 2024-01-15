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


def get_sorted_lineup(lineup) -> str:
    """
    获取排序好的整容
    :param lineup:
    :return:
    """
    return ",".join(sorted(list(lineup)))


def get_crack_lineup() -> dict:
    """
    获取破解整容的json数据
    :return:
    """
    result = {}
    try:
        with open("data/crack_lineup.json", "r") as file:
            result = json.loads(file.read())
    except Exception as e:
        print("get_crack_lineup error:{}".format(e.args[0]))
    return result


def crack_peak_arena_lineup(my_hero_pool: list, lineup1: list, lineup2: list, lineup3: list):
    """
    猜 <巅峰竞技场> 的阵容，返回自己英雄池存在的破解阵容
    :param my_hero_pool: 自己的英雄池
    :param lineup1: 第一队
    :param lineup2: 第二队
    :param lineup3: 第三队
    :return:
    """
    profiles = get_hero_profiles()
    print(profiles)


def crack_arena_lineup(my_hero_pool: list, defend_lineup: list, ignore_hero_pool=False):
    """
    根据自己英雄池返回 <普通竞技场> 破解阵容
    :param my_hero_pool:
    :param defend_lineup:
    :return:
    """
    all_crack_lineups = get_crack_lineup()
    sorted_defend_lineup = get_sorted_lineup(defend_lineup)
    print("对方阵容", sorted_defend_lineup)

    cracked_lineups = all_crack_lineups.get(sorted_defend_lineup)
    if cracked_lineups:
        for cracked_lineup in cracked_lineups:
            lineup = cracked_lineup.get("attack")
            rate = cracked_lineup.get("rate")

            has_matched_hero = True
            for hero in lineup.split(","):
                if hero not in my_hero_pool:
                    has_matched_hero = False
                    break
            if ignore_hero_pool:
                print("破解阵容", lineup)
                print("胜率", rate)
            elif has_matched_hero:
                print("破解阵容", lineup)
                print("胜率", rate)


def generate_latest_attack_lineup():
    """
    根据最新的竞技场对阵数据Excel生成攻击方的阵容(防守方的破解阵容)
    文件保存到: data/crack_lineup.json
    :return: [["1", "2", "3", "4", "5"], ["23", "24", "25", "26", "27"], ["23", "24", "75", "26", "17"]]
    """
    saved_res = {}
    excel = pd.read_excel("data/arena_data.xlsx")

    for index, row in excel.iterrows():
        print(f"第{index + 1}行数据：")
        attack_lineup = set()
        defend_lineup = set()
        for inner_index, values in enumerate(row.items()):
            # inner_index: 0-4 是攻, 5-9 是守，10 是进攻胜率
            # print("values", values)
            if inner_index <= 4:
                attack_lineup.add(values[1])
            elif inner_index <= 9:
                defend_lineup.add(values[1])
            elif inner_index == 10:
                try:
                    winning_rate = round(values[1], 2)
                except Exception as e:
                    print("winning_rate count error:{}".format(e.args[0]))
                    winning_rate = 0
                if winning_rate >= 0.5:
                    # 胜率大于 50%
                    if saved_res.get(get_sorted_lineup(defend_lineup)):
                        saved_res.get(get_sorted_lineup(defend_lineup)).append({
                                "defend": get_sorted_lineup(defend_lineup),
                                "attack": get_sorted_lineup(attack_lineup),
                                "rate": "{} %".format(winning_rate * 100)
                            })
                    else:
                        saved_res[get_sorted_lineup(defend_lineup)] = [{
                                "defend": get_sorted_lineup(defend_lineup),
                                "attack": get_sorted_lineup(attack_lineup),
                                "rate": "{} %".format(winning_rate * 100)
                            }]
    print("saved_res", saved_res)
    print("len saved_res", len(saved_res))
    with open("data/crack_lineup.json", "w") as file:
        res = json.dumps(saved_res)
        file.write(res)
    print("生成破解阵容的数据完毕，保存路径为:{}".format("data/crack_lineup.json"))


def run():
    print("小冰冰传奇助手开始运行")
    my_heros = ["光法", "大鱼", "巨魔", "影魔", "舞姬", "宙斯", "一姐", "发条", "圣堂", "死灵", "潮汐"]
    defend_lineup = ["骨王", "火猫", "精灵", "一姐", "圣堂"]
    crack_arena_lineup(my_heros, defend_lineup, True)


if __name__ == '__main__':
    # 从Excel里获取最新的英雄数据，检查表格里的异常数据并修改
    # get_hero()
    # 生成破解整容
    # generate_latest_attack_lineup()
    # res = get_crack_lineup()
    # for key, value in res.items():
    #     print("key", key)
    #     print("value", value)
    # print("len res", len(res))
    run()
