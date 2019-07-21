##############------2 chili-----------#################
#  Given a list of numbers and calculate the sum ofe  #
#  all the number can be produced to 10               #
#######################################################

# def sum_of_product_10(intList):
#     tong = 0
#     for i in intList:
#         if (10 % i ==0):
#             tong=i+tong
#     return tong
##############------3 chili-----------#################
#  Given 2 strings, determines if letters from one    #
#  appear in the other                                #
#######################################################
def check_if_letters_are_duplicated_in_two_strings (s1,s2):
    letters = set()  # cấu trúc dữ liệu chỉ cho phép tồn taij phần tử không trùng nhau
    for i in s1:
         for r in s2:
            if i == r:
                letters.add(i)
    return letters


##############------4 chili-----------#################
#  Given a list of numbers and determines if all the  #
#  numbers are different from each other              #
#######################################################

##############------5 chili-----------#################
#  Given a list of numbers and find the max of the    #
#  sum of any sequence inside                         #
#######################################################


#-------------------------------------------------------
s1 = 'tilytrant'
s2 = 'tilyt'
## Comment out - ctrl + / - lam dong code bi xam di, khong execute
# print(sum_of_product_10(intList))
# tily de thuong
print (check_if_letters_are_duplicated_in_two_strings(s1,s2))