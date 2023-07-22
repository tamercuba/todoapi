from typing import Protocol, TypeVar

from pydantic import BaseModel

IRequest = TypeVar("IRequest", bound=BaseModel, contravariant=True)
IResponse = TypeVar("IResponse", covariant=True)


class IUseCase(Protocol[IRequest, IResponse]):
    async def handle(self, data: IRequest) -> IResponse:
        ...
