# # Python interview practice prompts

# # Basics
# # 1. Reverse a string without using slicing.
# # 2. Check whether a string is a palindrome.
# # 3. Count vowels, consonants, digits, and spaces in a string.
# # 4. Remove duplicate characters from a string while keeping order.
# # 5. Find the second largest number in a list.


# a = 'hello world'

# # 1. Reverse a string without using slicing.
# def reverse_string(s):
#     reversed_str = ''
#     for char in s:
#         reversed_str = char + reversed_str
#     return reversed_str

# print(reverse_string(a))

# #Reverse a string using slicing.
# def reverse_string_slicing(s):
#     return s[::-1]
# print(reverse_string_slicing(a))

# #explain in simplest words possible s[::-1]
# # The expression s[::-1] is a slicing operation that creates a new string by taking all characters from the original string 's' but in reverse order. The first colon (:) indicates that we want to include all characters, and the -1 means we want to step through the string backwards, effectively reversing it. So, if s is "hello", s[::-1] will return "olleh".


# # 2. Check whether a string is a palindrome.
# b = 'racecar'
# def is_palindrome(s):
#     return s == s[::-1]

# #without slicing
# def is_palindrome_no_slicing(s):
#     left, right = 0, len(s) - 1
#     while left < right:
#         if s[left] != s[right]:
#             return False
#         left += 1
#         right -= 1
#     return True


# # 3. Count vowels, consonants, digits, and spaces in a string.
# def count_characters(s):
#     vowels = 'aeiouAEIOU'
#     counts = {'vowels': 0, 'consonants': 0, 'digits': 0, 'spaces': 0}

#     for char in s:
#         if char in vowels:
#             counts['vowels'] += 1
#         elif char.isalpha():
#             counts['consonants'] += 1
#         elif char.isdigit():
#             counts['digits'] += 1
#         elif char.isspace():
#             counts['spaces'] += 1

#     return counts


# # 4. Remove duplicate characters from a string while keeping order.
# s = 'hello world'
# def remove_duplicates(s):
#     seen = set()
#     result = []
#     for char in s:
#         if char not in seen:
#             seen.add(char)
#             result.append(char)
#     return ''.join(result)

# print(remove_duplicates(s))
# # why using set?
# # Using a set is efficient for checking if a character has already been seen because sets in Python have O(1) average time complexity for membership tests. This means that checking if a character is in the 'seen' set is very fast, even as the number of characters increases. By using a set, we can quickly determine whether to add a character to our result list without having to search through it, which would be less efficient.



# # Lists and Tuples
# # 6. Flatten a list of lists into a single list.

# nested_list = [[1, 2], [3, 4], [5, 6]]
# def flatten_list(nested_list):
#     flatten_list = []
#     for sublist in nested_list:
#         for item in sublist:
#             flatten_list.append(item)
#     return flatten_list

# print(flatten_list(nested_list))

# # 7. Find the most frequent element in a list.

# most_frequent_list = [1, 2, 3, 2, 4, 1, 2]
# def most_frequent(lst):
#     frequency = {}
#     for item in lst:
#         if item in frequency:
#             frequency[item] += 1
#         else:
#             frequency[item] = 1

#     most_frequent_item = None
#     max_count = 0
#     for item, count in frequency.items():
#         print(f"Item: {item}, Count: {count}")
#         if count > max_count:
#             max_count = count
#             most_frequent_item = item

#     return most_frequent_item

# print(most_frequent(most_frequent_list))


# # 8. Rotate a list to the right by k steps.
# rotate_list_example = [1, 2, 3, 4, 5]
# def rotate_list(lst, k):
#     k = k % len(lst)  # Handle cases where k is greater than list length
#     return lst[-k:] + lst[:-k]

# print(rotate_list(rotate_list_example, 2))

