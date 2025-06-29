from pathlib import Path

DATA_INPUT_FOLDER = Path(__file__).parent / "data" / "inputs"

GET_DATA_API_ENDPOINT = "/get_data/"

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

order_forcecast_schema = {
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

