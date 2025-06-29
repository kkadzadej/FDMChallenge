from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, Boolean
)
from typing import Dict, Any, Type
from setup_db import Base, engine, SessionLocal
from constants import db_schema, DAILY_CHARGE_SCHEDULE, PRODUCT_GROUP_MONTHLY, STEEL_GRADE_PRODUCTION
import os

# Mapping string names to SQLAlchemy types
SQLALCHEMY_TYPE_MAP = {
    "Integer": Integer,
    "String": String,
    "Text": Text,
    "DateTime": DateTime,
    "Float": Float,
    "Boolean": Boolean
}

class DBTables:

    def create_tables(self):
        """
        Create the db tables based on the schemas in constants.py
        """

        Orders = self.create_model("steel_grade_production_schema", db_schema[f"{STEEL_GRADE_PRODUCTION}_schema"])
        ProductionHistory = self.create_model("product_groups_monthly_schema", db_schema[f"{PRODUCT_GROUP_MONTHLY}_schema"])
        DailyChargeSchedule = self.create_model("daily_charge_schedule", db_schema[f"{DAILY_CHARGE_SCHEDULE}_schedule"])

        Base.metadata.create_all(bind=engine)

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

if __name__ == "__main__":

    create_tables = DBTables()
    create_tables.create_tables()
