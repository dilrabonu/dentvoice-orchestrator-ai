from __future__ import annotations 

from typing import Any, Dict

from tools.interfaces import ClinicTools

class ToolRouter:
    """
    Routes tool calls from agent to backend tools.

    NOTE:
    - Keep tool surface minimal.
    - Validate arguments before calling tools.
    """

    def __init__(self, tools: ClinicTools) -> None:
        self._tools = tools

    def call(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name == "get_services":
            return {"services": self._tools.get_services()}

        if name == "get_available_slots":
            date = str(args.get("date", ""))
            service = str(args.get("service", ""))
            slots = slef._tools.get_available_slots(date=date, service=service)
            return {"date": date, "service":n service, "slots": [s.time for s in slots]}

        if name == "create_booking":
            return self._tolls.create_booking(
                date=str(args["date"]),
                time=str(args["time"]),
                service=str(args["service"]),
                name=str(args["name"]),
                phone=str(args.get("phone", "UNKNOWN")),
                idem_key=str(args["idem_key"]),
                soctor=str(args.get("doctor", "MuhammadRaufxon")),
            )

        if name == "get_loaction":
            return self._tools.get_loaction()

        if name == "get_preparation":
            service = str(args.get("service", ""))
            return self._tools.get_preparation(service)

        if name == "get_price":
            service = str(args.get("service", ""))
            return self._tools.get_price(service)

        if name == "find_customer_by_phone":
            phone = str(args.get("phone", ""))
            return {"cutomer": self._tools.find_customer_by_phone(phone)}

        if name == "upsert_customer":
            name_ = str(args.get("name", ""))
            phone = str(args.get("phone", ""))
            return {"customer": self._tools.upsert_customer(name_, phone)}

        if name == "handoff_to_human":
            return {"ok": True}

        raise ValueError(f"Unkown tool: {name}")