import pymongo
import dns
import webbrowser

conn = pymongo.MongoClient(
    "mongodb+srv://username:password@cluster0.igqz6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# Create database
db = conn["HealthRecords"]
# Ceate hospital collection
mycol1 = db["Hospitals"]
# Ceate doctor collection
mycol2 = db["Doctors"]


def createcols():
    # Documents to be entered
    mydata1 = [{"hospital_id": "1", "hospital_name": "Agakhan", "address": "Nairobi"},
               {"hospital_id": "2", "hospital_name": "Mater", "address": "Nairobi"},
               {"hospital_id": "3", "hospital_name": "Metropolis", "address": "Kisumu"}]
    # Insert documents to collection
    x = mycol1.insert_many(mydata1)

    # Dociments to be added to doctor collection
    mydata2 = [
        {"doctor_id": 11, "doctor_name": "Mercy", "hospital_id": "1", "date_joined": "2012-02-12",
         "speciality": "Gynacology", "Salary": 50000, "experience": 10},
        {"doctor_id": 12, "doctor_name": "James", "hospital_id": "2", "date_joined": "2017-05-17",
         "speciality": "Physisian", "Salary": 40000, "experience": 4},
        {"doctor_id": 13, "doctor_name": "MercyAngie", "hospital_id": "3", "date_joined": "2018-02-06",
         "speciality": "Neurology", "Salary": 80000, "experience": 7}
    ]
    # Insert documents to collection
    y = mycol2.insert_many(mydata2)


def querycols():
    # Fetch documents as a list of dictionaries
    search = mycol2.find()
    # print list line by line
    for s in search:
        print(s)


def querysalary():
    # Query documents whose salary is greater than 40000
    myquery = {"Salary":  {"$gt": 40000}}
    # Fetch results of the query
    search2 = mycol2.find(myquery)
    # print list line by line
    for x in search2:
        print(x)


the_join = []

tbl = "<tr><td>_id</td><td>hospital_id</td><td>hospital_name</td><td>address</td><td>hospital_join</td></tr>"
the_join.append(tbl)


def joincols():
    # Use aggregate function to join the tables
    join_cursor = db.Hospitals.aggregate(
        [
            {
                "$lookup": {
                    "from": "Doctors",
                    "localField": "hospital_id",
                    "foreignField": "hospital_id",
                    "as": "hospital_join"
                }
            }
        ]
    )

   # print results line by line
    for y in join_cursor:
        # print(j)

        a = "<tr><td>%s</td>" % y['_id']
        the_join.append(a)
        b = "<td>%s</td>" % y['hospital_id']
        the_join.append(b)
        c = "<td>%s</td>" % y['hospital_name']
        the_join.append(c)
        d = "<td>%s</td></tr>" % y['address']
        the_join.append(d)
        e = "<td>%s</td></tr>" % y['hospital_join']
        the_join.append(e)


# Enter hospital docs as a list of html records
health = []
tbl = "<tr><td>_id</td><td>hospital_id</td><td>hospital_name</td><td>address</td></tr>"
health.append(tbl)
for y in mycol1.find():
    a = "<tr><td>%s</td>" % y['_id']
    health.append(a)
    b = "<td>%s</td>" % y['hospital_id']
    health.append(b)
    c = "<td>%s</td>" % y['hospital_name']
    health.append(c)
    d = "<td>%s</td></tr>" % y['address']
    health.append(d)

# Enter hospital docs as a list of html records
docs = []
tbl2 = '''
               <tr><td>_id</td><td>doctor_id</td><td>doctor_name</td><td>hospital_id</td><td>date_joined</td><td>speciality</td><td>salary</td><td>experience</td></tr>'''
docs.append(tbl2)
for y in mycol2.find():
    a = "<tr> <td > %s < /td >" % y['_id']
    docs.append(a)
    b = "<td>%s</td>" % y['doctor_id']
    docs.append(b)
    c = "<td>%s</td>" % y['doctor_name']
    docs.append(c)
    d = "<td>%s</td>" % y['hospital_id']
    docs.append(d)
    e = "<td>%s</td>" % y['date_joined']
    docs.append(e)
    f = "<td>%s</td>" % y['speciality']
    docs.append(f)
    g = "<td>%s</td>" % y['Salary']
    docs.append(g)
    h = "<td>%s</td></tr>" % y['experience']
    docs.append(h)


def displayhtml():

    # Create html file
    f = open('hrec.html', 'w')

    # First part of html docstring
    the_html = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta cSharset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Records</title>
    </head>
    <body>
        <h1>Health records</h1>
        <table style="border: solid; border-spacing: 25px, border-collapse: collapse;">
        <thead><caption><h2> Hospitals </h2></caption></thead>
        %s
        </table>
        <table style="border: solid; border-spacing: 25px, border-collapse: collapse;">
        <thead><caption><h2> Doctors </h2></caption></thead>
        %s
        </table>
         <table style="border: solid; border-spacing: 25px, border-collapse: collapse;">
        <thead><caption><h2> Joined </h2></caption></thead>
        %s
        </table>
    </body>
    </html>''' % (health, docs, the_join)  # from list

    # write to html file
    f.write(the_html)
    # close file
    f.close()

    # Open file in browser
    webbrowser.open_new_tab('hrec.html')


# createcols()
joincols()
displayhtml()
