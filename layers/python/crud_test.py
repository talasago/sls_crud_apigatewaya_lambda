import json
import os
import boto3

rdsData       = boto3.client('rds-data')
cluster_arn   = os.environ['CLUSTER_ARN']
secret_arn    = os.environ['SECRET_ARN']
database_name = os.environ['DATABASE_NAME']
schema_name   = os.environ['SCHEMA_NAME']

class CrudTest:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def _rds_begin_transaction(self):
        return rdsData.begin_transaction(
                            database = database_name,
                            resourceArn = cluster_arn,
                            secretArn = secret_arn,
                            )

    def _rds_commit_transaction(self,   tran_id):
        return rdsData.commit_transaction(
                            resourceArn = cluster_arn,
                            transactionId = tran_id,
                            secretArn = secret_arn,
                            )

    # AuroraServerlessへのsql実行メソッド
    def _rds_exe_statement(self, exe_sql, param = None, tran_id=""):
        return rdsData.execute_statement(
                        resourceArn = cluster_arn,
                        secretArn = secret_arn,
                        database = database_name,
                        sql = exe_sql,
                        parameters = param,
                        transactionId = tran_id)

    def select(self):
        sql = ""
        param = []

        if self.id == None:
            sql =  f"select * from crud_test;"
        else:
            sql =  f"select * from crud_test where id = :id;"
            param = [{'name': 'id', 'value': { 'longValue': self.id }}]

        exe_statement_response = self._rds_exe_statement(exe_sql = sql, param = param)
        print(exe_statement_response)

        return exe_statement_response['records']

    def insert(self):

        sql = f"insert into crud_test (content) values (:content);"
        param = [{'name': 'content', 'value': { 'stringValue': self.content }},]

        res_begin_transaction = self._rds_begin_transaction()
        tran_id = res_begin_transaction['transactionId']
        res_exe_statement = self._rds_exe_statement(sql, param, tran_id)
        res_commit_transaction = self._rds_commit_transaction(tran_id)

        print(res_exe_statement)
        print(res_commit_transaction)

        if res_commit_transaction['transactionStatus'] != 'Transaction Committed':
            #TODO:ロールバック処理
            raise

        # 新規付番されたIDを返す
        return res_exe_statement['generatedFields'][0]['longValue']

    def update(self):
        sql = f"update crud_test set content = :content where id = :id;"
        param = [ {'name': 'id', 'value': { 'longValue': self.id }},
                  {'name': 'content', 'value': { 'stringValue': self.content }},
        ]

        res_begin_transaction = self._rds_begin_transaction()
        tran_id = res_begin_transaction['transactionId']
        res_exe_statement = self._rds_exe_statement(sql, param, tran_id)

        # 1件以上更新されるのはerrorとする
        if res_exe_statement['numberOfRecordsUpdated'] != 1:
            #TODO:ロールバック処理
            raise

        # コミット
        commit_result = self._rds_commit_transaction(tran_id = tran_id)

        return {"updated_id": self.id, "updated_content:": self.content}


    def delete(self):
        sql = f"delete from crud_test where id = :id;"
        param = [{'name': 'id', 'value': { 'longValue': self.id }},]

        res_begin_transaction = self._rds_begin_transaction()
        tran_id = res_begin_transaction['transactionId']
        res_exe_statement = self._rds_exe_statement(sql, param, tran_id)

        # 削除されたかわからないので確認SELECT
        sel_sql = f"select * from crud_test where id = :id"
        sel_exe_statement_responce = self._rds_exe_statement(exe_sql = sel_sql,
                                                   param = param,
                                                   tran_id = tran_id)

        # 更新件数が0件以外の場合はエラー
        if len(sel_exe_statement_responce['records']) != 0:
            #TODO:ロールバック処理
            raise

        # コミット
        res_commit_transaction = self._rds_commit_transaction(tran_id)

        if res_commit_transaction['transactionStatus'] != 'Transaction Committed':
            #TODO:ロールバック処理
            raise

        print(res_exe_statement)
        print(res_commit_transaction)

        return self.id