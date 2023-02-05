# python -m pip install suds
from suds.client import Client
from spyne import Array

client = Client('http://localhost:8000/?wsdl')


#output = client.service.login("robert", "robi")
#print(output)

#output1 = client.service.assign_roles_to_user("admin", ["administrator_aplicatie", "client"])

jws = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEwLCJuYW1lIjoicm9iZXJ0Iiwicm9sZXMiOlsiY2xpZW50Il0sImV4cCI6MTAwMTAzMzAyMzJ9.yQngxiftcF5s1kRk8-LvdOP7Dbelv1bCflfZm8C3E0M"
#output = client.service.logout(jws)
#print(output)

#userAndRoles = client.service.get_user_info_and_his_roles(10, jws)
#print(userAndRoles)

print(client.service.create_new_user("robert", "robi"))
print(client.service.create_new_user("andrei", "andrei"))
print(client.service.create_new_user("sebi", "sebi"))
print(client.service.create_new_user("teo", "teo"))