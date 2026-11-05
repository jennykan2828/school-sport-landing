# f = open('hello.txt', 'r')
# content = f.read()
# f.close()
# print(content)
# 
# print('----')
# with open ('hello.txt', 'r') as f:
#      content = f.read()
#      f.close()
#     
# print(content)
# 
# filename='names.txt'
# with open(file=filename, mode = 'w') as f:
#      f.write('mark')
# 
# 
# with open(file=filename, mode = 'r') as f:
#      name = f.readline(1)
#      print(f'hi {name}')

# name_list = input("what are the students' names?").split()
# name_list = [name + '\n' for name in name_list]
# print(name_list)
# #store names individually 
# filename='users.txt'
# with open(file=filename, mode = 'a') as f:
#     f.writelines(name_list)

# with open(file=filename, mode = 'r') as f:
# #     name = f.readline()
#     for name in f:
#        print(f'hi {name}')

utf8= 'utf-8'
with open('chinese.txt', 'w', encoding = utf8) as f:
    f.write('你好')