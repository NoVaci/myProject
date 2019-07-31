# -*- coding: utf-8 -*-
can = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
giap = ['Tý', 'Sửu', 'Dần', 'Mẹo', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

can_chi = {1: 'Giáp Tý', 2: 'Ất Sửu'}
# 1924 Giáp Tý
def tinhNamConGiap(year):
    if year < 1984:
        gap = (year - (1984 - 60*33)) % 60
    else :
        gap = (year - 1984) % 60
    return can_chi[gap]
print(tinhNamConGiap(1925))