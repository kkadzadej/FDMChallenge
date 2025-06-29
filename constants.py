from pathlib import Path

DATA_INPUT_FOLDER = Path(__file__).parent / "data" / "inputs"

GET_DATA_API_ENDPOINT = "/get_data/"
POST_RESULT_API_ENDPOINT = "/september_batches/"

PRODUCT_GRADE_MAPPING = {
"Rebar": ["B500A", "B500B", "B500C"],
"MBQ": ["A36", "A5888", "GR50", "44W", "50W", "55W", "60W"],
"SBQ": ["S235JR", "S355J", "C35", "C40"],
"CHQ": ["A53/A543","A53/C591"]
}

daily_charge_schedule_schema = {
    "Start time": {
        "type": "DateTime",
        "index": True,
        "primary_key": True
    },
    "Grade": {
        "type": "String"
    },
    "Mould size": {
        "type": "Float"
    }
}

product_groups_monthly_schema = {
    "date": {
        "type": "DateTime",
        "index": True,
        "primary_key": True
    },
    "Rebar": {
        "type": "Float"
    },
    "MBQ": {
        "type": "Float"
    },
    "SBQ": {
        "type": "Float"
    },
    "CHQ": {
        "type": "Float"
    }
}

steel_grade_production_schema = {
    "date": {
        "type": "DateTime",
        "index": True,
        "primary_key": True
    },
    "B500A": {
        "type": "Float"
    },
    "B500B": {
        "type": "Float"
    },
    "B500C": {
        "type": "Float"
    },
    "A36": {
        "type": "Float"
    },
    "A5888": {
        "type": "Float"
    },
    "GR50": {
        "type": "Float"
    },
    "44W": {
        "type": "Float"
    },
    "50W": {
        "type": "Float"
    },
    "55W": {
        "type": "Float"
    },
    "60W": {
        "type": "Float"
    },
    "S235JR": {
        "type": "Float"
    },
    "S355J": {
        "type": "Float"
    },
    "C35": {
        "type": "Float"
    },
    "C40": {
        "type": "Float"
    },
    "A53/A543": {
        "type": "Float"
    },
    "A53/C591": {
        "type": "Float"
    }
}

DAILY_CHARGE_SCHEDULE = "daily_charge_schedule"
PRODUCT_GROUP_MONTHLY = "product_groups_monthly"
STEEL_GRADE_PRODUCTION = "steel_grade_production"

db_schema = {
    f"{DAILY_CHARGE_SCHEDULE}_schema": daily_charge_schedule_schema,
    f"{PRODUCT_GROUP_MONTHLY}_schema": product_groups_monthly_schema,
    f"{STEEL_GRADE_PRODUCTION}_schema": steel_grade_production_schema
}

