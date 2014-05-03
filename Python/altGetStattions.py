
##alternative work flow
import psycopg2

class get(object):
    def __init__(self):
        self.lat=0.0 #passed from map
        self.long=0.0#passed from map
        self.cnxn = psycopg2.connect("dbname=CitiBike user=postgres password = 'hosts464'")
        self.results =[]
        ids=''
        
    def nearby(self, dist):
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
    def __init__(self):
        self.OroD = 0 #origin (-1)/destination (1) / NA (0)
        self.top3={}
        self.dow='FRI'
        self.hh=8
        self.fifteen=0
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

get= get()
best=bestBet()
get.lat=-73.99392888
get.long=40.76727216
get.nearby(0.01)

best.best(get.ids,get.cnxn)
        

