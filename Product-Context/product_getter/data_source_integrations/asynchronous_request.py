import asyncio
from enum import Enum
import logging
import time
from typing import Any, Dict, List
import aiohttp
from fn_utils import colored

Method = Enum('Method', ['GET', 'POST', 'DELETE'])

class ShipperRequest():
  
  def __init__(self): 
      self.log = logging.getLogger(__name__)
      self.log.info(f"ShipperRequest class called")
      self.list_result:List[Dict[str, Any]] = []
      self.asyncQueueRequest = asyncio.Queue()
      self.n_workers:int = 6 
  
  async def producer( self, 
                      data_producer: List[Dict[str, str]]):
      
    session  = aiohttp.ClientSession()
    
    if data_producer:
        for dict_request in data_producer:
            print(dict_request)
            self.asyncQueueRequest.put_nowait(dict_request)
        # Create (n_workers:int) worker tasks to process the queue concurrently.
        tasks = []

        total_task_to_do:int = len(data_producer)
        if total_task_to_do < self.n_workers:
            self.n_workers = total_task_to_do

        for _ in range(self.n_workers):
            task = asyncio.create_task(self.request_worker(session))
            tasks.append(task)

        started_at = time.monotonic()
        await self.asyncQueueRequest.join()
        total_slept_for = time.monotonic() - started_at
        print(colored("All queueRequest done !", "yellow"))
        await session.close()
        print(colored("session client aiohttp closed", "yellow"))
        print(colored(255, 255, 0, "session client aiohttp closed"))

        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are cancelled.
        await asyncio.gather(*tasks, return_exceptions=True)
        print(colored(255, 155, 0, "======================================"))
        print(colored(255, 155, 0,f'{self.n_workers} workers slept in parallel for {total_slept_for:.2f} seconds'))

    async def request_worker(self, session):
        while True:
                data_request:Dict[str, str] = await self.asyncQueueRequest.get()

                await self.request_post(data_request=data_request,
                                        session=session)

            
            
        

    async def request_post( self,
                            data_request: any,
                            session:aiohttp.ClientSession,
                            method=Method.POST
                            ) -> Dict:
        try:
            
            url = data_request.get("url")
            headers = data_request.get("headers")
            data_request = data_request.get("data")
                        
            if method == Method.POST :
                async with session.post(url=url, headers=headers, data=data_request) as response_post:
                    response = await response_post.json()

            elif method == Method.GET:
                async with session.get(url=url, headers=headers, data=data_request) as response_get:
                    response = await response_get.json()
            
            
            self.list_result.append(response)       
            self.asyncQueueRequest.task_done()

        except aiohttp.ClientConnectorError as e:
            self.asyncQueueRequest.task_done()

      