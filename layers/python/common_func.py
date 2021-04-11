def req_param_require_validation(body, require_elem = []):
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
