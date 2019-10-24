# This is a Python code snippet that sorts a dictionary based on its value in the form of a list of tuple's

import operator
d = {'Festus': 4, 'Abass':3 , 'Patrick': 6, 'Victor': 1, 'Paul': 2, 'Doyin': 3}
new_tuple = sorted(d.items(), key = operator.itemgetter(1))
print(new_tuple)
