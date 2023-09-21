from icecream import ic
list_1 = ['a', 'b', 'c']
list_2 = list_1
list_3 = list(list_1)

ic(list_1)
ic(list_2)
ic(list_3)

ic(list_1 == list_2)
ic(list_2 == list_3)

ic(list_1 is list_2)
ic(list_2 is list_3)

ic(id(list_1))
ic(id(list_2))
ic(id(list_3))