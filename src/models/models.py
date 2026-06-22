from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class SavedSummary(Base):
    __tablename__ = "saved_summaries"

    url: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_takeaways: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    estimated_reading_time: Mapped[str] = mapped_column(String, nullable=False)
