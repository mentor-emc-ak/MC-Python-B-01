# our check decorator function
def only_numbers(fn):
    def inner_method(*args, **kwargs):
        santized_args = []
        for arg in args:
            if isinstance(arg, (int, float)):
                santized_args.append(arg)

        return fn(*santized_args, **kwargs)

    return inner_method


@only_numbers
def add_three_numbers(num1, num2, num3):
    return num1 + num2 + num3

three_value = add_three_numbers(12, 77, '23', 34, 'dfsdf')
print(three_value)


@only_numbers
def sum_of_numbers(*args, **kwargs):
    total = 0
    for num in args:
        total += num
    return total

value = sum_of_numbers(12, 77, 23, 54, 77, 'sdf', 'sdfds')

print(value)





