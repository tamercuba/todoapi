import pytest

from src import main

pytestmark = pytest.mark.asyncio


async def test_main():
    assert main() == 1
