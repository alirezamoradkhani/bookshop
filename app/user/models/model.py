from sqlalchemy import ForeignKey, Integer, String, Boolean,DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import app.user.models.enums as enum
from sqlalchemy.types import Enum as sqlEnum
from datetime import datetime



class BaseUser(Base):
    __tablename__ = "base_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    role: Mapped[enum.Role] = mapped_column(sqlEnum(enum.Role),nullable= False)
    wallet_amount: Mapped[int] = mapped_column(Integer, default=0)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    __mapper_args__ = {
        "polymorphic_on": role,
        "polymorphic_identity": "base_user",
    }


class User(BaseUser):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(ForeignKey("base_users.id"), primary_key=True)
    plan: Mapped[enum.UserPlan] = mapped_column(
        sqlEnum(enum.UserPlan, name="plan_enum"),
        default=enum.UserPlan.BRONZE,
        nullable=False
    )
    plan_expire : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": enum.Role.USER,
    }
    


class Author(BaseUser):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(ForeignKey("base_users.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": enum.Role.AUTHOR,
    }


class Admin(BaseUser):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(ForeignKey("base_users.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": enum.Role.ADMIN,
    }