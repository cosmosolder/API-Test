# API Tool using FastMCP
# This script provides a FastMCP server that allows users to upload any API call, with argument payload, and get the results
import sys
from typing import Any
import httpx
from anthropic import Anthropic
from mcp.server.fastmcp import FastMCP
import requests
import json

# Initialize FastMCP server
mcp = FastMCP("api-test", description="API Testing Tool using FastMCP", version="1.0.0")

# Constants
url = "https://excel.uat.us.coherent.global/presales/api/v3/folders/Solder-Test/services/mortgage-amort-calculator/execute"

payload = json.dumps({
   "request_data": {
      "inputs": {
         "ExtraPrincPmt": 100,
         "InterestRate": 0.05,
         "Lender": "Wells Fargo",
         "LoanStartDate": "2025-05-28",
         "LoanTermYrs": 30,
         "OrigLoanAmt": 200000,
         "PaymentsPerYear": 12
      }
   },
   "request_meta": {
      "version_id": "aeffe1e2-529b-4c2f-9755-5473a391aa83",
      "transaction_date": None,
      "call_purpose": None,
      "source_system": None,
      "correlation_id": None,
      "service_category": "",
      "requested_output": None
   }
})
headers = {
   'Content-Type': 'application/json',
   'x-tenant-name': 'presales',
   'x-synthetic-key': '46ac56eb-90ea-4570-80c3-4750ffae5874'
}

#response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

@mcp.tool()
def call_api(
    endpoint: str = url,
    method: str = "POST",
    params: dict = None,
    data: dict = payload,
    headers: dict = headers
) -> dict:
    """
    Calls an arbitrary API endpoint with the specified method and arguments.
    Returns the JSON response or text.
    """
    try:
        response = requests.request(
            method=method,
            url=endpoint,
            params=params,
            json=data,
            headers=headers
        )
        try:
            print(response.text)
            return {"status_code": response.status_code, "json": response.json()}
        except Exception:
            return {"status_code": response.status_code, "text": response.text}
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    # Initialize and run the server
    #mcp.run(transport='stdio')
    print('IN API-Test.PY +++++++++++++++++++++++', file=sys.stderr)
    print('API',url, file=sys.stderr)
