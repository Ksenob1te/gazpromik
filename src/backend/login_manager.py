import json

# TODO: install fastapi_login normally
from fastapi_login import LoginManager

from src.database import sessionmanager
from src.database import UserRepository
from src.exceptions import NotAuthenticatedException
from src.enviroments import SECRET_KEY
from uuid import UUID

manager = LoginManager(SECRET_KEY, token_url='/api/auth/login',
                       use_cookie=True, not_authenticated_exception=NotAuthenticatedException)


# TODO: stopped here
@manager.user_loader()
async def load_user(user_str: str):  # could also be an asynchronous function
    async with sessionmanager.session() as session:
        user_repository = UserRepository(session)
        user: dict = json.loads(user_str)
        user_id = user.get("ID", None)
        secret = user.get("Secret", None)
        if user_id is None or user is None:
            return None
        profile = await user_repository.get_by_id(user_id)
        if profile is None:
            return None
        if profile.secret == secret:
            return profile
        return None
