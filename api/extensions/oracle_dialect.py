from sqlalchemy.dialects.oracle.base import OracleDialect
import oracledb

class OracleDialect_oracledb(OracleDialect):
    driver = 'oracledb'

    @classmethod
    def dbapi(cls):
        return oracledb

    def create_connect_args(self, url):
        kwargs = url.translate_connect_args()
        kwargs.setdefault('host', url.host)
        kwargs.setdefault('port', url.port)
        kwargs.setdefault('service_name', url.database)
        return [], kwargs

    def is_disconnect(self, e, connection, cursor):
        return isinstance(e, oracledb.InterfaceError) and "not connected" in str(e).lower()

# 注册新的方言  #Arthur 我取消注册
#from sqlalchemy.dialects import registry
#registry.register("oracle.oracledb", "oracle_dialect", "OracleDialect_oracledb")