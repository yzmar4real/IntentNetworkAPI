from fastapi import FastAPI
from genie.testbed import load
import logging
import json

logging.basicConfig(level=logging.DEBUG)

testbed = load('./genie.yml')

app = FastAPI()

@app.get("/v1/route_check")
def root():

    for dev in testbed:
         
        dev.connect(learn_hostname=True,init_exec_commands=[],init_config_commands=[],log_stdout=True)

        try:
            routes = dev.api.get_routes()
            if '0.0.0.0/0' in routes:
                 Status = True
                # return {"Device_Name": dev.hostname, "Output": 'Default_Route_Present', "Code": '0'}
            else:
                 Status = False
                # return {"Device_Name": dev.hostname, "Output": 'Default_Route_Absent', "Code": 1}
        except Exception as e:
                Status = f"Not reacheable with error {e}"
                # logging.exception({"Device_Name": dev.hostname, "Output": 'Default_Route_Absent', "Code": 1})

    return{"Default Route Results": Status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3443)

