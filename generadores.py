# def my_gen():
#     a = 1
#     yield a

#     a = 2
#     yield a

#     a = 3
#     yield a


# my_first_gen = my_gen()

# print(next(my_first_gen))


def even_numbers():
    for i in range(101):
        if i % 2 == 0:
            print(i)


even_numbers()
