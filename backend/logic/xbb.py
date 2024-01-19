import copy
import json

import pandas as pd

from helper.utils import is_subset, has_common_element
from module.sqlite3_base import HeroProfile


my_heros = ["大鱼", "巨魔", "影魔", "舞姬", "宙斯", "修补", "暗牧", "尸王", "骨王", "巫妖", "光法", "人马", "冰女", "小黑",
            "全能", "潮汐", "天怒", "幻刺", "DP", "一姐", "末日", "巫医", "白虎", "火猫", "剑圣", "神灵"]


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
    result = {}
    try:
        with open("data/hero_profile.json", "r") as file:
            res = file.read()
        result = json.loads(res)
    except Exception as e:
        print("获取所有英雄的各项数据 error:{}".format(e.args[0]))
    return result


def sort_defend_lineup(defends: list) -> list:
    """
    按照英雄的站位排序
    :param defends:
    :return:
    """
    profiles = get_hero_profiles()
    sort_items = {i: int(profiles.get(i).get("location")) for i in defends}
    sorted_keys = [k for k, v in sorted(sort_items.items(), key=lambda item: item[1])]
    return sorted_keys


def get_sorted_lineup(lineup) -> str:
    """
    获取排序好的整容
    :param lineup:
    :return:
    """
    return ",".join(sorted(list(lineup)))


def get_guess_lineup(lineup: list):
    """
    猜测阵容的隐藏英雄，并返回破解阵容
    :param lineup:
    :return: [[隐藏的英雄], [可能的防守阵容], [对应的破解阵容], 胜率]
    """
    statement = HeroProfile.generate_peak_arena_lineup_query(lineup)
    matched_heros = HeroProfile().match_cracked_lineup(statement)

    # 保存匹配的阵容
    saved_match_lineup = []
    for matched_hero in matched_heros:
        defend_lineup = matched_hero[6:-1]
        attack_lineup = matched_hero[1:6]
        rate = matched_hero[-1]
        # 拿到可能的隐藏阵容
        hidden_lineup1 = []
        for index, item in enumerate(lineup):
            if not item:
                hidden_lineup1.append(defend_lineup[index])
        # [[隐藏的英雄], [可能的防守阵容], [对应的破解阵容], 胜率]
        saved_match_lineup.append([hidden_lineup1, defend_lineup, attack_lineup, rate])
    # print("可能匹配的阵容数据", saved_match_lineup)
    return saved_match_lineup


