from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from DataBase.models.key_data import KeyData
from DataBase.models.profile import Profile
from DataBase.models.workspace import Workspace
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.repository.lobby_repository import LobbyRepository