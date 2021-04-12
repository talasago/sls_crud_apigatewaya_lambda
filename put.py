import json
from crud_test import CrudTest

def update(event, context):
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
    content = ""
    try:
        id      = int(body_load['id'])
        content = str(body_load['content'])
    except:
        raise TypeError('param type error')

    crud_test_data = CrudTest(id = id, content = content)
    updated_data = crud_test_data.update()

    response = {
        "statusCode": 200,
        "body": json.dumps(updated_data)
    }

    return response
