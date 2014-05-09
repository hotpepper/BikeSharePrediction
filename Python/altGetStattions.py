
##alternative work flow
import psycopg2
from datetime import datetime

class userInput(object):
    def __str__(self):
        return '''gets user selcted input from map / web input'''
    def __init__(self):
        self.lat=0.0 #passed from map
        self.long=0.0#passed from map
        self.OorD = 0 #origin (-1)/destination (1) / NA (0)
        self.time = datetime.now() #time used for querying -  defaults to current
        self.dow='FRI'
        self.hh=8
        self.fifteen=0
    def hourAdjustment(self):
        if self.time.minute>53: self.hh=self.hh+1

    def dateParse(self):
        m=int(self.time.minute)
        if m <8: self.fifteen=0
        elif m<24: self.fifteen=15
        elif m<38: self.fifteen=30
        elif m<53: self.fifteen=45
        else: self.fifteen=0
        hourAdjustment()


class get(object): 
    def __str__(self):
        return '''queries DB for all stations within [distance] of desired coordinates'''
        
    def __init__(self):
        self.cnxn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
        self.results =[]
        ids=''
        
    def nearby(self, qry, dist=0.01):
        #connect to db - pass this query
        cur = self.cnxn.cursor()
        SQL = """select *
                from stations_shp as s
                where st_intersects(
                ST_BUFFER(ST_GeomFromText('POINT(%s %s)'), %s), s.geom)"""
        #where st_intersects(ST_BUFFER(ST_GeomFromText('POINT(985069.266642 207601.2461)'), 1000), b.geom)
        data = (self.lat, self.long, dist)
        cur.execute(SQL, data)
        for i in cur.fetchall():
            self.results.append(int(i[1]))
        self.id_format()
        #self.results = cur.fetchall()
        
    def id_format(self):
        q=str(self.results)
        self.ids="("+q[1:-1]+")"

class bestBet(object):
    def __str__(self):
        return '''Queries DB for ordered by docks or bikes, within search radius. 
                Has Top3 attribute to store the best 3 locations (distance ad bikes/docks.'''
                
    def __init__(self):
        self.top3={}
        self.results ={}
        
    def query(self, ids, cnxn):
        cur = cnxn.cursor()
        #string concatination here is wrong, but resolved sql error
        SQL = """select *
                from summary as s
                where s.station_id in """+ids+"""
                and s.dow = %s
                and s.hh = %s
                and s."Fifteen" = %s
                order by s."Bikes" desc"""
        data = (self.dow, self.hh, self.fifteen)
        cur.execute(SQL, data)
        temp = cur.fetchall()
        
        for i in temp:
            self.results[int(i[1])]=i[6]
        return temp[:3]

    def best(self,ids,cnxn):
        t3=self.query(ids,cnxn)
        for i in t3:
            self.top3[i[1]]=i[6]

        
#testing----------------
org = userInput()
org.Oord = -1
org.time = dattime.now() #from Map
org.lat=-73.99392888 #from Map
org.long=40.76727216 #from Map
org.dateParse()

Oget= get()  #maybe this should just be called from bestBet()
Oget.nearby(org) #maybe this should just be called from bestBet()

Obest=bestBet()
Obest.best(Oget.ids,Oget.cnxn)
        

