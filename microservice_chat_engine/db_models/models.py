
from enum import Enum as pyEnum
from microservice_chat_engine import Base

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Boolean, DateTime, BigInteger, LargeBinary, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, Relationship

class MissedEvent(Base):
    __tablename__='missed_events'
    id: Mapped[int] = mapped_column(primary_key=True)
    type_of_event: Mapped[str] = mapped_column(String)
    payload: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(BigInteger)
    