def crack_peak_arena_lineup(my_hero_pool: list, lineup1: list, lineup2: list, lineup3: list, ignore_hero_pool=False):
    """
    猜 <巅峰竞技场> 的阵容;
    巅峰竞技场的防守阵容，每队最多隐藏两个位置，要根据站位情况猜测出隐藏的英雄;
    防守方显示的站位顺序跟进攻方完全相反，前排是站在左边；
    传入的阵容的位置一定要严格按照顺序
    :param my_hero_pool: 自己的英雄池， eg. ["骨王", "小黑", "巨魔", "幻刺", "白虎", "幻刺", "天怒"]
    :param lineup1: ["骨王", "", "", "幻刺", "白虎"]
    :param lineup2: ["潮汐", "全能", "", "巫医", ""]
    :param lineup3: ["末日", "军团", "", "小黑", ""]
    :param ignore_hero_pool: 忽略英雄池给出阵容破解推荐
    :return:
    """
    guessed_lineup = []

    """
    !!!!!
    !!!!!  进攻方也需要剔除重复的英雄!!!
    !!!!!
    """

    # 获得明面上的防守方英雄
    known_hero = [i for i in lineup1 if i]
    known_hero += [i for i in lineup2 if i]
    known_hero += [i for i in lineup3 if i]
    print("known_hero", known_hero)

    # 只要猜出两队的防守阵容，就保存这个防守阵容
    # 以第一队作为参考
    lineups1 = get_guess_lineup(lineup1)
    # 以第二队作为参考
    lineups2 = get_guess_lineup(lineup2)
    # 以第三队作为参考
    lineups3 = get_guess_lineup(lineup3)

    # 排列组合出没有重复英雄的阵容
    # 第一二三队做排列组合
    for item1 in lineups1:
        hidden1, defend1, attack1, rate1 = item1[0], item1[1], item1[2], item1[3]
        # 保存当前组合的合格猜测阵容
        # 阵容的数据结构为元组，保证不可变和顺序性
        # 样式: [((攻击阵容), (防守阵容), 胜率)), ...x2]
        # 当前的排列组合里，已经出现的防守阵容和攻击阵容里的英雄
        current_defend_pool = known_hero

        # 在不忽略英雄池的情况下，如果破解阵容的英雄不在池子里，直接跳过
        if not ignore_hero_pool and not is_subset(attack1, my_hero_pool):
            continue
        # 隐藏阵容不能出现在当前的防守池子中(不能有重复英雄), 攻击阵容也不能重复(第一队的攻击阵容肯定不会重复)
        if has_common_element(hidden1, current_defend_pool):
            continue
        # 猜测的隐藏英雄加入当前出现的英雄池子
        current_defend_pool += hidden1

        # 跟第二队做匹配 - 嵌套
        for item2 in lineups2:
            current_defend_pool2 = copy.deepcopy(current_defend_pool)
            current_attack_pool2 = copy.deepcopy(attack1)
            hidden2, defend2, attack2, rate2 = item2[0], item2[1], item2[2], item2[3]
            if not ignore_hero_pool and not is_subset(attack2, my_hero_pool):
                continue
            if has_common_element(hidden2, current_defend_pool2) or has_common_element(attack2, current_attack_pool2):
                continue
            current_defend_pool2 += hidden2
            current_attack_pool2 += attack2

            # 跟第三队做匹配 - 嵌套
            inner_flag = False  # 如果第三队有破解阵容，则在第三队里添加破解阵容，否则就在第二队里添加破解阵容
            for item3 in lineups3:
                current_defend_pool3 = copy.deepcopy(current_defend_pool2)
                current_attack_pool3 = copy.deepcopy(current_attack_pool2)
                hidden3, defend3, attack3, rate3 = item3[0], item3[1], item3[2], item3[3]
                if not ignore_hero_pool and not is_subset(attack3, my_hero_pool):
                    continue
                if has_common_element(hidden3, current_defend_pool3) or has_common_element(attack3, current_attack_pool3):
                    continue
                inner_flag = True
                guessed_lineup.append([
                    (tuple(attack1), tuple(defend1), rate1),
                    (tuple(attack2), tuple(defend2), rate2),
                    (tuple(attack3), tuple(defend3), rate3)])
            if not inner_flag:
                guessed_lineup.append([
                    (tuple(attack1), tuple(defend1), rate1),
                    (tuple(attack2), tuple(defend2), rate2)])

        # 跟第三队做匹配 - 嵌套
        for item3 in lineups3:
            current_defend_pool3 = copy.deepcopy(current_defend_pool)
            current_attack_pool3 = copy.deepcopy(attack1)
            hidden3, defend3, attack3, rate3 = item3[0], item3[1], item3[2], item3[3]
            if not ignore_hero_pool and not is_subset(attack3, my_hero_pool):
                continue
            if has_common_element(hidden3, current_defend_pool3) or has_common_element(attack3, current_attack_pool3):
                continue
            guessed_lineup.append([
                (tuple(attack1), tuple(defend1), rate1),
                (tuple(attack3), tuple(defend3), rate3)])

    # 第二三队做排列组合
    for item2 in lineups2:
        hidden2, defend2, attack2, rate2 = item2[0], item2[1], item2[2], item2[3]
        current_defend_pool = known_hero
        if not ignore_hero_pool and not is_subset(attack2, my_hero_pool):
            continue
        if has_common_element(hidden2, current_defend_pool):
            continue
        current_defend_pool += hidden2

        # 跟第三队做匹配 - 嵌套
        for item3 in lineups3:
            current_defend_pool3 = copy.deepcopy(current_defend_pool)
            current_attack_pool3 = copy.deepcopy(attack2)
            hidden3, defend3, attack3, rate3 = item3[0], item3[1], item3[2], item3[3]
            if not ignore_hero_pool and not is_subset(attack3, my_hero_pool):
                continue
            if has_common_element(hidden3, current_defend_pool3) or has_common_element(attack3, current_attack_pool3):
                continue
            guessed_lineup.append([
                (tuple(attack2), tuple(defend2), rate2),
                (tuple(attack3), tuple(defend3), rate3)])

    return guessed_lineup