# # What does that mean lst[-k:] + lst[:-k]?
# # lst[-k:] gets the last k elements of the list.
# # lst[:-k] gets all elements except the last k elements.
# # Adding them together rotates the list to the right by k steps.

# # 9. Find the intersection of two lists without using set operations.
# intersection_list1 = [1, 2, 3, 4]
# intersection_list2 = [3, 4, 5, 6]
# def intersection(lst1, lst2):
#     result = []
#     for item in lst1:
#         if item in lst2 and item not in result:
#             result.append(item)
#     return result
# print(intersection(intersection_list1, intersection_list2))

# # 10. Swap every pair of adjacent elements in a list.
# swap_list = [1, 2, 3, 4, 5]
# def swap_adjacent(lst):
#     for i in range(0, len(lst) - 1, 2):
#         lst[i], lst[i + 1] = lst[i + 1], lst[i]
#     return lst
# print(swap_adjacent(swap_list))
# # explain the range(0, len(lst) - 1, 2)
# # The range(0, len(lst) - 1, 2) generates a sequence of indices starting from 0 up to len(lst) - 1, with a step of 2. This means it will give us the indices of the first element in each pair of adjacent elements. For example, if lst has 5 elements, the range will produce indices 0 and 2, which correspond to the pairs (lst[0], lst[1]) and (lst[2], lst[3]). This allows us to swap adjacent elements without going out of bounds.


# # Dictionaries and Sets
# # 11. Count the frequency of each word in a sentence.
# sentece = "hello world hello"
# def word_frequency(sentence):
#     frequency = {}
#     words = sentence.split()
#     print(f"Words: {words}")
#     for word in words:
#         if word in frequency:
#             frequency[word] += 1
#         else:
#             frequency[word] = 1
#     return frequency

# print(word_frequency(sentece))

# # 12. Group a list of words by their first letter.
# string_list = ["apple", "banana", "avocado", "grape", "blueberry"]
# def group_by_first_letter(words):
#     grouped = {}
#     for word in words:
#         first_letter = word[0]
#         if first_letter not in grouped:
#             grouped[first_letter] = []
#         grouped[first_letter].append(word)
#     return grouped

# print(group_by_first_letter(string_list))

# # 13. Find common keys between two dictionaries.
# dict1 = {'a': 1, 'b': 2, 'c': 3}
# dict2 = {'b': 3, 'c': 4, 'd': 5}
# def common_keys(d1, d2):
#     common = []
#     for key in d1:
#         if key in d2:
#             common.append(key)
#     return common

# print(common_keys(dict1, dict2))

# # 14. Remove duplicate values from a dictionary, keeping the first key for each value.
# dict_with_duplicates = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
# def remove_duplicate_values(d):
#     seen_values = set()
#     result = {}
#     for key, value in d.items():
#         if value not in seen_values:
#             seen_values.add(value)
#             result[key] = value
#     return result
# print(remove_duplicate_values(dict_with_duplicates))


# # 15. Check if two strings are anagrams using a dictionary.
# # Anagrams are words that contain the same characters in the same quantities but in a different order. example "listen" and "silent" are anagrams because they both contain the letters 'l', 'i', 's', 't', 'e', and 'n' in the same quantities, just arranged differently. To check if two strings are anagrams using a dictionary, we can count the frequency of each character in both strings and compare the counts.
# anagram_str1 = "listen"
# anagram_str2 = "silent"
# def are_anagrams(str1, str2):
#     if len(str1) != len(str2):
#         return False

#     char_count = {}

#     for char in str1:
#         char_count[char] = char_count.get(char, 0) + 1

#     for char in str2:
#         if char not in char_count or char_count[char] == 0:
#             return False
#         char_count[char] -= 1

