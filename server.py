from flask import Flask, jsonify, url_for, request, redirect, abort
import mysql.connector
from humanresourcesDAO import humanresourcesDAO

#url http://127.0.0.1:5000/employees

app=Flask(__name__, static_url_path='', static_folder='staticpages')

@app.route('/')
def index():
    return "hello"

#get all
@app.route('/employees')
def getAll():
    results = humanresourcesDAO.getAll()
    return jsonify(results)

#find by StaffID
@app.route('/employees/<int:StaffID>')
def findBySatffID(StaffID):
    foundEmployee = humanresourcesDAO.findByStaffID(StaffID)
    
    return jsonify(foundEmployee)

#Create
# curl -X POST -H "content-type:application/json" -d "{\"Role\":\"test\", \"Name\":\"Mr Test\", \"DepartmentID\":123}" http://127.0.0.1:5000/employees

@app.route('/employees', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    #Checking
    employee = {
        "Name": request.json["Name"],
        "Position": request.json["Position"],
        "Role": request.json["Role"],
        "DepartmentID": request.json["DepartmentID"]
    }
    values =(employee['Name'],employee['Position'],employee['Role'],employee['DepartmentID'])
    newStaffID = humanresourcesDAO.create(values)
    employee['StaffID'] = newStaffID
    return jsonify(employee)

#Update
# curl -X PUT -d "{\"Name\":\"New Employee\", \"DepartmentID\":999}" -H "content-type:application/json" http://127.0.0.1:5000/employees

@app.route('/employees/<int:StaffID>', methods=['PUT'])
def update(StaffID):
    foundEmployee = humanresourcesDAO.findByStaffID(StaffID)
    if not foundEmployee:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'DepartmentID' in reqJson and type(reqJson['DepartmentID']) is not int:
        abort(400)

    if 'Name' in reqJson:
        foundEmployee['Name'] = reqJson['Name']
    if 'Position' in reqJson:
        foundEmployee['Position'] = reqJson['Position']
    if 'Role' in reqJson:
        foundEmployee['Role'] = reqJson['Role']
    if 'DepartmentID' in reqJson:
        foundEmployee['DepartmentID'] = reqJson['DepartmentID']
    values = (foundEmployee['StaffID'],foundEmployee['Name'],foundEmployee['Position'],foundEmployee['Role'],foundEmployee['DepartmentID'])
    humanresourcesDAO.update(values)
    return jsonify(foundEmployee)

#Delete
# curl -X DELETE http://127.0.0.1:5000/employees

@app.route('/employees/<int:StaffID>' , methods=['DELETE'])
def delete(StaffID):
    humanresourcesDAO.delete(StaffID)
    return jsonify({"done":True})

if __name__=="__main__":
    app.run(debug=True)