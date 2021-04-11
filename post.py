import json
from crud_test import CrudTest

def create(event, context):
    # 更新パラメータ取得
    body = event.get('body')

    print(event)
    print(body)

    # 必須チェック
    # パラメータがないならばエラー
    if body == None:
        raise
    # パラメータがないならばエラー
    body_load = json.loads(body)
    if body_load == None:
        raise
    # 更新パラメータがないならばエラー
    if not 'content' in body_load:
        raise

    content = ""

    #error_massage = req_param_require_validation(body=req_body,
    #                                            require_elem=['content'])
    #if error_massage != "":
    #    raise error_massage
    try:
        content = str(body_load['content'])
    except:
        raise TypeError('param type error')


    crud_test_data = CrudTest(content=content)
    created_id = crud_test_data.insert()

    body = {
        "created_id": created_id
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