#     return True
# #explain char_count.get(char, 0) + 1
# # The expression char_count.get(char, 0) retrieves the current count of the character 'char' from the dictionary 'char_count'. If 'char' is not already a key in the dictionary, it returns the default value of 0. Then, we add 1 to this count to account for the occurrence of 'char' in the string. This way, we can easily count the frequency of each character without having to check if the key exists in the dictionary first.
# #dry run the function with "listen" and "silent"
# # For "listen":
# # char_count = {}
# # 'l' -> char_count = {'l': 1}
# # 'i' -> char_count = {'l': 1, 'i': 1}
# # 's' -> char_count = {'l': 1, 'i': 1, 's': 1}
# # 't' -> char_count = {'l': 1, 'i': 1, 's': 1, 't': 1}
# # 'e' -> char_count = {'l': 1, 'i': 1, 's': 1, 't': 1, 'e': 1}
# # 'n' -> char_count = {'l': 1, 'i': 1, 's': 1, 't': 1, 'e': 1, 'n': 1}
# # For "silent":
# # 's' -> char_count = {'l': 1, 'i': 1, 's': 0, 't': 1, 'e': 1, 'n': 1}
# # 'i' -> char_count = {'l': 1, 'i': 0, 's': 0, 't': 1, 'e': 1, 'n': 1}
# # 'l' -> char_count = {'l': 0, 'i': 0, 's': 0, 't': 1, 'e': 1, 'n': 1}
# # 'e' -> char_count = {'l': 0, 'i': 0, 's': 0, 't': 1, 'e': 0, 'n': 1}
# # 'n' -> char_count = {'l': 0, 'i': 0, 's': 0, 't': 1, 'e': 0, 'n': 0}
# # 't' -> char_count = {'l': 0, 'i': 0, 's': 0, 't': 0, 'e': 0, 'n': 0}
# # Since all counts are zero at the end, "listen" and "silent" are anagrams, and the function will return True.


# # Functions and Scope
# # 16. Accept any number of integers and return their average.in

# integers = [1, 2, 3, 4, 5]
# def average(*args):
#     if len(args) == 0:
#         return 0
#     return sum(args) / len(args)
# print(average(*integers))


# # 17. Show the difference between mutable and immutable arguments.
# # Mutable arguments (like lists and dictionaries) can be changed in place, meaning that if you pass a mutable object to a function and modify it, the changes will be reflected outside the function. Immutable arguments (like integers, floats, strings, and tuples) cannot be changed in place. If you try to modify an immutable object, a new object will be created instead.
# def modify_list(lst):
#     lst.append(4)  # This modifies the original list

# my_list = [1, 2, 3]
# modify_list(my_list)
# print(my_list)  # Output: [1, 2, 3, 4]

# def modify_string(s):
#      s += " world"
#      return s  # This creates a new string

# my_string = "hello"
# modify_string(my_string)
# print(modify_string(my_string))
# print(my_string)  # Output: "hello" (original string is unchanged)


# # 18. Write a closure that remembers how many times it has been called.
# def create_counter():
#     count = 0
#     def counter():
#         nonlocal count
#         count += 1
#         return count
#     return counter

# counter = create_counter()
# print(counter())  # Output: 1
# print(counter())  # Output: 2
# print(counter())  # Output: 3
# #define closure
# # A closure is a function that retains access to variables from its enclosing scope, even after the outer function has finished executing. In the example above, the inner function 'counter' is a closure because it has access to the 'count' variable defined in the outer function 'create_counter'. Each time 'counter' is called, it can modify and access the 'count' variable, allowing it to remember how many times it has been called. This is a powerful feature of closures, as it allows us to create functions with persistent state without using global variables or classes.

# # 19. Use default arguments safely.
# def append_to_list(value, lst=None):
#     if lst is None:
#         lst = []
#     lst.append(value)
#     return lst
# print(append_to_list(1))  # Output: [1]
# print(append_to_list(2))  # Output: [2] (not [1, 2])



# # 20. Write a decorator that prints execution time.
# import time
# def execution_time_decorator(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print(f"Execution time: {end_time - start_time} seconds")
#         return result
#     return wrapper

