import json
from crud_test import CrudTest

def create(event, context):
    # 更新パラメータ取得
    body = event.get('body')

    print(event)
    print(body)

    # パラメータがないならばエラー
    if body == None:
         raise

    body_load = json.loads(body)

    # パラメータがないならばエラー
    if body_load == None:
        raise
    # 更新パラメータがないならばエラー
    if not 'id' in body_load or not 'content' in body_load:
        raise

    id = ""
    content = ""
    try:
        id      = int(body_load['id'])
        content = str(body_load['content'])
    except:
        raise TypeError('param type error')

    crud_test_data = CrudTest(id=id, content=content)
    created_id = crud_test_data.insert()

    body = {
        "created_id": created_id
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
