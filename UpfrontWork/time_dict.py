import os, csv

folder = r'C:\Users\SHostetter\Desktop\GIT\BikeShareTesting\UpfrontWork'


def read(in_file):
    row_cnt=0
    data={}
    ods=[]
    with open(in_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            od = set([row[3],row[7]])
            od_key= (row[3],row[7])
            if od in ods:
                try:
                    data[od_key].append(row[0])
                except:
                    od_key= (row[7],row[3])
                    data[od_key].append(row[0])
            else:
                ods.append(set([row[3],row[7]]))
                data[od_key]=[row[0]]
            #data.append(row)
            row_cnt+=1
        
    print str(row_cnt)+" rows were read from "+str(in_file)   
    return data

data = read(os.path.join(folder,'2013-08 - Citi Bike trip data.csv'))


import pickle



with open(os.path.join(folder,'data.pickle'), 'wb') as handle:
  pickle.dump(data, handle)

##with open(os.path.join(folder,'data.pickle'), 'rb') as handle:
##  b = pickle.load(handle)