# @execution_time_decorator
# def example_function(n):
#     total = 0
#     for i in range(n):
#         total += i
#     return total


# one practical example of decorators
import time
def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper

@execution_time_decorator
def fibonacci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

print(fibonacci(30))  # This will print the first 30 numbers in the Fibonacci sequence along with the execution time.


# # Loops and Comprehensions
# # 21. Use a list comprehension to filter all odd numbers from a list.
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# odd_numbers = [num for num in numbers if num % 2 != 0]
# print(odd_numbers)  # Output: [1, 3, 5, 7, 9]

# # 22. Use a dictionary comprehension to square numbers from 1 to n.
# n = 5
# squares = {x: x**2 for x in range(1, n+1)}
# print(squares)  # Output: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
# #is x:x**2 lambda function?
# # No, x: x**2 is not a lambda function. It is a key-value pair in a dictionary comprehension. In this case, x is the key and x**2 is the value. A lambda function is an anonymous function defined using the lambda keyword, and it would look like this: lambda x: x**2. In the context of a dictionary comprehension, we are simply creating key-value pairs, not defining a function.


# # 23. Find the first non-repeating character in a string.
# non_repeating_string = "swiss"
# def first_non_repeating_character(s):
#     char_count = {}
#     for char in s:
#         char_count[char] = char_count.get(char, 0) + 1

#     for char in s:
#         if char_count[char] == 1:
#             return char
#     return None
# print(first_non_repeating_character(non_repeating_string))  # Output: 'w' (the first non-repeating character in "swiss")


# # 24. Print a multiplication table using nested loops. it takes 2 args, size of table and, table of digit, like table of 5 or 10 or 2.
# def multiplication_table(tableof, size=10):
#     for i in range(1, size + 1):

#         print(f"{tableof} x {i} = {tableof * i}")



# multiplication_table(5)
# # getting this output, which is correct, but explain the formatting in print(f"{i * j:4}", end=''):
# # The expression f"{i * j:4}" is a formatted string (f-string) that formats the product of i and j to be right-aligned within a field of 4 characters. The ":4" specifies that the output should take up at least 4 characters in width. If the product of i and j is less than 4 characters long, it will be padded with spaces on the left to ensure that it takes up 4 characters. The end='' argument in the print function prevents it from adding a newline after each print statement, allowing the products to be printed on the same line. After the inner loop finishes, print() is called without arguments to move to the next line for the next row of the multiplication table. This results in a neatly formatted multiplication table where each number is aligned in columns.
# #   1   2   3   4   5
# #    2   4   6   8  10
# #    3   6   9  12  15
# #    4   8  12  16  20
# #    5  10  15  20  25


# # 25. Generate the first n numbers of the Fibonacci sequence.

# def fibonacci(n):
#     sequence = []
#     a, b = 0, 1
#     for _ in range(n):
#         sequence.append(a)
#         a, b = b, a + b
#     return sequence
# #explain fibonacci sequence
# # The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, usually starting with 0 and 1. The sequence goes like this: 0, 1, 1, 2, 3, 5, 8, 13, 21, and so on. In the function above, we initialize two variables a and b to represent the two most recent numbers in the sequence. We then loop n times, appending the current value of a to the sequence list, and then update a and b to the next two numbers in the sequence. This way, we generate the first n numbers of the Fibonacci sequence efficiently.
# # _ in the loop is a common convention in Python to indicate that the loop variable is not going to be used. It is a placeholder that allows us to run the loop a specific number of times without needing to reference the loop variable itself. In this case, we just want to generate n numbers in the Fibonacci sequence, and we don't need to use the loop variable, so we use _ to indicate that it is intentionally unused.

# # Strings
# # 26. Count how many times each character appears in a string.
# count_string = "hello world"
# def character_count(s):
#     count = {}
#     for char in s:
#         count[char] = count.get(char,0)+1

#     return count

# print(character_count(count_string))

