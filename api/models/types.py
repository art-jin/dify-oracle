import json

from sqlalchemy import CHAR, Index, Text, TypeDecorator
from sqlalchemy import JSON as SAJSON
from sqlalchemy.dialects.mysql import JSON as MYSQL_JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import JSONB, UUID
#from sqlalchemy.types import TypeDecorator, CHAR, UUID ##Arthur:Oracle
from sqlalchemy.dialects.oracle import RAW ##Arthur:Oracle
import uuid ##Arthur:Oracle

##Oracle:MySQL/Oracle
##这个实现假设你的 Oracle 数据库支持 RAW 类型。在实际使用前，请在你的 Oracle 环境中测试这个实现，以确保它能正确工作。
class StringUUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "oracle":#Arthur:Oracle
            if isinstance(value, uuid.UUID):
                return value.bytes
            elif isinstance(value, str):
                return uuid.UUID(value).bytes
            else:
                return uuid.uuid4().bytes  # 生成新的UUID
        elif dialect.name in {"postgresql", "mysql"}:
            return str(value)
        else:
            return value.hex

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        elif dialect.name == "oracle":
            return dialect.type_descriptor(RAW(16))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "oracle":
            if isinstance(value, bytes):
                return str(uuid.UUID(bytes=value))
            else:
                return str(uuid.UUID(value))
        return str(value)


import json
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON as SAJSON
from sqlalchemy.dialects.mysql import JSON as MYSQL_JSON
from sqlalchemy.dialects.oracle import CLOB

class AdjustedJSON(TypeDecorator):
    """
    Adjusted JSON type for PostgreSQL, MySQL, and Oracle.
    It is treated as JSONB in PostgreSQL, JSON in MySQL, and CLOB in Oracle.
    """
    impl = SAJSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return json.dumps(value)

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB)
        elif dialect.name == "mysql":
            return dialect.type_descriptor(MYSQL_JSON)
        elif dialect.name == "oracle":
            return dialect.type_descriptor(CLOB)
        else:
            raise NotImplementedError(f"Unsupported dialect: {dialect.name}")

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        print(f"Type of value: {type(value)}")
        print(f"Value content: {value}")
        if dialect.name == "oracle":
            # Oracle returns CLOB, which needs to be read
            # Check if value is a CLOB or a string
            if hasattr(value, 'read'):
                return json.loads(value.read())
            else:
                return json.loads(value)
            #return json.loads(value.read())
        return json.loads(value)



###Arthur:Oracle
from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.oracle import CLOB

class AdaptiveText(TypeDecorator):
    """
    Adaptive Text type for PostgreSQL, MySQL, and Oracle.
    It is treated as TEXT in PostgreSQL, LONGTEXT in MySQL, and CLOB in Oracle.
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(Text)
        elif dialect.name == "mysql":
            return dialect.type_descriptor(LONGTEXT)
        elif dialect.name == "oracle":
            return dialect.type_descriptor(CLOB)
        else:
            raise NotImplementedError(f"Unsupported dialect: {dialect.name}")


"""
class PostgresJSONIndex(Index):
    JSON index for PostgreSQL.
    This should be ignored in MySQL, because MySQL does not support indexing JSON column directly.
    Reference: https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html#json-column-indirect-index
    It's required to modify the index creation statement for this index in the migration script.

    pass
"""
##这个实现假设你的 Oracle 数据库版本支持 JSON 操作。
from sqlalchemy import Index
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement

class CreateOracleJSONIndex(DDLElement):
    def __init__(self, name, table, column):
        self.name = name
        self.table = table
        self.column = column

@compiles(CreateOracleJSONIndex, 'oracle')
def compile_oracle_json_index(element, compiler, **kw):
    return (
        f"CREATE INDEX {element.name} ON {element.table} "
        f"(json_value({element.column}, '$' returning VARCHAR2(4000) ERROR ON ERROR))"
    )

class PostgresJSONIndex(Index):
    """
    JSON index for PostgreSQL and Oracle.
    This will be ignored in MySQL, as MySQL does not support indexing JSON columns directly.
    For PostgreSQL, it creates a GIN index.
    For Oracle, it creates a function-based index on JSON data.
    """
    def __init__(self, name, column, **kw):
        self.name = name
        self.column = column
        self.kw = kw
        super(PostgresJSONIndex, self).__init__(name, column, **kw)

    def create(self, bind=None, checkfirst=False):
        if bind.dialect.name == 'postgresql':
            Index(self.name, self.column, postgresql_using="gin").create(bind, checkfirst)
        elif bind.dialect.name == 'oracle':
            CreateOracleJSONIndex(
                self.name,
                self.table.name,
                self.column.name
            ).execute(bind)
        # For MySQL, we do nothing as it doesn't support direct JSON indexing

    def drop(self, bind=None, checkfirst=False):
        if bind.dialect.name in ['postgresql', 'oracle']:
            bind.execute(text(f"DROP INDEX {self.name}"))
        # For MySQL, we do nothing as it doesn't support direct JSON indexing

