import os
import ydb
import ydb.iam

from dbclient import ydb_client
from statereader import state_reader
from dbclient import to_json_array
from exception import ConnectionFailure

pool = ydb.SessionPool(ydb_client.create_driver())

def read_car_params(reader, parameters):
  if('gov_number' in parameters):
    reader.select_gov_number(parameters['gov_number'])
    return True
  if('name' in parameters):
    reader.select_name(parameters['name'])
    return True
  return False

def read_all_data(reader, parameters):
    if(parameters['all'] == 'cars'):
        return pool.retry_operation_sync(state_reader.select_all_cars)
    elif(parameters['all'] == 'models'):
        return pool.retry_operation_sync(state_reader.select_all_models)
    return None

def handler(event, context):
  parameters = event['queryStringParameters']
  status = 200
  result = None

  if(event['httpMethod'] == 'GET'):
    if('all' in parameters):
      result = read_all_data(state_reader, parameters)
      if(result == None):
        status = 400
    elif('sort-by-model' in parameters):
        state_reader.select_model(parameters['sort-by-model'])
        result = pool.retry_operation_sync(state_reader.select_cars_by_model)
    else:
      if(read_car_params(state_reader, parameters)):
        result = pool.retry_operation_sync(state_reader.select_cars_by_parameters)
        state_reader.clear_state()
      else:
        status = 501
  else:
    status = 501

  return {
    'statusCode': status,
    'body': to_json_array(result[0].rows) if status == 200 else '',
  }