from typing import Optional

from fastapi import Depends
# TODO: install fastapi_controller normally
from fastapi_controllers import Controller, get
from pydantic import BaseModel

from src.database import get_db_session
from src.database import User
# from DataBase.models.workspace_profile import WorkspaceProfile
from src.database.scheme import UserScheme
# from DataBase.schemes.workspace_profile import WorkspaceProfileScheme
from Site.loginManager import manager
from Site.service.workspace_profile_service import WorkspaceProfileService
from Site.utils import get_workspace_profile

class UserController(Controller):