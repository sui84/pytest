from winevt import EventLog
query = EventLog.Query("System","Event/System[EventID=27035]")
event = next(query)