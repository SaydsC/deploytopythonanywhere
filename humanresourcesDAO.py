import mysql.connector
import config as cfg
from config import mysqldb

class humanresourcesDAO:
    connection=""
    cursor =''
    host=''
    user=''
    password=''
    database=''

    def __init__(self):
        self.host=       cfg.mysqldb['host']
        self.user=       cfg.mysqldb['username']
        self.password=   cfg.mysqldb['password']
        self.database=   cfg.mysqldb['database']

    def employee(self, Employees):
        print (Employees)
        
        values = [
        Employees["StaffID"],
        Employees["Name"],
        Employees["Position"],
        Employees["Role"],
        Employees["DepartmentID"]

    ]           
    
    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            username=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def closeAll(self):
        self.connection.close()
        self.cursor.close()
    
    values = []

    def create(self, values):
        cursor = self.getcursor()
        sql="insert into Employees (Name, Position, Role, DepartmentID) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newStaffID = cursor.lastrowid
        self.closeAll()
        return newStaffID

    def getAll(self):
        cursor = self.getcursor()
        sql="select * from Employees"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByStaffID(self, StaffID):
        cursor = self.getCursor()
        sql="select * from Employees where StaffID = %s"
        values = (StaffID,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="update Employees set Name= %s, Position=%s, Role=%s, DepartmentID=%s  where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete(self, StaffID):
        cursor = self.getcursor()
        sql="delete from Employees where StaffID = %s"
        values = (StaffID,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll
        #print("delete done")

    def convertToDictionary(self, result):
        colnames=['StaffID','Name','Position','Role', "DepartmentID"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

humanresourcesDAO = humanresourcesDAO()