from aiohttp import ClientSession
from asyncio import Lock, sleep, run
from collections import defaultdict
from datetime import datetime, timedelta
from os import name
from ujson import dumps
 
class StackSession:
    def __init__(self):
        if name == 'posix':
            from uvloop import install
            install()
    
        self.backoffs = defaultdict(datetime.now)
        self.calls = 0
        self.lock = Lock()
        self.session = ClientSession(json_serialize=dumps)
    
    async def __aenter__(self):
        await self.session.__aenter__()
        return self
    
    async def __aexit__(self, *args):
        await self.session.__aexit__(*args)
        await sleep(.25)
 
    async def get(self, method, **params):
        while datetime.now() < self.backoffs[method]:
            await sleep((self.backoffs[method] - datetime.now()).total_seconds())
 
        async with self.lock:
            if self.calls > 15:
                await sleep(1)
                self.calls = 0
        self.calls += 1
 
        params['site'] = 'stackoverflow'
        async with self.session.get('https://api.stackexchange.com/2.3/' + method, params=params) as response:
            if response.ok:
                response = await response.json()
                self.backoffs[method] = max(datetime.now() + timedelta(response.get('backoff', 0)), self.backoffs[method])
                return response
 
async def test():
    async with StackSession() as session:
        json = await session.get('search', tagged='react-dates', pagesize=100, page=1)
        json2 = await session.get('search', pagesize=100, intitle='react-dates', nottagged='react-dates', page=1)
        # json = await session.get('search/advanced', tagged='react-dates', closed='True')
        if (json is not None):
            print(len(json['items']))
            print(json)
        if (json2 is not None):
            print(len(json2['items']))
 
run(test())