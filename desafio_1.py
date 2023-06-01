
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import random

Base = declarative_base()


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False)
    address = Column(String(50), nullable=False)


    accounts = relationship(
        "Accounts", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'Client (id={self.id}, Name= {self.name}, CPF= {self.cpf}, Address= {self.address})'



class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    agency = Column(String(4), nullable=False)
    num = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)


    client = relationship(
        "Client", back_populates="accounts"
    )

    def __repr__(self):
        return f'Accounts (id= {self.id}, Account_Type= {self.type}, Agency= {self.agency}, CC= {self.num}, Client_id= {self.client_id} )'



engine = create_engine("sqlite://")
Base.metadata.create_all(engine)



with Session(engine) as sess:

    data = [
    {
		"name": "Dai Murphy",
		"cpf": "626.556.875-61",
		"address": "329-4477 Posuere Street"
	},
	{
		"name": "Hyatt Nash",
		"cpf": "833.277.687-04",
		'address': "988-418 Euismod Ave"
	},
	{
		"name": "Velma Moreno",
		"cpf": "242.562.181-53",
		"address": "Ap #124-7676 Facilisi. Av."
	},
	{
		"name": "Cailin Osborne",
		"cpf": "572.415.956-06",
		"address": "5296 Gravida Rd."
	},
	{
		"name": "Claudia Bailey",
		"cpf": "382.811.841-13",
		"address": "P.O. Box 706, 934 Nullam Rd."
	}     
    ]
 
    for d in data:
        tmp = Client(
            name = d['name'],
            cpf = d['cpf'],
            address = d['address'],
            accounts = [Accounts(type="Conta_Corrente", agency="0001", num=random.randint(10000, 99999))]
        )

        sess.add(tmp)
        sess.commit()


stmt_order = select(Client).order_by(Client.name.asc())
for result in sess.scalars(stmt_order):
    print(result)


stmt_join = select(Client.name, Accounts.type, Accounts.agency, Accounts.num).join_from(Accounts, Client)


connection = engine.connect()
results = connection.execute(stmt_join)
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Accounts)
for result in sess.scalars(stmt_count):
    print(result)