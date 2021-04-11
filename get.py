import json
from crud_test import CrudTest

def read(event, context):
    # クエリパラメータ取得
    queryParam = event.get('queryStringParameters') # クエリパラメータ取得
    print(queryParam)

    id = None
    # クエリパラメータ(id)がある場合
    if not queryParam == None and not queryParam.get('id') == None:
        try:
            id = int(queryParam.get('id'))
        except:
            raise TypeError('id is type error')

    crud_test_data = CrudTest(id = id)
    result_records = crud_test_data.select()

    body = {
        "result_records": result_records
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
