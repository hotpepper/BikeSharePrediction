
##alternative work flow
import psycopg2
from datetime import datetime

class userInput(object):
    def __init__(self):
        self.Olat=0.0
        self.Olong=0.0
        self.Odatetime=None
        self.Dlat=0.0
        self.Dlong=0.0
        self.Ddatetime=None
        
    def __str__(self):
        return '''gets the start and end locations and times from map'''

class get(object):
    def __init__(self):
        self.cnxn = psycopg2.connect("dbname=CitiBike user=postgres password = ''")
        self.results =[]
        ids=''
        
    def nearby(self, Ulat,Ulong,dist = 0.01):
        #connect to db - pass this query
        cur = self.cnxn.cursor()
        SQL = """select *
                from stations_shp as s
                where st_intersects(
                ST_BUFFER(ST_GeomFromText('POINT(%s %s)'), %s), s.geom)"""
        #where st_intersects(ST_BUFFER(ST_GeomFromText('POINT(985069.266642 207601.2461)'), 1000), b.geom)
        data = (Ulat, Ulong, dist)
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
        self.top3={}
        self.dow=''
        self.hh=8
        self.fifteen=0
        self.results ={}

    def getFifteen(self, minute):
        m=int(minute)
        if m>53: hself.hh+=1
        if m <8: f=0
        elif m<24: f=15
        elif m<38: f=30
        elif m<53: f=45
        else: f=0
        self.fifteen=f
      
    def processDate(self, Udatetime):
        '''takes in the datetime of the start or end and pulls necessary data'''
        day = {1:'MON', 2:'TUE', 3:'WED',4:'THUR',5:'FRI',6:'SAT',7:'SUN'}
        self.dow = day[Udatetime.weekday()]
        self.hh = Udatetime.hour
        getFifteen(Udatetime.minute)
        
    def query(self, ids, cnxn, Udatetime):
        processDate(Udatetime)
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

    def best(self,ids,cnxn, Udatetime):
        t3=self.query(ids,cnxn, Udatetime)
        for i in t3:
            self.top3[i[1]]=i[6]

        
#testing----------------
userInput =  userInput()
userInput.Olat=-73.99392888
userInput.Olong=40.76727216
userInput.Odatetime=datetme.datetime.now()

get= get()
best=bestBet()
get.nearby(userInput.Olat,userInput.Olong)
 
best.best(get.ids,get.cnxn, userInput.Odatetime)
        

