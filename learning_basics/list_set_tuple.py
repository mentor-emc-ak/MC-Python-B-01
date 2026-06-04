# # Creating a List
# a = [1, 2, 3, 'Python', 3]

# # Accessing elements by indexing
# print(a[0]) 
# print(a[-1]) 

# # Modifying an element
# a[1] = 'Updated'
# print(a)  

# # Appending an element
# a.append(4)

# # Removing an element
# a.remove(3)

# # List slicing
# print(a[1:3])


# # Creating a Set
# s = {1, 2, 3, 'Python', 3}
# print(s) 

# # Adding elements
# s.add(4)

# # Removing elements
# s.remove(3)  # KeyError if the element is not present

# # Accessing elements (No indexing because it is unordered)
# for element in s:
#     print(element)

# set_converted = list(s)
# print("this is set value", set_converted[0])



# # Creating a Tuple
# tup = (1, 2, 3, 'Python', 3)

# # Accessing elements by indexing
# print(tup[0])
# print(tup[-1])

# # Tuple slicing
# print(tup[1:4])

# # Attempting to modify a tuple (Raises TypeError)
# # tup[1] = 'Updated'  # Uncommenting this will raise an error



# # Arithmetic Operations

# a = 1
# b = 2

# print(a + b)  # Addition
# print(a - b)  # Subtraction
# print(a * b)  # Multiplication
# print(a / b)  # Division
# print(a % b)  # Modulus

# # Comparison Operators

# print(a == b)  # Equal to
# print(a != b)  # Not equal to
# print(a > b)   # Greater than
# print(a < b)   # Less than
# print(a >= b)  # Greater than or equal to
# print(a <= b)  # Less than or equal to

# # Logical Operators

# print(a > 0 and b > 0)  # Logical AND true and true = true | false and true = false | true and false = false | false and false = false
# print(a > 0 or b < 0)   # Logical OR true or true = true | false or true = true | true or false = true | false or false = false
# print(not (a > 0))      # Logical NOT true = false | false = true

# print((a > 0 and b < 0) or (a < 0 or (a == 0)))  # Logical AND and OR combined
# #      true             or (false or false)


# number = -2

# # 15 % 2 = 1
# # 14 % 2 = 0

# if number == 0:
#     print("This Neither Even Nor Odd")
# elif number < 0:
#     print("Negative")
# elif (number % 2) == 0:
#     print("Even")
# else:
#     print("Odd")



# # Using the 'in' operator to check for membership

# programming_languages = ['css', 'html', 'js', 'react', 'Pythn', 'ts', 'node', 'express', 'golang']
# #                         0      1       2     3        4         5      6        7         8

# programming_languages[4] = 'Python'

# # [start:stop:step]
# print(programming_languages[0:5:2])  # Slicing the list to get the first five elements

# # for example i need from 1 to 5 but excluding 4 na how can i do that  ?
# for i in range(6):
#     if i != 4:
#         print(programming_languages[i])

 
# my_name = 'akhshy'
# print(my_name.lower())  # Convert to lowercase 

# upper_case_programming_languages = []
# for language in programming_languages:
#     upper_case_programming_languages.append(language.upper())  # Convert each language to uppercase and add to the new list

# print(upper_case_programming_languages)

# print(my_name[0:7:2])

# print(my_name[::-1])

# print(programming_languages)
# print(', '.join(programming_languages))

# print(my_name.split('h'))

# print(f'My name is {my_name.capitalize()} and I am learning Python.')
# print(f'My name is {my_name.upper()} and I am learning Python.')
# print('My name is' + ' ' + my_name.upper() + ' ' + 'and I am learning Python.')


# print(f"My name is \"{my_name.capitalize()}\" and I am learning Python.")

# print("""My name is Akhshy \n I want to learn Python""")


# print('Hello, World!')  # This is a comment

# x = 1
# y = []

# if y == 0:
#         print("Cannot divide by zero.")
# elif type(y) == str:
#     print("Cannot divide by string.")
# else:
#     print("Result of x divided by y is: ", x / y)
#     print(x/y)


# try:
#     print("this time x is ", x)
#     print("this time y is ", y)


#     if y == 0:
#         print("Cannot divide by zero.")
#     else:
#         print("Result of x divided by y is: ", x / y)
#         print(x/y)

# except Exception as e:
#     print(f"An error occurred: {e}")
#     print("Please check your inputs and try again.")

# finally:
#     print("This will always execute regardless of whether an error occurred or not.")



# print("This will still execute even if there was an error.")


# set builtin methods

x = {1, 2, 3, 'Python', 3}
y = {2, 3, 5}
print(x)  # Output: {1, 2, 3, 'Python'}

x.add(4)  # Adding an element to the set
print(x)  # Output: {1, 2, 3, 'Python', 4}

x.remove(2)  # Removing an element from the set
print(x)  # Output: {1, 3, 'Python', 4}

x.remove(5)  # Attempting to remove an element that does not exist (raises KeyError)

x.discard(5)  # Attempting to discard an element that does not exist (does not raise an error)
print(x)  # Output: {1, 3, 'Python', 4}

print(x.union(y))  # Output: {1, 2, 3, 4, 5, 'Python'}
print(x.intersection(y))  # Output: {2, 3}
print(x.difference(y))  # Output: {1, 4, 'Python'}


print(x.copy())  # Output: {1, 3, 'Python', 4}


# dict builtin methods
my_dict = {
    'name': 'Akhshy',
    'age': 25,
    'city': 'New York'
}

print(my_dict) # Output: {'name': 'Akhshy', 'age': 25, 'city': 'New York'}
print(my_dict['name'])  # Output: 'Akhshy'
print(my_dict['marriage'])  # KeyError: 'marriage' (because the key does not exist in the dictionary)
print(my_dict.get('age'))  # Output: 25
print(my_dict.get('marriage'))  # Output: None (because the key does not exist in the dictionary)

print(my_dict.keys())  # Output: dict_keys(['name', 'age', 'city'])
print(my_dict.values())  # Output: dict_values(['Akhshy', 25, 'New York'])
print(my_dict.items())  # Output: dict_items([('name', 'Akhshy'), ('age', 25), ('city', 'New York')])

my_dict['age'] = 26  # Updating the value of an existing key
my_dict.update({'age': 26, 'marriage': 'Single'})  # Updating existing key and adding a new key
print(my_dict)  # Output: {'name': 'Akhshy', 'age': 26, 'city': 'New York', 'marriage': 'Single'}


# tuple builtin methods
t = (10, 20, 30, 40, 50, 60, 70, 50, 90, 50)

print(t.count(50))  # Output: 3 (number of occurrences of 50 in the tuple)
print(t.index(30))  # Output: 2 (index of the first occurrence of
print(t.index(50))  # Output: 4 (index of the first occurrence of 50 in the tuple)

t[9] = 100  # TypeError: 'tuple' object does not support item assignment (because tuples are immutable)

try:
    t[9] = 100  # Attempting to modify a tuple (raises TypeError)
except Exception as e:
    print(f"An error occurred: {e}")