# # 27. Capitalize the first letter of every word without using title().

# def capitalize_words(s):
#     words = s.split()
#     print(f"Words: {words}")
#     capitalized_words = [word[0].upper() + word[1:] if word else '' for word in words]
#     return ' '.join(capitalized_words)

# print(capitalize_words(count_string))  # Output: "Hello World"

# # explain apitalized_words = [word[0].upper() + word[1:] if word else '' for word in words]
# # This is a list comprehension that iterates over each word in the 'words' list. For each 'word', it checks if the word is not empty (if word else ''). If the word is not empty, it takes the first character (word[0]), converts it to uppercase using upper(), and concatenates it with the rest of the word (word[1:]). If the word is empty, it simply returns an empty string. The result is a new list called 'capitalized_words' where each word has its first letter capitalized. Finally, we join the capitalized words back into a single string with spaces in between using ' '.join(capitalized_words).


# # 28. Check if one string is a rotation of another.
# def check_rotation(s1, s2):
#     if len(s1) != len(s2):
#         return False
#     print(f"s1 + s1: {s1 + s1}")
#     return s2 in s1 + s1
# print(check_rotation("hello", "lohel"))  # Output: True (because "lohel" is a rotation of "hello")
# print(check_rotation("hello", "world"))  # Output: False (because "world" is not a rotation of "hello")
# # explain s2 in s1 + s1?
# # This checks if s2 is a substring of s1 + s1. If s2 is a rotation of s1, then it will appear as a substring in the concatenated string s1 + s1.
# #how lohel is a rotation of hello?
# # "lohel" is a rotation of "hello" because if you take the string "hello" and rotate it to the left by 2 characters, you get "lohel". In other words, you can take the first two characters "he" from "hello" and move them to the end of the string, resulting in "lohel". This is why "lohel" is considered a rotation of "hello".


# # 29. Remove all punctuation from a string.
# import string
# def remove_punctuation(s):
#     return s.translate(str.maketrans('', '', string.punctuation))
# punctuated_string = "Hello, world! This is a test."
# print(remove_punctuation(punctuated_string))  # Output: "Hello world This is a test"


# # 30. Find the longest word in a sentence.

# def longest_word(sentence):
#     words = sentence.split()
#     longest = ''
#     for word in words:
#         if len(word) > len(longest):
#             longest = word
#     return longest

# print(longest_word("The quick brown fox jumps over the lazy dog"))  # Output: "jumps"


# # OOP Basics
# # 31. Create a BankAccount class with deposit, withdraw, and balance methods.

# class BankAccount:
#     def __init__(self, initial_balance=0):
#         self.__balance = initial_balance

#     def deposit(self,amount):
#         if amount>0:
#             self.__balance +=amount
#             print(f"Deposited: {amount}, New Balance: {self.__balance}")
#         else:
#             print("Deposit amount must be positive.")

#     def withdraw(self, amount):
#         if amount > self.__balance:
#             print("Insufficient funds.")
#         elif amount <= 0:
#             print("Withdrawal amount must be positive.")
#         else:
#             self.__balance -= amount
#             print(f"Withdrew: {amount}, New Balance: {self.__balance}")

#     def get_balance(self):
#         return self.__balance


# if __name__ == "__main__":
#     account = BankAccount(100)
#     account.deposit(50)  # Output: Deposited: 50, New Balance: 150
#     account.withdraw(30)  # Output: Withdrew: 30, New Balance: 120
#     print(account.get_balance())  # Output: 120

# # 32. Create a Student class with name, marks, and average_marks method.

# class Student:
#     def __init__(self, name, marks):
#         self.name = name
#         self.marks = marks

#     def average_marks(self):
#         if len(self.marks) == 0:
#             return 0
#         return sum(self.marks) / len(self.marks)


# # 33. Create a class hierarchy for Animal, Dog, and Cat.

