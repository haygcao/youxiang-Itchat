# coding=utf-8


def format_fen(value):
    value = int(value)
    return "{:.2f}".format(value / 100)


def format_price(value):
    return round(float(value), 2)


def clamp_min(value, minimum=0):
    return max(value, minimum)
