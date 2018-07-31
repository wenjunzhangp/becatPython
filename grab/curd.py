#mysql增删改查py版
import pymysql
import time

#获取参数
host = "127.0.0.1"
username = "root"
password = "root"
database = "test"

#测试数据库连接
def testconnect():
    #打开数据库链接
    db = pymysql.connect(host,username,password,database)
    #使用cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    #使用execute()方法执行SQL查询
    cursor.execute("select version()")
    #使用fetchone ()获取单条数据
    data = cursor.fetchone()
    print(data)
    db.close()

#插入数据库
def InsertDate():
    #打开数据库链接
    db = pymysql.connect(host,username,password,database,charset='utf8')
    #使用cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    end_time = time.strftime('%Y-%m-%d %H:%M:%S')
    #Sql 插入语句
    sql = "INSERT INTO sys_user_role (`sys_user_id`, `sys_role_id`) " \
          "VALUES ('%s','%s')" \
          %(5,10)
    try:
        tt = cursor.execute(sql)
        db.commit()
        print("新增成功，事物已提交")
    except UnicodeEncodeError as e :
        #发生错误时回滚
        print(e)
        db.rollback()
        db.close()

#查询操作
def selectData():
    db = pymysql.connect(host, username, password, database, charset='utf8')
    # 使用cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from sys_user_role where id >='%d'" %(1)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            sys_user_id = row[1]
            sys_role_id = row[2]
            print("id = %d,sys_user_id=%s,sys_role_id=%s" %(id,sys_user_id,sys_role_id))
        db.commit()
    except UnicodeEncodeError as e :
        #发生错误时回滚
        print(e)
        db.close()

#更新操作
def update_data():
    db = pymysql.connect(host, username, password, database, charset='utf8')
    # 使用cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = "update sys_user_role set sys_user_id ='%s' where id >='%d' " %(20,1)
    try:
        #执行sql
        cursor.execute(sql)
        db.commit()
        print("更新成功事物已提交")
    except UnicodeEncodeError as e :
        #发生错误时回滚
        print(e)
        db.rollback()
        db.close()

#删除操作
def delete_Date():
    db = pymysql.connect(host, username, password, database, charset='utf8')
    # 使用cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "delete from sys_user_role where id <='%d' " %(1)
    try:
        cursor.execute(sql)
        db.commit()
        print("删除成功事物已提交")
    except UnicodeEncodeError as e :
        #发生错误时回滚
        print(e)
        db.rollback()
        db.close()

if __name__ == '__main__':
    # testconnect()
    # InsertDate()
    selectData()
    # update_data()
    # delete_Date()