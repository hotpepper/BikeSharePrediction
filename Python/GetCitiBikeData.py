def get_hh(date):
        
    ap = date[-2:]
    h=date[-11:-9]
    if ap == 'AM':
        if h=='12':
            h=0
    else:
        if h=='12':
            h=12
        else:
            h=int(h)+12

    return h


def read_json():
    import urllib2
    import csv
    import json
    from pprint import pprint
    
    site= 'http://citibikenyc.com/stations/json'
    json_data=urllib2.urlopen(site)#.read()

    data = json.load(json_data)
    pprint(data)
    json_data.close()

    #new_csv = r'C:\Users\Seth\Desktop\citbikeJSONtest3.csv'
    #c_out = open(new_csv,'wb')
    #cw=csv.writer(c_out, dialect='excel')

    siteList=['time','altitude', 'availableBikes', 'availableDocks', 'city', 'id', 'landMark', 'lastCommunicationTime','latitude', 'location', 'longitude', 'postalCode','stAddress1', 'stAddress2','stationName','statusKey', 'statusValue', 'testStation', 'totalDocks']
    #cw.writerow(siteList)
    for i in data['stationBeanList']:
        siteData=[data['executionTime'],i['altitude'],i['availableBikes'],i['availableDocks'],i['city'],i['id'],i['landMark'],i['lastCommunicationTime'],i['latitude'],i['location'],i['longitude'],i['postalCode'],i['stAddress1'],i['stAddress2'],i['stationName'],i['statusKey'],i['statusValue'],i['testStation'],i['totalDocks']]
        #cw.writerow(siteData)
    #c_out.close()
    return data


def fifteen(minute):
    m=int(minute)
    if m <8:
        f=0
    elif m<24:
        f=15
    elif m<38:
        f=30
    elif m<53:
        f=45
    else:
        f=0
    return f

def fifteen_hr(h, m):
    if m>53: h=h+1
    return h

def connect_to_db(data):    
    import psycopg2
    import datetime
    day= datetime.datetime.today().weekday()
    dow={}
    dow[0]='MON'
    dow[1]='TUE'
    dow[2]='WED'
    dow[3]='THU'
    dow[4]='FRI'
    dow[5]='SAT'
    dow[6]='SUN'




    conn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    for i in data['stationBeanList']:
        #print data['executionTime']+"',"+str(i['latitude'])+","+str(i['longitude'])+",'"+i['stAddress1']+"',"+"'"+i['stAddress2']+"'," +"'"+i['stationName']+"',"+"'"+(i['statusKey'])+"','"+i['statusValue']+"',"+str(i['totalDocks'])+","+ str(i['availableBikes'])+","+ str(i['availableDocks'])

        cur.execute("""INSERT INTO rawCitiBike("time", "latitude", "longitude","id","stAddress1", "stAddress2", "stationName", "statusKey", "statusValue", "totalDocks", "availableBikes", "availableDocks", "dow", "hh", "mm", "Fifteen", "day","mth")
VALUES ('"""+data['executionTime']+"',"+str(i['latitude'])+","+str(i['longitude'])+","+str(i['id'])+",'"+i['stAddress1']+"',"+"'"+i['stAddress2']+"'," +"'"+i['stationName']+"',"+"'"+str(i['statusKey'])+"','"+i['statusValue']+"',"+str(i['totalDocks'])+","+ str(i['availableBikes'])+","+ str(i['availableDocks'])+",'"+dow[day]+"',"+str(fifteen_hr(int(get_hh(data['executionTime'])),int(data['executionTime'][-8:-6])))+","+data['executionTime'][-8:-6]+","+str(fifteen(data['executionTime'][-8:-6]))+","+data['executionTime'][8:10]+","+str(int(data['executionTime'][5:7]))+")")



    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()




def sample_connect_to_db(input_name):
    print input_name
    import psycopg2
    # Connect to an existing database
    conn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
                (100, "abc'def"))
    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM test;")
    cur.fetchone()
    #(1, 100, "abc'def")
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

connect_to_db(read_json())
