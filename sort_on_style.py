from PySide6.QtGui import QColor


def sort_item_vent(name):
    match name.split()[0]:
        case "Воздуховод":
            return vozd_vod(name)
    if "x" in name:
        if not "-" in name:
            return fasonka_rd(name)
        if name.count("x") > 1:
            return fasonka_rd(name)

        else:
            return fasonka(name)
    if "Ф" in name:
        return fasonka_round(name)


def vozd_vod(name):
    if ("L=1250" in name and "x" in name) or "спирал" in name:
        return QColor("#C3C2BC")
    return QColor("green")


def fasonka_rd(name):
    return QColor("#010B65")


def fasonka(name):
    return QColor("blue")


def fasonka_round(name):
    return QColor("#593000")
