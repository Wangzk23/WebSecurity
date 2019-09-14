import re

i,j=1,'john'
print(i,'\n',j);

b="0123456"
list = ['a',123,1.2,b]
t = [123, 'john']   #列表
y = ('f','j')   #元组

print(b[1:3])
print(list)
print(list[0])
print(t * 2)
print(list +t)

Money = 2000


def AddMoney():
    # 想改正代码就取消以下注释:
    global Money
    Money = Money + 1

print (Money)
AddMoney()
print(Money)

'''str = input("Input：")
print("Output:",str)'''

fo = open("foo.txt","w")
str = fo.write("abc\ndef\n")
fo.close()
print("文件是否被关闭：",fo.closed)

fo = open("foo.txt","r+")
str = fo.read(6)
print("读取的字符串是：\n",str)
fo.close()

str= 'server version for the right syntax to use near \'(\'1\'\') LIMIT 0,1\''
find1 = re.search(r'\'([\'\"\(]*)[0-9]*\'', str)    #find1可行
find2 = re.search(r'\'.*([0-9]{1,2})\'([\'\"\)]*)', str)
print(find1.group(1))


print('-'*20)

var = "b"
dict = {'a':var}
print(dict['a'])