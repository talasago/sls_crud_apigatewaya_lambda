import json
from crud_test import CrudTest

def delete(event, context):
    # 更新パラメータ取得
    body = event.get('body')
    # パラメータがないならばエラー
    if body == None:
         raise

    body_load = json.loads(body)
    # パラメータがないならばエラー
    if body_load == None:
        raise
    # idパラメータがないならばエラー
    if not 'id' in body_load:
        raise

    id = ""
    try:
        id = int(body_load['id'])
    except:
        raise TypeError('param type error')

    crud_test_data = CrudTest(id = id)
    deleted_id = crud_test_data.delete()

    body = {
        "deleted id": deleted_id
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
