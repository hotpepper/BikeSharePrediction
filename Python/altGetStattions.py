
##alternative work flow
#import psycopg2
import pyodbc
class get(object):
    def __init__(self):
        self.OroD = 0 #origin (-1)/destination (1) / NA (0)
        self.lat=0.0 #passed from map
        self.long=0.0#passed from map
        self.cnxn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
        self.resutls =[]
        
    def nearby(self, dist):
        #connect to db - pass this query
        cur = cnxn.cursor()
        SQL = """select *
                from pt_citibikestations_20130731_wavgride as b
                where st_intersects(ST_BUFFER(ST_GeomFromText('POINT(%s %s)'), %s), b.geom)"""
        #where st_intersects(ST_BUFFER(ST_GeomFromText('POINT(985069.266642 207601.2461)'), 1000), b.geom)
        data (self.lat, self.long, dist)
        cur.execute(SQL, data)
        self.results = cur.fetchall()

#testing----------------

get= get()
get.lat=985069.266642
get.long=207601.2461
get.nearby(1000)
        



