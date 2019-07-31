def palindrome(chuoi):
    reverse = ''        # --->  khởi tạo biến lưu giá trị chuỗi đảo ngược
    dodai = len(chuoi)  # ---> tính độ da
    for i in range(dodai - 1, -1, -1):
        reverse += chuoi[i]
    return reverse == chuoi

"""
def: từ khóa để định nghĩa 1 hàm (define a function)
palindrome(): tên hàm - tùy theo mục đích sẽ đặt tên, không được bắt đầu bằng số
chuoi: biến (aka argument) truyền vào hàm

range(start, end, step): 
- bắt đầu với start (giá trị start phải tồn tại) 
- kết thúc tại giá trị end - 1 => end có thể là giá trị không tồn tại trong chuỗi
- step: dương là tăng dần, âm là giảm (đi lùi)

reverse += chuoi[i] : phép cộng chuỗi, tương đương reverse = reverse + chuoi[i].
Giá trị sau khi cộng sẽ được gán lại vào reverse.
* Cộng chuỗi tương đương cộng số.

return: cú pháp trả về giá trị của một hàm. Cần thiết cho những trường hợp ta sử dụng giá trị của hàm
này cho một hàm khác. Nếu không có return, kết quả của bất kì phép toán nào trong hàm cũng không sử dụng lại được

reverse == chuoi: phép so sánh, khi chạy code, nó sẽ tự thực hiện so sánh và cho ra kết quả True/False
"""