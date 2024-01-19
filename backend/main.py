import flask


from logic.xbb import get_hero, generate_latest_attack_lineup, crack_arena_lineup_entry, crack_peak_arena_lineup_entry

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
    crack_arena_lineup_entry()
    # 巅峰竞技场
    crack_peak_arena_lineup_entry()
