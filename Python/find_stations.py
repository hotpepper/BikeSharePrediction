import psycopg2,  Tkinter

def get_stations():
    conn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
    # Open a cursor to perform database operations
    cur = conn.cursor()

    
    cur.execute("""select distinct "id", "stationName", latitude, longitude
from rawcitibike
order by id""")

    # Close communication with the database
    station_dict={}
    for i in cur:
        station_dict[i[0]]=i[1:]
    cur.close()
    conn.close()
    return station_dict
    
stations=get_stations()

def get_best3(stations):
       
    st_id=int(raw_input('What Station # do you want? \n'))#place holder for testing 
    #get station from map
    print stations[st_id]
    h= int(raw_input('What time do you expect to arrive (hours 24h)?\n'))

    conn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
    cur = conn.cursor()
    #change query to get all stations within x distance geo query
    #then sort based on availibility
    cur.execute("""select station2 as Station_ID, st_name2 as Name, hh as Hour, avg_Docks, (avg_Docks/"totalDocks")*100 as pct_empty, distance

    from 
    (select station2,  st_name2, distance
    from station_distance
    where station1 = """+str(st_id)+"""
    order by distance 
    limit 4) as top_3, 


    (select id, hh,  avg("availableBikes") as avg_Bikes, 
    avg("availableDocks") as avg_Docks, count("ID") as cnt, "totalDocks"
    from rawcitibike
    where dow in ('TUE', 'WED', 'THU') and hh = """+str(h)+""" 
    group by hh,  id, "totalDocks") as open

    where station2=id
    order by pct_empty desc""")
    print "At "+str(h)+':00 best chances are'
    print "-----------------------------------"
    for i in cur:
        print str(i[0])+':', i[1], '\n',str(int(i[3]))+' docks open |', str(int(i[4]))+'% open |', str(i[5])[:5]+' degrees away','\n'
    conn.close()
    return st_id

while st_id!=0:
    print "enter '0' for station to end"
    get_best3(stations)