# class Animal:
#     def __init__(self, name):
#         self.name = name

#     def speak(self):
#         raise NotImplementedError("Subclasses must implement this method")

# class Dog(Animal):
#     def speak(self):
#         return f"{self.name} says Woof!"

# class Cat(Animal):
#     def speak(self):
#         return f"{self.name} says Meow!"


# if __name__ == "__main__":
#     dog = Dog("Buddy")
#     cat = Cat("Whiskers")
#     print(dog.speak())  # Output: Buddy says Woof!
#     print(cat.speak())  # Output: Whiskers says Meow!

# # 34. Define __str__ and __repr__ clearly in a class.

# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def __str__(self):
#         return f"Point({self.x}, {self.y})"

#     def __repr__(self):
#         return f"Point(x={self.x}, y={self.y})"

# if __name__ == "__main__":
#     p = Point(1, 2)
#     print(str(p))  # Output: Point(1, 2)
#     print(repr(p)) # Output: Point(x=1, y=2)

# # 35. Use a property to protect a private attribute.
# class Temperature:
#     def __init__(self, celsius):
#         self._celsius = celsius

#     @property
#     def celsius(self):
#         return self._celsius

#     @celsius.setter
#     def celsius(self, value):
#         if value < -273.15:
#             raise ValueError("Temperature cannot be below absolute zero.")
#         self._celsius = value

# #what is this @celsius.setter?
# # The @celsius.setter is a decorator that defines the setter method for the 'celsius' property. It allows you to set the value of the 'celsius' attribute while also performing validation. In this case, it checks if the value being set is below absolute zero (-273.15 degrees Celsius) and raises a ValueError if it is. This way, we can protect the private attribute _celsius from being set to invalid values while still allowing controlled access through the property.


# # Iterators and Generators
# # 36. Write a generator that yields numbers from 1 to n.

# def number_generator(n):
#     for i in range(1, n + 1):
#         yield i

# next(number_generator(5))  # Output: 1
# next(number_generator(5))  # Output: 1 (because we are creating a new generator each time)
# # To use the generator properly, we should create an instance of it and then call next() on that instance:
# gen = number_generator(5)
# print(next(gen))  # Output: 1
# print(next(gen))  # Output: 2
# print(next(gen))  # Output: 3
# print(next(gen))  # Output: 4
# print(next(gen))  # Output: 5
# # If we call next() again after the generator is exhausted, it will raise a StopIteration exception:


# # 37. Write a generator that yields only even numbers from a list.

# def even_number_generator(lst):
#      for num in lst:
#         if num % 2 == 0:
#             yield num


# print(next(even_number_generator([1, 2, 3, 4, 5, 6]))) # Output: 2
# print(next(even_number_generator([1, 2, 3, 4, 5, 6])))  # Output: 2 (because we are creating a new generator each time)
# # To use the generator properly, we should create an instance of it and then call next() on that instance:
# even_gen = even_number_generator([1, 2, 3, 4, 5, 6])
# print(next(even_gen))  # Output: 2
# print(next(even_gen))  # Output: 4
# print(next(even_gen))  # Output: 6
# # If we call next() again after the generator is exhausted, it will raise a StopIteration exception:
# # print(next(even_gen))  # This will raise StopIteration because there are no more even numbers to yield.


# # 38. Create a custom iterator for a counte
# #how is it custom? # A custom iterator is an object that implements the iterator protocol, which consists of the __iter__() and __next__() methods. In the example below, we create a custom iterator called CounterIterator that yields numbers from 0 to n-1. This is custom because we are defining our own logic for how the iteration works, rather than using built-in iterators like lists or dictionaries.

# class CounterIterator:
#     def __init__(self, n):
#         self.n = n
#         self.count = 0

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.count < self.n:
#             current = self.count
#             self.count += 1
#             return current
#         else:
#             raise StopIteration



