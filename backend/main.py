import json

from flask import Flask, request

from logic.xbb import get_hero, generate_latest_attack_lineup, crack_arena_lineup_entry, crack_peak_arena_lineup_entry

app = Flask(__name__)


@app.route("/crack_arena_lineup", methods=['GET', 'POST'])
def arena_lineup():
    """
    普通竞技场
    :return:
    """
    if request.method == 'POST':
        try:
            body = request.data
            body = json.loads(body)
            defend_lineup = [body["lineup1"], body["lineup2"], body["lineup3"], body["lineup4"], body["lineup5"]]
            return crack_arena_lineup_entry(defend_lineup)
        except Exception as e:
            err_msg = "普通竞技场 error:{}".format(e.args[0])
            print(err_msg)
            return err_msg
    else:
        return "请发POST请求获取数据"


@app.route("/crack_peak_arena_lineup", methods=['GET', 'POST'])
def peak_arena_lineup():
    """
    巅峰竞技场
    :return:
    """
    if request.method == 'POST':
        try:
            body = request.data
            body = json.loads(body)
            return crack_peak_arena_lineup_entry(body["lineup1"], body["lineup2"], body["lineup3"])
        except Exception as e:
            err_msg = "普通竞技场 error:{}".format(e.args[0])
            print(err_msg)
            return err_msg
    else:
        return "请发POST请求获取数据"


if __name__ == '__main__':
    # 从Excel里获取最新的英雄数据，检查表格里的异常数据并修改
    # get_hero()
    # 生成破解整容
    # generate_latest_attack_lineup()
    # HeroProfile().create_table()
    # HeroProfile().clear_table("arena_data")
    # HeroProfile().get_all("arena_data")
    # HeroProfile().execute("drop table hero;")
    # HeroProfile().execute("DELETE FROM hero WHERE id = 2;")

    # 普通竞技场
    # crack_arena_lineup_entry()
    app.run("0.0.0.0", port=8035, debug=True)
