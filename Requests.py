# Requests ~ 12/12/21; December 12, 2021

import requests as Requests

Toyhouse = 'https://Toyhouse.novan1ty.repl.co'
Endpoint = '/registration'
Queries = 'username=PixelLeaf'

Response = Requests.get(f'{Toyhouse + Endpoint}?{Queries}')
# print(Response)

print(Response.text)