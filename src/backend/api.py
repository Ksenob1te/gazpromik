from fastapi import APIRouter

from .controllers import *

router = APIRouter(
    prefix="/api",
)

router.include_router(UserController.create_router())
router.include_router(AuthController.create_router())
router.include_router(CompanyController.create_router())
