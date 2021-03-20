#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pymongo
import dnspython


# In[16]:


#Connect to mongodbatlas
conn = pymongo.MongoClient("mongodb+srv://ess:newlight@cluster0.igqz6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

#Create database
db = conn["HealthRecords"]

#Ceate hospital collection
mycol1 = db["Hospital"]


# In[8]:


#Documents to be entered
mydata1 = [    {"hospital_id": "1", "hospital_name": "Agakhan", "address": "Nairobi" },
    {"hospital_id": "2", "hospital_name": "Mater", "address": "Nairobi" },
         {"hospital_id": "3", "hospital_name": "Metropolis", "address": "Kisumu" }]

#Insert documents to collection
x = mycol1.insert_many(mydata1)


# In[7]:


#Show databases
print(conn.list_database_names())


# In[19]:


#Show collections
print(db.list_collection_names())


# In[44]:


#Check if database exists
dblist = conn.list_database_names()
if "" in dblist:
    print ("Database exists")


# In[10]:



#Ceate doctor collection
mycol2 = db["Doctor"]

#Dociments to be added to doctor collection
mydata2 = [
    {"doctor_id": 11, "doctor_name": "Mercy", "hospital_id": "1", "date_jponed":"2012-02-12",
     "speciality": "Gynacology", "Salary": 50000, "experience": 10},
    {"doctor_id": 12, "doctor_name": "James", "hospital_id": "2", "date_jponed": "2017-05-17",
     "speciality": "Physisian", "Salary": 40000, "experience": 4},
    {"doctor_id": 13, "doctor_name": "MercyAngie", "hospital_id": "3", "date_jponed": "2018-02-06",
     "speciality": "Neurology", "Salary": 80000, "experience": 7}
]

#Insert documents to collection
y = mycol2.insert_many(mydata2)


# In[13]:


#Fetch documents as a list of dictionaries
search = mycol2.find()

#print list line by line
for s in search:
    print (s)


# In[18]:


#Query documents whose salary is greater than 40000
myquery = {"Salary":  { "$gt": 40000 }}
#Fetch results of the query
search2 = mycol2.find(myquery)

#print list line by line
for x in search2:
    print (x)


# In[30]:


#Use aggregate function to join the tables
join_cursor = db.Hospital.aggregate(
[
    {
        "$lookup": {
        "from": "Doctor",
        "localField" : "hospital_id", 
       "foreignField" : "hospital_id",
     "as" : "hospital_join"       
    }
    }
]
)

#print results line by line
for j in join_cursor:
    print (j)


# In[34]:


import webbrowser
import json


# In[58]:


#Sample list of dictionaries
a = [{'sam': 'name'},{'Harris':'name'},{'is':'age'},
    {'ess': 'name'},{'josh':'name'},{'age':23}]


# In[59]:


#Create html file
f = open('hrec.html', 'w')

#First part of html docstring
m1 = ''',<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Records</title>
</head>
<body>
    <h1>Health records</h1>'''

#write to html file
f.write(m1)

#wresults of join
for x in join_cursor:
    jsn = json.dumps(x) #convert list of dictionaies to json
    f.write(jsn) #write fson to html

#using sample
for y in a:
    testjsn = json.dumps(y)
    f.write(testjsn)

#closing html tags
m2 = '''</body>
</html>'''
f.write(m2)

#close file
f.close()

#Open file in browser
webbrowser.open_new_tab('hrec.html')


# In[ ]:




