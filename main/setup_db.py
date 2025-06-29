from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, Boolean
)
from typing import Dict, Any, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from constants import db_schema, DAILY_CHARGE_SCHEDULE, PRODUCT_GROUP_MONTHLY, STEEL_GRADE_PRODUCTION

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# Mapping string names to SQLAlchemy types
SQLALCHEMY_TYPE_MAP = {
    "Integer": Integer,
    "String": String,
    "Text": Text,
    "DateTime": DateTime,
    "Float": Float,
    "Boolean": Boolean
}

class DB:

    def create_tables(self):
        """
        Create the db tables based on the schemas in constants.py
        """

        Orders = self.create_model(STEEL_GRADE_PRODUCTION, db_schema[f"{STEEL_GRADE_PRODUCTION}_schema"])
        ProductionHistory = self.create_model(PRODUCT_GROUP_MONTHLY, db_schema[f"{PRODUCT_GROUP_MONTHLY}_schema"])
        DailyChargeSchedule = self.create_model(DAILY_CHARGE_SCHEDULE, db_schema[f"{DAILY_CHARGE_SCHEDULE}_schema"])

        Base.metadata.create_all(bind=engine)

    def write_files_to_db_tables(self, files: {}):
        """
        Method that creates the database tables them and writes the data to them
        """

        db_tables = DB()
        db_tables.create_tables()

        for filename, file in files.items():
            file.to_sql(f"{filename}_1", con=engine, if_exists="replace", index=False)

    @staticmethod
    def create_model(name: str, schema: Dict[str, Dict[str, Any]]) -> Type[Base]:
        """
        Dynamically creates a SQLAlchemy model class.

        :param name: Name of the model/table.
        :param schema: Dict of column definitions.
        :return: SQLAlchemy model class.
        """
        attrs = {
            '__tablename__': name,
            '__table_args__': {'extend_existing': True}
        }

        for column_name, options in schema.items():
            column_type = options.get("type")
            col_type = SQLALCHEMY_TYPE_MAP[column_type]
            col_args = {}
            if "primary_key" in options:
                col_args["primary_key"] = options["primary_key"]
            if "index" in options:
                col_args["index"] = options["index"]

            attrs[column_name] = Column(col_type, **col_args)

        return type(name, (Base,), attrs)
