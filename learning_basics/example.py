# a = 10
# b = 20

# print("The value of a is:", a)
# print("The value of b is:", b)

# print(a + b)

# x = 10
# y = 20

# print("The value of x is:", x)
# print("The value of y is:", y)

# print(x + y)

# s = 10
# d = 20

# print("The value of s is:", s)
# print("The value of d is:", d)

# print(s + d)

# def add_two_numbers(num1, num2):
#     return num1 + num2

# add_two_numbers(122, 7897, 66)


# def divide_two_numbers(num1, num2):
#     if type(num1) != int:
#         return "num1 should be integers."
#     elif type(num2) != int:
#         return "num2 should be integers."
#     elif num2 == 0:
#         return "num2 should not be zero."

#     print("The value of num1 is:", num1)
#     print("The value of num2 is:", num2)

#     try:
#         value = num1 / num2
#     except Exception as e:
#         return f"An error occurred: {e}"

#     return f"The division of num1 by num2 is: {value}."

# value = divide_two_numbers(122, 0)

# print(value)

#                 *args and **kwargs
# def sum_of_numbers(num1, num2):
#     if type(num1) != int:
#         return "num1 should be integers."
#     elif type(num2) != int:
#         return "num2 should be integers."

#     print("The value of num1 is:", num1)
#     print("The value of num2 is:", num2)

#     try:
#         value = num1 + num2
#     except Exception as e:
#         return f"An error occurred: {e}"

#     return f"The sum of num1 and num2 is: {value}."


# print(sum_of_numbers(122, 7897, 2323, 23))


# def sum_of_numbers(*args, **kwargs):
#     total = 0
#     for num in args:
#         total += num
#     return total
# print(sum_of_numbers(12, 77, 23, 54, 77, 34, 56.77))

value = sum([1, 2, 3, 4, 5])

print(value)

# print(sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))


# add_10 = lambda x, y: x + y + 10

# # def add_10(x):
# #     return x + 10

# print(add_10(5, 5))





















