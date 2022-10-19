import time


class ParseFlanc:

    def __init__(self):
        self.dict_20_flance = {}
        self.dict_30_flance = {}

    def start_parse_flance(self, list_for_parse=[]):
        _list = list_for_parse[1].split()
        shina_all = "".join([i for i in _list if "/" in i])

        for i in _list:
            if "x" in i and "-" in i:
                if list_for_parse[1].count("/") == 1:
                    self.size_flance_too(i, shina_all, list_for_parse)
                if list_for_parse[1].count("/") == 2:
                    self.size_flance_troynik(i, shina_all, list_for_parse)

            if "x" in i and "-" not in i:
                self.size_flance(i, shina_all, list_for_parse)
        return [self.dict_20_flance, self.dict_30_flance]

    def size_flance_troynik(self, size_str, shina, list_for_parse):
        shina = shina.split("/")
        size = size_str.replace("(", "").replace(")", "").split("-")
        for i in size:
            if "x" in i and "Ф" not in i:
                size[size.index(i)] = self.sort_size(i)
        size1 = [shina[0], size[0], list_for_parse[-3]]
        size2 = [shina[2], size[0], list_for_parse[-3]]
        size3 = [shina[1], size[1], list_for_parse[-3]]
        self.list_into_dict(size1)
        self.list_into_dict(size2)
        self.list_into_dict(size3)

    def size_flance(self, size_str, shina, list_for_parse):
        size = self.sort_size(size_str)
        xlistForCount1 = [shina.split("/")[0], size, list_for_parse[-3]]
        xlistForCount2 = [shina.split("/")[1], size, list_for_parse[-3]]
        self.list_into_dict(xlistForCount1)
        self.list_into_dict(xlistForCount2)

    def size_flance_too(self, size_str, shina, list_for_parse):
        size = size_str.replace("(", "").replace(")", "").split("-")
        for i in size:
            if "x" in i:
                size[size.index(i)] = self.sort_size(i)
        size1 = [shina.split("/")[0], size[0], list_for_parse[3]]
        size2 = [shina.split("/")[1], size[1] if "=" not in size[1] else size[0], list_for_parse[3]]
        self.list_into_dict(size1)
        self.list_into_dict(size2)

    def sort_size(self, size_str):
        size = sorted(size_str.split("x"), key=int)
        return "x".join(size)

    def list_into_dict(self, lst):
        if "ш20" == lst[0]:
            self.shina20_in_dict(lst)
        if "ш30" == lst[0]:
            self.shina30_in_dict(lst)

    def shina20_in_dict(self, lst):
        if self.dict_20_flance.get(lst[1]):
            self.dict_20_flance[lst[1]] += lst[2]
        else:
            self.dict_20_flance[lst[1]] = lst[2]

    def shina30_in_dict(self, lst):
        if self.dict_30_flance.get(lst[1]):
            self.dict_30_flance[lst[1]] += lst[2]
        else:
            self.dict_30_flance[lst[1]] = lst[2]


parse_flance_fasonka = ParseFlanc()
parse_flance = ParseFlanc()


def count_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print(time.time() - start_time)

    return wrapper
