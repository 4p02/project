from typing import Any, Union, Optional, Sequence, Self, Mapping, Literal
from collections.abc import AsyncIterator

from ollama import AsyncClient, Message, Options, ResponseError, ChatResponse

from backend import config


class Ollama():
    client: AsyncClient

    def __init__(self, client: AsyncClient): self.client = client

    @staticmethod
    async def connect() -> Self:
        client = AsyncClient(config.ollama.endpoint)
        client._client.base_url = config.ollama.endpoint
        if config.ollama.bearer_token is not None:
            client._client.headers = {"Authorization": f"Bearer {config.ollama.bearer_token}"}

        self = Ollama(client)
        models = (model["name"] for model in (await self.client.list())["models"])
        if self.model not in models:
            raise Exception(f"selected model {self.model} is not available on ollama endpoint")

        return self

    @property
    def model(self) -> str: return config.ollama.model

    async def chat(
        self,
        messages: Optional[Sequence[Message]] = None,
        format: Literal['', 'json'] = '',
        **kwargs: Optional[Options],
    ) -> ChatResponse:
        return await self.client.chat(
            model=self.model,
            messages=messages,
            stream=False,
            format=format,
            options=kwargs
        )

    async def chat_stream(
        self,
        messages: Optional[Sequence[Message]] = None,
        format: Literal['', 'json'] = '',
        **kwargs: Optional[Options],
    ) -> AsyncIterator[ChatResponse]:
        return await self.client.chat(
            model=self.model,
            messages=messages,
            stream=True,
            format=format,
            options=kwargs
        )
