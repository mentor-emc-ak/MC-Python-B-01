my_list = [1, 2, 3, 4, 5]

# another_list = []

# for num in my_list:
#     if num % 2 != 0:
#         another_list.append(num * 2)

# print(another_list)


multipled_list = [num * 2 for num in my_list if num % 2 != 0]
print(multipled_list)

# dict comprehension

my_dict = {num: num * 2 for num in my_list}
print(my_dict)
