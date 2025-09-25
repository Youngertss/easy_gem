import pytest
from httpx import ASGITransport, AsyncClient

from src.auth.routers import get_user_by_name

pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"
