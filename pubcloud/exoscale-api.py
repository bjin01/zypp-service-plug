from collections import abc
import base64
import hashlib
import hmac
import json
import requests
from urllib.request import urlopen
from urllib.parse import quote, urlencode

API_KEY = "EXOc06c3bbb964cef9bdf82349d"
API_SECRET= "Uyo8BpMmfdmYpm6Shy8cD8e2T2FhLBbsw_T2ro0Qqys"

COMPUTE_ENDPOINT = "https://api.exoscale.ch/compute"

def sign(command, secret):
  """Adds the signature bit to a command expressed as a dict"""
  # order matters
  arguments = sorted(command.items())

  # urllib.parse.urlencode is not good enough here.
  # key contains should only contain safe content already.
  # safe="*" is required when producing the signature.
  query_string = "&".join("=".join((key, quote(value, safe="*")))
                          for key, value in arguments)

  # Signing using HMAC-SHA1
  digest = hmac.new(
      secret.encode("utf-8"),
      msg=query_string.lower().encode("utf-8"),
      digestmod=hashlib.sha1).digest()

  signature = base64.b64encode(digest).decode("utf-8")

  return dict(command, signature=signature)


# The command contains the apikey and the parameters
command = {
  "command":           "listVirtualMachines",
  "apikey":            API_KEY,
}

# Signing the request and URL encoding it
params = sign(command, API_SECRET)
query_string = urlencode(params)
endurl = COMPUTE_ENDPOINT + "?" + query_string
# As GET
response = requests.get(endurl)
json_response = response.json()
print(type(json_response))
for h, i in json_response.items():
     print(type(h), type(i))
     if isinstance(h, str):
         try:
             res = json.loads(h)
             #print(res)
             if isinstance(res, dict):
                 for k, v in res.items():
                     print(k, v)
         except:
             print(h)

     if isinstance(i, dict):
         for x, y in i.items():
             print(type(x), type(y))
             try:
                 res = json.loads(x)
                 for a, b in res.items():
                     print(type(a), type(b))
                     try:
                         res = json.loads(a)
                         if isinstance(a, dict):
                             for k, v in a.items():
                                 print(k, v)
                     except:
                          print(a)
             except:
                 print(x)

