from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from models.user import UserRegistrationForm, UserFull
from sqlmodel import select
from database import get_session
from forms import OAuth2UsernamePasswordRequestForm
from utils.auth import authenticate_user, get_password_hash, get_user
from fastapi_utils.cbv import cbv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
router = APIRouter(prefix="/api/auth", tags=["authentication"])


@cbv(router)
class AuthRouter:
    @router.post("/token")
    async def login(self, form_data: OAuth2UsernamePasswordRequestForm = Depends(),
                    session: AsyncSession = Depends(get_session)):
        user = await authenticate_user(form_data.username, form_data.password, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"access_token": user.username, "token_type": "bearer"}

    @router.get("/users/me")
    async def read_users_me(self, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
        user = await get_user(token, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user

    @router.post("/register")
    async def register(self, user_form: UserRegistrationForm, session: AsyncSession = Depends(get_session)):
        async with session.begin():
            result = await session.execute(select(UserFull).where(UserFull.username == user_form.username))
        user = result.scalars().first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        hashed_password = get_password_hash(user_form.password)
        user_to_db = UserFull(
            username=user_form.username,
            email=user_form.email,
            full_name=user_form.email,
            hashed_password=hashed_password,
            disabled=False,
        )
        async with session.begin():
            session.add(user_to_db)
        return {"msg": "User registered successfully"}


auth_router = router
