# Review 1
def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

"""
The default argument will get cached once it get called. So when calling the second time with default argument, `my_list` will not be empty.
Example: 
add_to_list(1) # return [1]
add_to_list(2) # return [1,2]

Fix it by avoid referencing object in default argument:
def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list
"""
 
# Review 2
def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."
"""
Missing an f for f-string, the code return the string without Interpreting the variable.
Example:
format_greeting("Yuk", 28) # return "Hello, my name is {name} and I am {age} years old."

Fix by making it a f-string:
def format_greeting(name, age):
    return f"Hello, my name is {name} and I am {age} years old."
"""
 
# Review 3
class Counter:
    count = 0
 
    def __init__(self):
        self.count += 1
 
    def get_count(self):
        return self.count
    
"""
I am guessing this code are trying to increase the count each time when Counter class is Initialized? However since is is increasing self.count in __init__ function, it is increasing the instance specific variable. In order to increase the class variable, we need to use Counter.count.
Example:
Counter().get_count() #return 1
Counter().get_count() #return 1

Fix by increasing class variable:
class Counter:
    count = 0
 
    def __init__(self):
        Counter.count += 1
 
    def get_count(self):
        return Counter.count
"""
 
# Review 4
import threading
 
class SafeCounter:
    def __init__(self):
        self.count = 0
 
    def increment(self):
        self.count += 1
 
def worker(counter):
    for _ in range(1000):
        counter.increment()
 
counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)
 
for t in threads:
    t.join()

"""
+= isn't guaranteed atomic, it require a lock to be thread safe.
Fix by adding lock on increasing count:
class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
 
    def increment(self):
        with self.lock:
            self.count += 1
"""
 
# Review 5
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] =+ 1
        else:
            counts[item] = 1
    return counts

"""
Wrong Symbol. =+ is interpreted as counts[item] = (+1). So it is assigning 1 to existing item, not increasing.
Example:
count_occurrences([1,2,3,3]) # return {1: 1, 2: 1, 3: 1}
Fix by correcting symbol:
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts
"""
 