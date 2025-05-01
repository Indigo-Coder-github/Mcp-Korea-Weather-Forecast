import argparse
from calendar import c
from datetime import datetime, timedelta

import requests
from mcp.server.fastmcp import FastMCP

from coordination import map_to_grid
from utils import *

# servername
mcp = FastMCP(
    "Korea_Meterological_Administration",
    "This server provides short weather forecasting data for South Korea.",
)

# constants
BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/"
DATA_TYPE = "JSON"

# parser
def parse_args():
    parser = argparse.ArgumentParser(description="Weather Forecasting Server")

    parser.add_argument(
        "--api_key",
        required=True,
        help="API key from data.go.kr"
    )
    
    return parser.parse_args()
    

# tools
@mcp.tool()
async def get_ultra_short_nowcast(latitude: str, longitude: str) -> dict[str, str]:
    '''
    Provides the weather nowcast based on date, time, and coordination.
    '''
    args = parse_args()
    
    current_date, current_time = datetime.now().strftime("%Y%m%d"), datetime.now().strftime("%H%M")
    x, y = map_to_grid(float(latitude), float(longitude))
    url = f"{BASE_URL}getUltraSrtNcst?serviceKey={args.api_key}&pageNo=1&numOfRows=1000&dataType={DATA_TYPE}&base_date={current_date}&base_time={current_time}&nx={x}&ny={y}"
    items = requests.get(url).json()["response"]["body"]["items"]["item"]
    
    result = dict()
    
    for item in items:
        match item["category"]:
            case "PTY":
                match int(item["obsrValue"]):
                    case 0: result["Precipitation Type"] = "None"
                    case 1: result["Precipitation Type"] = "Rain"
                    case 2: result["Precipitation Type"] = "Rain/Snow"
                    case 3: result["Precipitation Type"] = "Snow"
                    case 4: result["Precipitation Type"] = "Sudden Rain"
            case "REH":
                result["Relative Humidity"] = f"{item["obsrValue"]}%"
            case "RN1":
                if item["obsrValue"] == "0": result["Rainfall"] = "None"
                else: result["Rainfall"] = item["obsrValue"]
            case "T1H":
                result["Temperature"] = f"{item["obsrValue"]}°C"
            case "UUU":
                result["East-West Wind Component"] = f"East {item["obsrValue"]} m/s" if float(item["obsrValue"]) > 0 else f"West {item["obsrValue"]} m/s"
            case "VEC":
                result["Wind Direction"] = f"{item["obsrValue"]}°"
            case "VVV":
                result["South-North WInd Component"] = f"North {item["obsrValue"]} m/s" if float(item["obsrValue"]) > 0 else f"South {item["obsrValue"]} m/s"
            case "WSD":
                wind_speed = float(item["obsrValue"])
                if wind_speed < 4: result["Wind Speed"] = "Weak"
                elif 4 <= wind_speed < 9: result["Wind Speed"] = "Little Strong"
                elif 9 <= wind_speed < 14: result["Wind Speed"] = "Strong"
                elif 14 <= wind_speed < 20: result["Wind Speed"] = "Very Strong"
    
    return result

