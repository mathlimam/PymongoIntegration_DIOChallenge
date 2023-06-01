import pymongo as pym
import datetime as dt
import random



client = pym.MongoClient("mongodb+srv://admin:1234@diochallenge.9rp3hor.mongodb.net/?retryWrites=true&w=majority")


db = client.bank
clients = db.clients
accounts = db.accounts


new_clients = [
    {
		"name": "Dai Murphy",
		"cpf": "626.556.875-61",
		"address": "329-4477 Posuere Street",
        "date":dt.datetime.utcnow()
	},
	{
		"name": "Hyatt Nash",
		"cpf": "833.277.687-04",
		'address': "988-418 Euismod Ave",
        "date":dt.datetime.utcnow()
	},
	{
		"name": "Velma Moreno",
		"cpf": "242.562.181-53",
		"address": "Ap #124-7676 Facilisi. Av.",
        "date":dt.datetime.utcnow()
	},
	{
		"name": "Cailin Osborne",
		"cpf": "572.415.956-06",
		"address": "5296 Gravida Rd.",
        "date":dt.datetime.utcnow()
	},
	{
		"name": "Claudia Bailey",
		"cpf": "382.811.841-13",
		"address": "P.O. Box 706, 934 Nullam Rd.",
        "date":dt.datetime.utcnow()
	}     
    ]


objInstance = clients.insert_many(new_clients).inserted_ids #Insere as informações no BD


data = clients.find()
for d in data:
    id = d["_id"]
    tmpInstance = accounts.insert_one({"client_id":id, "type":"Conta Corrente","agency":"0001", "cc": random.randint(10000, 99999)})
   

#Fazendo o Join das coleções
results = clients.aggregate([{
    '$lookup':{
        'from':'accounts',
        'localField':'_id',
        'foreignField':'client_id',
        'as':'accounts'

    }

}])


for result in results: 
    print(f'''
    Name: {result['name']}
    CPF: {result['cpf']}
    Address: {result['address']}
    Account Type: {result['accounts'][0]['type']}
    Agency: {result['accounts'][0]['agency']}
    C/C: {result['accounts'][0]['cc']}
    ''')






