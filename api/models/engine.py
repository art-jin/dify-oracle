from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import oracledb


#POSTGRES_INDEXES_NAMING_CONVENTION = {
#    "ix": "%(column_0_label)s_idx",
#    "uq": "%(table_name)s_%(column_0_name)s_key",
#    "ck": "%(table_name)s_%(constraint_name)s_check",
#    "fk": "%(table_name)s_%(column_0_name)s_fkey",
#    "pk": "%(table_name)s_pkey",
#}

#metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

# 保留原有索引命名约定
DB_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=DB_INDEXES_NAMING_CONVENTION)
db = SQLAlchemy(metadata=metadata)