def crack_arena_lineup(my_hero_pool: list, defend_lineup: list, ignore_hero_pool=False):
    """
    根据自己英雄池返回 <普通竞技场> 破解阵容
    :param my_hero_pool: 自己的英雄池
    :param defend_lineup: 防守方的阵容
    :param ignore_hero_pool: 忽视自己的英雄池，直接返回破解阵容
    :return:
    """
    result = {}
    heros = sort_defend_lineup(defend_lineup)
    print("对方阵容", heros)

    statement = """SELECT * FROM arena_data where defend1='{}' and defend2='{}' and defend3='{}' and defend4='{}' and defend5='{}'""".format(
        heros[0], heros[1], heros[2], heros[3], heros[4]
    )
    attack_lineups = HeroProfile().match_cracked_lineup(statement)
    if attack_lineups:
        for cracked_lineup in attack_lineups:
            lineup = [i for i in cracked_lineup[1:6]]
            lineup = sort_defend_lineup(lineup)
            rate = cracked_lineup[11]

            has_matched_hero = True
            for hero in lineup:
                if hero not in my_hero_pool:
                    has_matched_hero = False
                    break
            if ignore_hero_pool:
                result = {
                    "破解阵容": lineup,
                    "胜率": rate
                }
            elif has_matched_hero:
                result = {
                    "破解阵容": lineup,
                    "胜率": rate
                }
    return result


def generate_latest_attack_lineup():
    """
    根据最新的竞技场对阵数据Excel生成攻击方的阵容(防守方的破解阵容);
    文件保存到sqlite3;
    防守方的数据在保存到数据库之前，必须按照英雄的站位顺序排列好;
    :return:
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
            defends = sort_defend_lineup(defends)
            attacks = item.get("attack").split(",")
            rate = item.get("rate")
            if len(attacks) < 5 or len(defends) < 5:
                continue
            data = attacks + defends + [rate]
            print('data', data)
            HeroProfile().insert(data)

    print("生成破解阵容的数据完毕，保存到了数据库")


def crack_arena_lineup_entry(defend_lineup: list):
    # 获取普通竞技场的破解阵容
    print("普通竞技场的阵容破解")
    return crack_arena_lineup(my_heros, defend_lineup)


def crack_peak_arena_lineup_entry(lineup1: list, lineup2: list, lineup3: list):
    # 获取巅峰竞技场的破解阵容
    print("巅峰竞技场的阵容破解")
    result = []
    # lineup1 = ["骨王", "", "火猫", "", "圣堂"]
    # lineup2 = ["潮汐", "全能", "", "", "舞姬"]
    # lineup3 = ["末日", "", "流浪", "", "白虎"]
    cracked_lineups = crack_peak_arena_lineup(my_heros, lineup1, lineup2, lineup3, False)
    for item in cracked_lineups:
        # [((攻击阵容), (防守阵容), 胜率)), ... x2]
        res_str = ""
        inner_res = []
        for index, value in enumerate(item):
            res_str += "{}队: 进攻: {}, 防守: {}, 胜率: {}\n".format(index + 1, sort_defend_lineup(list(value[0])), value[1], value[2])
            inner_res.append("{}队: 进攻: {}, 防守: {}, 胜率: {}".format(index + 1, sort_defend_lineup(list(value[0])), value[1], value[2]))
        result.append(inner_res)
        res = """
===============================
{}===============================""".format(res_str)
        # print(res)
    print("当前阵容的破解数量为:{}".format(len(cracked_lineups)))
    return result
