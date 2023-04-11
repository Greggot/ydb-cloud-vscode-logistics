import os
import ydb
import ydb.iam 

# from dbclient import ydb_client

def blocking_query(session, query):
  return session.transaction().execute(
    query,
    commit_tx = True,
    settings = ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
  )

class stateReader:
    def __init__(self):
        self.gov_number = ''
        self.name = ''
        self.query = ''
        self.model = ''
        
    def select_name(self, name):
        self.name = name
    def select_gov_number(self, gov_number):
        self.gov_number = gov_number
    def select_model(self, model):
        self.model = model
    
    def select_all_cars(self, session):
        self.query = \
        '''SELECT 
            automobiles.id AS id,
            automobiles.name AS name,
            model
        FROM
            automobiles
        LEFT JOIN models AS mod ON automobiles.modelid = mod.id;''';
        return blocking_query(session, self.query)
    
    def select_all_models(self, session):
        self.query = 'SELECT * FROM models;'
        return blocking_query(session, self.query)

    def select_cars_by_parameters(self, session):
        if(self.gov_number == ''):
            self.query = 'SELECT * FROM automobiles WHERE name = \"' + self.name + '\";';
        elif(self.name == ''):
            self.query = 'SELECT * FROM automobiles WHERE gov_number = \"' + self.gov_number + '\";';
        else:
            self.query = 'SELECT * FROM automobiles WHERE name = \"' + self.name + '\" AND gov_number = "' + self.gov_number + '";';
        return blocking_query(session, self.query);

    def select_cars_by_model(self, session):
        self.query = \
        '''SELECT 
            automobiles.id AS id,
            automobiles.name AS name,
            model
        FROM
            automobiles
        LEFT JOIN models AS mod ON automobiles.modelid = 
            mod.id WHERE mod.model = "''' + self.model + '''";'''
        return blocking_query(session, self.query)

    def clear_state(self):
        self.name = ''
        self.gov_number = ''

    def get_last_query(self):
        return self.query
        
state_reader = stateReader()