import csv
from multiprocessing.sharedctypes import Value

class CsvFile :
    def __init__(self, path):
        self.path = path
        pass

    def getHeader(self):
        file = open(self.path)
        csvreader = csv.reader(file,delimiter=';')
        return next(csvreader)

    def getDataAsDict(self):
        file = open(self.path)
        csvreader = csv.reader(file,delimiter=';')
        header = next(csvreader)
        dataset = []
        for row in csvreader:
            rowtable = {}
            i=0
            for data in row:
                rowtable[header[i]] = data
                i+=1

            dataset.append(rowtable)
        file.close()
        return dataset
    
    def getDataAsArray(self):
        file = open(self.path)
        csvreader = csv.reader(file,delimiter=';')
        header = next(csvreader)
        dataset = []
        for row in csvreader:
            rows=[]
            for value in row:
                value = value.replace(',','.')
                rows.append(value)
            dataset.append(rows)
        file.close()
        return dataset
    
    def __str__(self) -> str:
        texte = self.getDataAsDict().__str__()
        return texte
    
class SqlQuery:
    def __init__(self,table,attributs) -> None:
        self.table = table
        self.attributs = attributs #must be an array
        pass

    def detectType(self,value):
        try:
            returnedValue = int(value)
            returnedValue = str(value)
        except ValueError:
            try:
                returnedValue = float(value)
                returnedValue = str(value)
            except ValueError:
                value = value.replace('\'','\'\'')
                returnedValue = '\' '+value+'\''
        return returnedValue

    def prepare(self, valeurs) -> str:
        query= 'INSERT INTO '+self.table+'( '
        for k in range(len(self.attributs)):
            query+=self.attributs[k]
            if(k!=len(self.attributs)-1):
                query+=' , '
        query+=') VALUES ('
        for k in range(len(valeurs)):
            query+=self.detectType(valeurs[k])
            if(k!=len(valeurs)-1):
                query+=', '
        query+=' );\n'
        return query
    
    

public = CsvFile('Cinemas2020.csv')
query = SqlQuery('cinema', public.getHeader())


f = open("insert.sql", "w")
data = public.getDataAsArray()

for k in range(len(data)):
    f.write(query.prepare(public.getDataAsArray()[k]))

f.close()