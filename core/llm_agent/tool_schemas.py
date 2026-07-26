TOOL_SCHEMAS = [
    {
        "name": "get_services",
        "description": "List available dental services offered by the clinic",
        "input_schema": {"type": "object", "properties": {}},

    },
    {
        "name": "get_available_slots",
        "description": "Get available appointment slots for a given date and service.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date, e.g. 2026-07-15 or 'ertaga'"},
                "service": {"type": "string", "enum": ["konsultatsiya", "tish davolash", "tish tozalash"]},
            },
            "required": ["date", "service"],
        },
    },
    {
        "name": "create_booking",
        "description": "Cerate a booking. MUST be called only after explicit user confirmation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "doctor": {"type": "string"},
                "service": {"type": "string"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "customer_name": {"type": "string"},
                "customer_phone": {"type": "string"},
                "idem_key": {"type": "string", "description": "call_id:turn_id:create_booking"},
            },
            "required": ["doctor", "service", "date", "time", "customer_name", "customer_phone", "idem_key"],
        },
    },
    {
        "name": "get_price",
        "description": "Get the price for a given service.",
        "input_schema": {
            "type": "object",
            "properties": {"service": {"type": "string"}},
            "required": ["service"],
        },
    },
    {}
        }
     
    
]