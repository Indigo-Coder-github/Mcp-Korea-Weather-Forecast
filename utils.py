from datetime import datetime, timedelta

def calc_standard_time(current_date: str, current_time: str) -> tuple[str, str]:
    available_times = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]
    
    for idx, time in enumerate(available_times):
        if datetime.strptime(current_time, "%H%M") < (datetime.strptime(time, "%H%M") + timedelta(minutes=11)):
            if idx == 0:
                return ((datetime.strptime(current_date, "%Y%m%d") -
                        timedelta(days=1)).strftime("%Y%m%d"), available_times[-1])
            else:
                return current_date, available_times[idx - 1]