import itertools
import time


# Brute force function
def try_password(password_set, string_typeset):
    start = time.time()
    chars = string_typeset
    attempts = 0
    for i in range(1, 9):
        for letter in itertools.product(chars, repeat=i):
            attempts += 1
            word = ''.join(letter)
            print(word)
            if word == password_set:
                print(word)
                end = time.time()
                distance = end - start
                return word, attempts, distance


password = input("Password >")
# Allowed characters
stringType = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()_-+=[{]}|:;'\",<.>/?"
word, tries, timeAmount = try_password(password, stringType)
print("Password %s in %s tries and %s seconds!" % (password, tries, timeAmount))
