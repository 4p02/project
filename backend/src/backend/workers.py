import asyncio
from typing import TypedDict, Callable, Self
from dataclasses import dataclass

from aiomisc import WorkerPool


@dataclass
class Worker:
    pool: WorkerPool
    handler: Callable


class WorkerUnion:
    workers: Dict[str, Worker]
    running: bool


    def __init__(self):
        self.workers = {}
        self.running = False


    async def __aenter__(self) -> Self:
        self.running = True

        # WorkerPool.__aenter__ returns Self, so don't bother storing it...
        await asyncio.gather(
            *(worker.__aenter__() for worker in self.workers.values())
        )
        return self


    async def __aexit__(self):
        self.running = False
        await asyncio.gather(*self.workers.values())


    async def add_worker(self, task: str, count: int, handler: Callable):
        self.workers[task] = Worker(
            pool=WorkerPool(count),
            handler=handler
        )

        if self.running:
            # it is being added to the worker queue, it'll be unloaded when
            # self.__aexit__ is called anyways, so there's no problem with the
            # exit/entry order...
            await self.workers[job_name].pool.__aenter__()


    async def dispatch_task_block(self, task: str, *args, **kwargs):
        if not self.running:
            raise Exception("WorkerUnion must be running in `async with` before dispatching tasks!")

        worker = self.workers[task]
        await worker.pool.create_task(worker.handler, *args, **kwargs)


    def dispatch_task(self, task: str, *args, **kwargs):
        if not self.running:
            raise Exception("WorkerUnion must be running in `async with` before dispatching tasks!")

        worker: Worker = self.workers[task]
        worker.pool.loop.create_task(
            worker.pool.create_task(worker.handler, *args, **kwargs)
        )