# def counter_iterator(n):
#     count = 0
#     while count < n:
#         yield count
#         count += 1
# counter_gen = counter_iterator(5)
# print(next(counter_gen))  # Output: 0
# print(next(counter_gen))  # Output: 1
# print(next(counter_gen))  # Output: 2
# print(next(counter_gen))  # Output: 3
# print(next(counter_gen))  # Output: 4


# # 39. Lazily read lines from a text file.
# def read_lines_lazy(file_path):
#     with open(file_path, 'r') as file:
#         for line in file:
#             yield line.strip()  # Yield each line without leading/trailing whitespace

# # read_lines= read_lines_lazy('test.txt')
# # print(next(read_lines))  # Output: First line of the file


# # 40. Compare an iterator and a generator in one small example.
# # An iterator is an object that implements the __iter__() and __next__() methods, while a generator is a special type of iterator that is defined using a function with the yield keyword. Here's a small example to compare them:
# # Using an iterator
# class CountIterator:
#     def __init__(self, n):
#         self.n = n
#         self.count = 0

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.count < self.n:
#             current = self.count
#             self.count += 1
#             return current
#         else:
#             raise StopIteration

# count_iter = CountIterator(5)
# print(next(count_iter))  # Output: 0
# print(next(count_iter))  # Output: 1
# # print(next(count_iter))  # Output: 2
# # print(next(count_iter))  # Output: 3
# # print(next(count_iter))  # Output: 4

# # Using a generator
# def count_generator(n):
#     count = 0
#     while count < n:
#         yield count
#         count += 1

# count_gen = count_generator(5)
# print(next(count_gen))  # Output: 0
# # print(next(count_gen))  # Output: 1
# # print(next(count_gen))  # Output: 2
# # print(next(count_gen))  # Output: 3
# # print(next(count_gen))  # Output: 4

# # Error Handling and Files
# # 41. Safely divide two numbers and handle ZeroDivisionError.

# def safe_divide(a, b):
#     try:
#         result = a / b
#         return result
#     except ZeroDivisionError:
#         return "Error: Cannot divide by zero."

# print(safe_divide(10, 2))  # Output: 5.0
# print(safe_divide(10, 0))  # Output: Error: Cannot divide

# # 42. Read a file and count the number of lines.
# def count_lines(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             print(f"Lines: {lines}")
#             return len(lines)
#     except FileNotFoundError:
#         return "Error: File not found."

# # print(count_lines('test.txt'))  # Output: Number of lines in the file or error message if file is not found.

# # 43. Handle missing keys in a dictionary gracefully.
# def get_value_safely(dictionary, key, default=None):
#     return dictionary.get(key, default)

# my_dict = {'a': 1, 'b': 2}
# print(get_value_safely(my_dict, 'a'))  # Output: 1
# print(get_value_safely(my_dict, 'c'))  # Output: None (default value)
# print(get_value_safely(my_dict, 'c', 'Key not found'))  # Output: Key not found (custom default value)
# #explain dictionary.get(key, default)
# # The dictionary.get(key, default) method is used to retrieve the value associated with a specified key from a dictionary. If the key exists in the dictionary, it returns the corresponding value. If the key does not exist, it returns the default value provided as the second argument. If no default value is specified, it returns None by default. This method allows you to handle missing keys gracefully without raising a KeyError, which would occur if you tried to access a key that doesn't exist using the standard dictionary access syntax (dictionary[key]).

# # 44. Validate user input and raise a ValueError when needed.

# def validate_age(age):
#     if age < 0:
#         raise ValueError("Age cannot be negative.")
#     elif age > 120:
#         raise ValueError("Age cannot be greater than 120.")
#     return age




# # 45. Write a context manager that opens and closes a file.

# class FileHandler:
#     def __init__(self, file_path, mode='r'):
#         self.file_path = file_path
#         self.mode = mode
#         self.file = None

#     def __enter__(self):
#         self.file = open(self.file_path, self.mode)
#         return self.file

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.file:
#             self.file.close()