@mcp.tool()
async def get_ultra_short_forecast(latitude: str, longitude: str) -> dict[str, dict[str, str]]:
    '''
    Provides the weather forecast based on date, time, and coordination.
    '''
    args = parse_args()
    
    current_date, current_time = datetime.now().strftime("%Y%m%d"), datetime.now().strftime("%H%M")
    if datetime.strptime(current_time, "%H%M") < datetime.strptime(f"{current_time[:2]}30", "%H%M"):
        if datetime.strptime(current_time, "%H%M") < datetime.strptime("0030", "%H%M"):
            current_date = datetime.strftime(datetime.strptime(current_date, "%Y%m%d") - timedelta(days=1), format="%Y%m%d")
        current_time = datetime.strftime(datetime.strptime(f"{current_time[:2]}30", "%H%M") - timedelta(hours=1), format="%H%M")
    
    x, y = map_to_grid(float(latitude), float(longitude))
    url = f"{BASE_URL}getUltraSrtFcst?serviceKey={args.api_key}&pageNo=1&numOfRows=1000&dataType={DATA_TYPE}&base_date={current_date}&base_time={current_time}&nx={x}&ny={y}"
    items = requests.get(url).json()["response"]["body"]["items"]["item"]
    
    result = {f"{item["fcstDate"]} {item["fcstTime"]}": dict() for item in items}
    
    for item in items:
        match item["category"]:
            case "LGT":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Lightning"] = f"{item["fcstValue"]} kA"
            case "PTY":
                match int(item["fcstValue"]):
                    case 0: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "None"
                    case 1: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Rain"
                    case 2: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Rain/Snow"
                    case 3: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Snow"
                    case 4: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Sudden Rain"
            case "RN1":
                if item["fcstValue"] == "0": result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Rainfall"] = "None"
                else: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Rainfall"] = item["fcstValue"]
            case "SKY":
                match int(item["fcstValue"]):
                    case 1: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Sky Condition"] = "Clear"
                    case 3: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Sky Condition"] = "Cloudy"
                    case 4: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Sky Condition"] = "Overcast"
            case "T1H":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Temperature"] = f"{item["fcstValue"]}°C"
            case "REH":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Relative Humidity"] = f"{item["fcstValue"]}%"
            case "UUU":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["East-West Wind Component"] = f"East {item["fcstValue"]} m/s" if float(item["fcstValue"]) > 0 else f"West {item["fcstValue"]} m/s"
            case "VVV":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["South-North Wind Component"] = f"North {item["fcstValue"]} m/s" if float(item["fcstValue"]) > 0 else f"South {item["fcstValue"]} m/s"
            case "VEC":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Wind Direction"] = f"{item["fcstValue"]}°"
            case "WSD":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Wind Speed"] = f"{item["fcstValue"]} m/s"
        pass
    
    return result

@mcp.tool()
async def get_vilage_forecast(latitude: str, longitude: str) -> dict[str, dict[str, str]]:
    '''
    Provides the 5-days weather forecast based on date, time, and coordination.
    '''
    args = parse_args()
    
    current_date = datetime.now().strftime("%Y%m%d")
    current_time = datetime.now().strftime("%H%M")
    
    standard_date, standard_time = calc_standard_time(current_date, current_time)
    x, y = map_to_grid(float(latitude), float(longitude))
    url = f"{BASE_URL}getVilageFcst?serviceKey={args.api_key}&pageNo=1&numOfRows=1000&dataType={DATA_TYPE}&base_date={standard_date}&base_time={standard_time}&nx={x}&ny={y}"
    items = requests.get(url).json()["response"]["body"]["items"]["item"]
    
    result = {f"{item["fcstDate"]} {item["fcstTime"]}": dict() for item in items}
    
    for item in items:
        match item["category"]:
            case "TMP":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Hourly Temperature"] = f"{item["fcstValue"]}°C"
            case "UUU":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["East-West Wind Component"] = f"East {item["fcstValue"]} m/s" if float(item["fcstValue"]) > 0 else f"West {item["fcstValue"]} m/s"
            case "VVV":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["South-North Wind Component"] = f"North {item["fcstValue"]} m/s" if float(item["fcstValue"]) > 0 else f"South {item["fcstValue"]} m/s"
            case "VEC":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Wind Direction"] = f"{item["fcstValue"]}°"
            case "WSD":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Wind Speed"] = f"{item["fcstValue"]} m/s"
            case "SKY":
                match int(item["fcstValue"]):
                    case 1: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Sky Condition"] = "Clear"
                    case 3: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Sky Condition"] = "Cloudy"
                    case 4: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Sky Condition"] = "Overcast"
            case "PTY":
                match int(item["fcstValue"]):
                    case 0: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "None"
                    case 1: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Rain"
                    case 2: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Rain/Snow"
                    case 3: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Snow"
                    case 4: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation Type"] = "Sudden Rain"
            case "POP":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Probability of Precipitation"] = f"{item["fcstValue"]}%"
            case "WAV":
                if item["fcstValue"] == "-999": result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Wave Height"] = "None"
                else: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Wave Height"] = f"{item["fcstValue"]} m"
            case "PCP":
                if item["fcstValue"] == "0": result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation"] = "None"
                else: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Precipitation"] = item["fcstValue"]
            case "REH":
                result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Relative Humidity"] = f"{item["fcstValue"]}%"
            case "SNO":
                if item["fcstValue"] == "0": result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Snowfall"] = "None"
                else: result[f"{item["fcstDate"]} {item["fcstTime"]}"]["Snowfall"] = item["fcstValue"]
    
    return result

# Start the server
if __name__ == "__main__":
    print("Starting the server...")
    mcp.run()
    print("Server started.")