

def has_common_element(left_list, right_list):
    # 判断左边列表中的是否有至少一个元素在右边列表中
    return any(x in right_list for x in left_list)


def is_subset(left_list, right_list):
    # 判断左边的列表是否都在右边的列表中（即判断左边的列表是否是右边列表的子集）
    set1 = set(left_list)
    set2 = set(right_list)
    return set1.issubset(set2)
