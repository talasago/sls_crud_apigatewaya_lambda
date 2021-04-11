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

    def _rds_commit_transaction(self,tran_id):
        return rdsData.commit_transaction(
                            resourceArn = cluster_arn,
                            transactionId = tran_id,
                            secretArn = secret_arn,
                            )

    # AuroraServerlessへのsql実行メソッド
    def _rds_exe_statement(self,exe_sql, param = [], tran_id=None):
        return rdsData.execute_statement(
                        resourceArn = cluster_arn,
                        secretArn = secret_arn,
                        database = database_name,
                        sql = exe_sql,
                        parameters = param,
                        transactionId = tran_id)

    def insert(self, exe_sql, param):
        res_begin_transaction = self._rds_begin_transaction()
        tran_id = res_begin_transaction['transactionId']

        res_exe_statement = self._rds_exe_statement(exe_sql,param,tran_id)

        res_commit_transaction = self._rds_commit_transaction(tran_id)

        print(res_exe_statement)
        print(res_commit_transaction)

        if res_commit_transaction['transactionStatus'] != 'Transaction Committed':
            #TODO:ロールバック処理
            raise

        # 新規付番されたIDを返す
        return res_exe_statement['generatedFields'][0]['longValue']
