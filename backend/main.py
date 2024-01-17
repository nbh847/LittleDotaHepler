import json
import os

import flask
import pandas as pd

from module.sqlite3_base import HeroProfile


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


def guess_peak_arena_lineup(lineup1: list, lineup2: list, lineup3: list):
    """
    猜 <巅峰竞技场> 的阵容;
    巅峰竞技场的防守阵容，每队最多隐藏两个位置，要根据站位情况猜测出隐藏的英雄;
    :param lineup1: ["白虎", "幻刺", "", "", "骨王"]
    :param lineup2: ["", "巫医", "", "全能", "潮汐"]
    :param lineup3: ["", "小黑", "", "军团", "末日"]
    :return:
    """
    guessed_lineup = []
    profiles = get_hero_profiles()

    # 获得明面上的防守方英雄
    known_hero = [i for i in lineup1 if i]
    known_hero += [i for i in lineup2 if i]
    known_hero += [i for i in lineup3 if i]

    # 只要猜出两队的防守阵容，就保存这个防守阵容
    # 第一队
    profile_lineup1 = [profiles.get(hero) for hero in lineup1 if hero]
    profile_lineup1 = [i for i in profile_lineup1 if i]
    sorted_lineup1 = sorted(profile_lineup1, key=lambda x: x["location"])
    print(sorted_lineup1)
    # 第二队

    # 第三队


def crack_peak_arena_lineup(my_hero_pool: list, lineup1: list, lineup2: list, lineup3: list, ignore_hero_pool=False):
    """
    根据自己英雄池返回 <巅峰竞技场> 破解阵容
    :param my_hero_pool: 自己的英雄池
    :param lineup1: 第一队
    :param lineup2: 第二队
    :param lineup3: 第三队
    :param ignore_hero_pool: 忽视自己的英雄池，直接返回破解阵容
    :return:
    """
    guess_peak_arena_lineup(lineup1, lineup2, lineup3)


def crack_arena_lineup(my_hero_pool: list, defend_lineup: list, ignore_hero_pool=False):
    """
    根据自己英雄池返回 <普通竞技场> 破解阵容
    :param my_hero_pool: 自己的英雄池
    :param defend_lineup: 防守方的阵容
    :param ignore_hero_pool: 忽视自己的英雄池，直接返回破解阵容
    :return:
    """
    sorted_defend_lineup = get_sorted_lineup(defend_lineup)
    print("对方阵容", sorted_defend_lineup)

    heros = sorted_defend_lineup.split(",")
    statement = """SELECT * FROM arena_data where defend1='{}' and defend2='{}' and defend3='{}' and defend4='{}' and defend5='{}'""".format(
        heros[0], heros[1], heros[2], heros[3], heros[4]
    )
    attack_lineups = HeroProfile().match_cracked_lineup(statement)
    if attack_lineups:
        for cracked_lineup in attack_lineups:
            lineup = [i for i in cracked_lineup[1:6]]
            rate = cracked_lineup[11]

            has_matched_hero = True
            for hero in lineup:
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
    文件保存到sqlite3
    :return: eg. [["1", "2", "3", "4", "5"], ["23", "24", "25", "26", "27"], ["23", "24", "75", "26", "17"]]
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
                                "rate": winning_rate * 100
                            })
                    else:
                        saved_res[get_sorted_lineup(defend_lineup)] = [{
                                "defend": get_sorted_lineup(defend_lineup),
                                "attack": get_sorted_lineup(attack_lineup),
                                "rate": winning_rate * 100
                            }]
    print("len saved_res", len(saved_res))
    for index, value in enumerate(saved_res.items()):
        print("写入第:{}行的数据".format(index + 1))
        for item in value[1]:
            defends = item.get("defend").split(",")
            attacks = item.get("attack").split(",")
            rate = item.get("rate")
            if len(attacks) < 5 or len(defends) < 5:
                continue
            data = attacks + defends + [rate]
            print('data', data)
            HeroProfile().insert(data)

    print("生成破解阵容的数据完毕，保存到了数据库")


def run():
    print("小冰冰传奇助手开始运行")
    my_heros = ["光法", "大鱼", "巨魔", "影魔", "舞姬", "宙斯", "一姐", "发条", "圣堂", "死灵", "潮汐"]
    defend_lineup = ["骨王", "火猫", "精灵", "一姐", "圣堂"]
    # 获取普通竞技场的破解阵容
    crack_arena_lineup(my_heros, defend_lineup, True)
    # 获取巅峰竞技场的破解阵容
    # lineup1 = ["白虎", "幻刺", "", "", "骨王"]
    # lineup2 = ["", "巫医", "", "全能", "潮汐"]
    # lineup3 = ["", "小黑", "", "军团", "末日"]
    # crack_peak_arena_lineup(my_heros, lineup1, lineup2, lineup3)


if __name__ == '__main__':
    # 从Excel里获取最新的英雄数据，检查表格里的异常数据并修改
    # get_hero()
    # 生成破解整容
    # generate_latest_attack_lineup()

    run()
    # HeroProfile().create_table()
    # HeroProfile().clear_table("arena_data")
    # HeroProfile().get_all("arena_data")
    # HeroProfile().execute("drop table hero;")
    # HeroProfile().execute("DELETE FROM hero WHERE id = 2;")
