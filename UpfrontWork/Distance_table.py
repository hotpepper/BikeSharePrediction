#this only needs to be run when statiions have changed



import csv, os, psycopg2

desk = r'C:\Users\'
f = 'citbikeJSONtest3.csv'

input_file = os.path.join(desk, f)
print input_file

def get_input():
    '''get the stations with lat/long'''
    dist={}
    with open(input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[5] != 'id':
                ID, lat, lng= int(row[5]), float(row[8]), float(row[10])
                if ID not in dist:
                    dist[ID]=[lat,lng]
    return dist

dist=get_input()

def distance(x1,y1, x2,y2):
    return (((x1-x2)**2)+((y1-y2)**2))**.5


def build_dict(d):
    dist={}
    for i in d.keys():
        dist[i]={}
        for j in d.keys():
            if j not in dist[i]:
                #print i, j
                dist[i][j]= distance(d[i][0],d[i][1],d[j][0],d[j][1])
    return dist

distance_dict=build_dict(dist)




def write_table(data, d):
    conn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
    cur = conn.cursor()
    for i in data:
        for j in data[i]:
            s1, s2, distance = i, j, data[i][j]
            cur.execute("""INSERT INTO station_distance( "station1", "lat1", "long1", "station2", "lat2", "long2", "distance" ) VALUES ("""+str(s1)+","+str(d[i][0])+","+str(d[i][1])+","+str(s2)+","+str(d[j][0])+","+str(d[j][1])+","+str(distance)+")")

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

write_table(distance_dict, dist)
