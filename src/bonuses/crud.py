from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import Bonuse, User


async def db_get_current_bonuses(session: AsyncSession):
    try:
        bonuses = await session.execute(select(Bonuse).options(selectinload(Bonuse.user)))
        bonuses = bonuses.scalars().all()
        if len(bonuses) != 2:
            raise Exception(f"{len(bonuses)} bonuses exist, not 2")
        
        return bonuses
    except Exception as e:
        await session.rollback()
        print("there is an arrror while getting current_bonuses:", e)
        return {"response": f"error: {e}"}


async def db_collect(is_super: bool, session: AsyncSession, user: User):
    try:
        bonuse = await session.execute(
            select(Bonuse)
            .where(Bonuse.is_super_bonuse == is_super)
        )
        bonuse = bonuse.scalars().first()
        print(bonuse)
        print(bonuse.is_super_bonuse)
        if bonuse is None:
            return {"response": "bonuse not found"}
        if bonuse.is_claimed:
            return {"response": "the bonuse is already claimed"}
        
        if bonuse.bonus_type=="money":
            user.balance += bonuse.value
        else:
            new_multiplier = Decimal(str(1 + (bonuse.value / 100)))
            if user.deposit_bonus_multiplier < new_multiplier:
                user.deposit_bonus_multiplier = new_multiplier
            else:
                return {"response":"user's deposit_bonuse is already equals or higher than this one"}

        if is_super:
            bonuse.user_id = user.id
            bonuse.is_claimed = True

        await session.commit()
        await session.refresh(bonuse)
        return {"response": "ok"}
    except Exception as e:
        await session.rollback()
        print("there is an arrror while collecting bonuse:", e)
        return {"response": f"error: {e}"}