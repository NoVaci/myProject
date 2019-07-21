##############------2 chili-----------#################
#  Given a list of numbers and calculate the sum ofe  #
#  all the number can be produced to 10               #
#######################################################

def sum_of_product_10(intList):
    tong = 0
    for i in intList:
        if (10 % i ==0):
            tong=i+tong
    return tong
##############------3 chili-----------#################
#  Given 2 strings, determines if letters from one    #
#  appear in the other                                #
#######################################################

##############------4 chili-----------#################
#  Given a list of numbers and determines if all the  #
#  numbers are different from each other              #
#######################################################

##############------5 chili-----------#################
#  Given a list of numbers and find the max of the    #
#  sum of any sequence inside                         #
#######################################################


#-------------------------------------------------------
intList = [2,3,4,5,1,7,8,10]
## Comment out - ctrl + / - lam dong code bi xam di, khong execute
print(sum_of_product_10(intList))
# tily de thuong