# # Usage example:
# # with FileHandler('test.txt', 'r') as file:
# #     content = file.read()
# #     print(content)  # Output: Contents of the file

# #how Filehandler helped us here?
# # The FileHandler class is a custom context manager that manages the opening and closing of a file. When we use the 'with' statement with FileHandler, it automatically calls the __enter__() method to open the file and returns the file object. This allows us to work with the file within the block of code under the 'with' statement. Once we exit that block, whether an exception occurred or not, the __exit__() method is called, which ensures that the file is properly closed. This helps prevent resource leaks and ensures that files are not left open unintentionally.


# # Mixed Practice
# # 46. Return the top 3 unique values in descending order from a list of integers.

# list_of_integers = [4, 1, 2, 2, 3, 4, 5]

# def top_three_unique(lst):
#     unique_values = set(lst)
#     print(f"Unique values: {unique_values}")
#     sorted_unique_values = sorted(unique_values, reverse=True)
#     print(f"Sorted unique values: {sorted_unique_values}")
#     return sorted_unique_values[:3]
# print(top_three_unique(list_of_integers))

# # 47. Given a sentence, return the word that appears most often.

# most_frequent_sentence = "the quick brown fox jumps over the lazy dog the"
# def most_frequent_word(sentence):
#     word_count = {}
#     words = sentence.split()
#     print(f"words: {words}")
#     for word in words:
#         word_count[word] = word_count.get(word,0)+1
#     print(f"word_count: {word_count}")
#     most_frequent = None
#     max_count = 0
#     for word,count in word_count.items():
#         if count> max_count:
#             max_count = count
#             most_frequent = word
#     return most_frequent

# print(most_frequent_word(most_frequent_sentence))


# # 48. Given two lists, return items that appear in both but only once.
# list1 = [1, 2, 3, 4, 5, 2]
# list2 = [3, 4, 5, 6, 7, 3]
# def find_common_unique(list1, list2):
#     set1 = set(list1)
#     set2 = set(list2)
#     return list(set1 & set2)

# print(find_common_unique(list1, list2))


# # 49. Given a list of dictionaries, sort them by a chosen key.
# def sort_dictionaries(dict_list, key):
#     return sorted(dict_list, key=lambda x: x[key])

# # i dont get this key=lambda x: x[key], explain it
# # The key=lambda x: x[key] is a way to specify the sorting criteria for the sorted() function. In this case, we want to sort a list of dictionaries based on a specific key in each dictionary. The lambda function takes a dictionary x as input and returns the value associated with the specified key. For example, if we want to sort a list of dictionaries by the 'age' key, the lambda function will return the value of 'age' for each dictionary, and the sorted() function will use those values to sort the dictionaries in ascending order. If you want to sort in descending order, you can add the reverse=True argument to the sorted() function like this: sorted
# # why not like this sorted(dict_list, key)?


# dictionaries = [
#     {'name': 'Alice', 'age': 30},
#     {'name': 'Bob', 'age': 25},
#     {'name': 'Charlie', 'age': 35}
# ]
# print(sort_dictionaries(dictionaries, 'age'))  # Output: [{'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Charlie', 'age': 35}]


# # 50. Flatten a nested dictionary into a single-level dictionary.
# nested_dict = {
#     'a': 1,
#     'b': {
#         'c': 2,
#         'd': 3
#     },
#     'e': {
#         'f': 4,
#         'g': {
#             'h': 5
#         }
#     }
# }
# def flatten_dictionary(d, parent_key='', sep='.'):
#     items = {}
#     for key, value in d.items():
#         new_key = f"{parent_key}{sep}{key}" if parent_key else key
#         if isinstance(value, dict):
#             items.update(flatten_dictionary(value, new_key, sep=sep))
#         else:
#             items[new_key] = value
#     return items

# print(flatten_dictionary(nested_dict))
