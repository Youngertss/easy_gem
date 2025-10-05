from decimal import Decimal

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import Bonuse, User


async def db_get_current_bonuses(session: AsyncSession) -> list[Bonuse]:
    try:
        bonuses = await session.scalars(select(Bonuse))
        bonuses = bonuses.all()
        if len(bonuses) != 2:
            raise Exception(detail=f"{len(bonuses)} bonuses exists, not 2")
        
        return bonuses
    except Exception as e:
        session.rollback()
        print("there is an arrror while getting current_bonuses:", e)


async def db_collect_super_bonuse(is_super: bool, session: AsyncSession, user: User):
    try:
            bonuse = await session.scalar(select(Bonuse).where(Bonuse.is_super_bonuse == is_super))

            if bonuse is None:
                return {"response": "bonuse not found"}
            if bonuse.is_claimed:
                return {"response": "the bonuse is already claimed"}
            
            if bonuse.value_type=="money":
                user.balance += bonuse.value
            else:
                new_multiplier = Decimal(str(1 + (bonuse.value / 100)))
                if user.deposit_bonus_multiplier < new_multiplier:
                    user.deposit_bonus_multiplier = new_multiplier
                else:
                    return {"response":"user's deposit is already equals or higher than this one"}

            if is_super:
                bonuse.user_id = user.id
                bonuse.is_claimed = True

            await session.commit()
            return {"response": "ok"}
    except Exception as e:
        session.rollback()
        print("there is an arrror while collecting bonuse:", e)