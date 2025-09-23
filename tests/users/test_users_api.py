
from src.auth.routers import get_user_by_name
from httpx import ASGITransport, AsyncClient

import pytest
pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"