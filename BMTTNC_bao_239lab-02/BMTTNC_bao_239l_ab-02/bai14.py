def tao_tuple_tu_list(lst):
    return tuple(lst)
input_list = input("Nhap danh cach cac so, ach nhau bang dau phat")
numbers = list(map(int,input_list.split(',')))
my_tuple = tao_tuple_tu_list(numbers)
print("List:",numbers)
print("Tuple tu List",my_tuple)