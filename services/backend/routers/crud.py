from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from models.advertisment import Advertisement, AdvertisementUpdate
from database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from utils.auth import get_user
from fastapi_utils.cbv import cbv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
router = APIRouter(prefix="/api/ads", tags=["advertisements"])


@cbv(router)
class AdvertisementRouter:
    @router.post("/advertisements/", response_model=Advertisement)
    async def create_advertisement(self, advertisement: Advertisement, session: AsyncSession = Depends(get_session),
                                   token: str = Depends(oauth2_scheme)):
        user = await get_user(token, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        # Check if ad_id already exists
        result = await session.exec(select(Advertisement).where(Advertisement.ad_id == advertisement.ad_id))
        existing_advertisement = result.one_or_none()
        if existing_advertisement is not None:
            raise HTTPException(status_code=400, detail="Advertisement with this ad_id already exists")

        try:
            session.add(advertisement)
            await session.commit()
            await session.refresh(advertisement)
            return advertisement
        except Exception as e:
            raise HTTPException(status_code=400, detail="Advertisement key violates model")

    @router.get("/advertisements/", response_model=list[Advertisement])
    async def read_all_advertisements(self, session: AsyncSession = Depends(get_session),
                                      token: str = Depends(oauth2_scheme)):
        user = await get_user(token, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        result = await session.exec(select(Advertisement))
        advertisements = result.all()
        return advertisements

    @router.get("/advertisements/{ad_id}", response_model=Advertisement)
    async def read_advertisement(self, ad_id: int, session: AsyncSession = Depends(get_session),
                                 token: str = Depends(oauth2_scheme)):
        user = await get_user(token, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        result = await session.exec(select(Advertisement).where(Advertisement.ad_id == ad_id))
        advertisement = result.one_or_none()
        if advertisement is None:
            raise HTTPException(status_code=404, detail="Advertisement not found")
        return advertisement

    @router.put("/advertisements/{ad_id}", response_model=Advertisement)
    async def update_advertisement(self, ad_id: int, advertisement_update: AdvertisementUpdate,
                                   session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
        user = await get_user(token, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        if advertisement_update.ad_id is not None and advertisement_update.ad_id != ad_id:
            result = await session.exec(select(Advertisement).where(Advertisement.ad_id == advertisement_update.ad_id))
            existing_advertisement = result.one_or_none()
            if existing_advertisement is not None:
                raise HTTPException(status_code=400, detail="Advertisement with this ad_id already exists")

        result = await session.exec(select(Advertisement).where(Advertisement.ad_id == ad_id))
        db_advertisement = result.one_or_none()
        if db_advertisement is None:
            raise HTTPException(status_code=404, detail="Advertisement not found")

        for key, value in advertisement_update.dict(exclude_unset=True).items():
            setattr(db_advertisement, key, value)

        session.add(db_advertisement)
        await session.commit()
        await session.refresh(db_advertisement)
        return db_advertisement

    @router.delete("/advertisements/{ad_id}", response_model=Advertisement)
    async def delete_advertisement(self, ad_id: int, session: AsyncSession = Depends(get_session),
                                   token: str = Depends(oauth2_scheme)):
        user = await get_user(token, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        result = await session.exec(select(Advertisement).where(Advertisement.ad_id == ad_id))
        advertisement = result.one_or_none()
        if advertisement is None:
            raise HTTPException(status_code=404, detail="Advertisement not found")
        await session.delete(advertisement)
        await session.commit()
        return advertisement


crud_router = router
