# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import hashlib
import json
import time
from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(

)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    reqestbody = {"abc": "hello", "macklu": "luxiaosan"}
    strbody = json.dumps(reqestbody)
    str = "abcdefg"
    m = hashlib.md5()
    m.update(strbody.encode(encoding="utf-8"))
    str_md5 = m.hexdigest()
    print(str_md5)
    appSecret = "ff71f1d41ac7"
    curTime = "1631611762867"
    sha_str = appSecret + str_md5 + curTime
    sha = hashlib.sha1()
    sha.update(sha_str.encode(encoding="utf-8"))
    sha_str_h = sha.hexdigest()
    print(sha_str_h)
    print(int(round(time.time() * 1000)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
