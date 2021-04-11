import json
import os
import boto3


class RdsConnect :
    rdsData       = boto3.client('rds-data')
    cluster_arn   = os.environ['CLUSTER_ARN']
    secret_arn    = os.environ['SECRET_ARN']
    database_name = os.environ['DATABASE_NAME']
    schema_name   = os.environ['SCHEMA_NAME']

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
    def _rds_exe_statement(self,exe_sql, param = None, tran_id=None):
        return rdsData.execute_statement(
                        resourceArn = cluster_arn,
                        secretArn = secret_arn,
                        database = database_name,
                        sql = exe_sql,
                        parameters = param,
                        transactionId = tran_id)

    # transactionを貼ってsqlを実行する必要がある用
    def transaction_access_to_exe_statement(self):
        tran_id  = self._rds_begin_transaction()
        result = self._rds_exe_statement(tran_id)
        tran_result = self._rds_commit_transaction(tran_id)
        return result

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
