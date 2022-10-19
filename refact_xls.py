import pandas as pd
from pasre_flance import parse_flance, parse_flance_fasonka


def refactXls(ws):
    countfinal = 1
    listFlances = []
    listFlancesFasonka = []
    nameClient = []
    check_list = []
    b = False
    for item_xls in ws.iter_rows(values_only=True):
        if b:
            listForParse = join_to_list(item_xls)
            check_list.append(listForParse)

            if isinstance(listForParse[1], str):
                if "/" in listForParse[1] and ("x" in listForParse[1] or "Ф" in listForParse[1]):
                    if "Воздуховод" in listForParse[1] and "L=1250" in listForParse[1]:
                        listFlances = parse_flance.start_parse_flance(listForParse)
                    else:
                        listFlancesFasonka = parse_flance_fasonka.start_parse_flance(listForParse)
                if "Заглушка" in listForParse[1]:
                    x = []
                    for i in listForParse[1].split():
                        if isinstance(i, str) and i in ("ш20", "ш30", "у25", "отб.", "отб"):
                            x.append(i + "/-")
                        else:
                            x.append(i)
                    listForParse[1] = " ".join(x)
                    listFlancesFasonka = parse_flance_fasonka.start_parse_flance(listForParse)

        if "№ сч" in item_xls:
            nameClient = name_account(item_xls)

        if "В производство" in item_xls:
            b = True
        if "Итого" in item_xls:
            countfinal -= 1
            if countfinal < 0:
                break

    b = False
    for index, item in enumerate(check_list):
        if len(check_list[index]) > 6:
            count = len(check_list[index])
            while count > 6:
                check_list[index][1] = f"{str(check_list[index][1])}   ***{str(check_list[index].pop())}***"
                count -= 1
        if len(item) < 6:
            while len(item) < 6:
                check_list[index].append(0)

    dict_pandas = {}
    for item_xls in range(max(len(i) for i in check_list)):
        time_list = []

        for j in range(1, len(check_list[1:])):
            time_list.append(check_list[j][item_xls])
            dict_pandas[check_list[0][item_xls]] = time_list
    df_Voz_d = df_fix_view(pd.DataFrame(listFlances, index=["20", "30"]))
    df_fasonka = df_fix_view(pd.DataFrame(listFlancesFasonka, index=["20", "30"]))


    df = pd.DataFrame(dict_pandas)
    parse_flance_fasonka.dict_30_flance = {}
    parse_flance_fasonka.dict_20_flance = {}
    parse_flance.dict_20_flance = {}
    parse_flance.dict_30_flance = {}

    return [df, df_Voz_d, df_fasonka, nameClient]


def df_fix_view(df):
    df = df.T
    df = df.fillna(0)
    df = df.astype(int)
    return df


def join_to_list(lst):
    listForParse = []
    for item in lst:
        if item:
            listForParse.append(item)
    return listForParse


def name_account(lst):
    name_Client = []
    for item in lst:
        if item:
            if "Ном." not in item and "№ сч" not in item:
                name_Client.append(item)
    return name_Client

