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
                
            }
        }
     
    
]