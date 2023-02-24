# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    file = open("man_case.txt")
    lines = file.readlines()
    for line in lines:
        items = line.split("\t")
        if len(items) == 4:
            newline = re.sub(r'\D',"",items[0])+"\t"+re.sub(r'\D',"",items[1])+"\t"+re.sub(r'\D',"",items[2])+"\t"+re.sub(r'\D',"",items[3])
            print(newline)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
