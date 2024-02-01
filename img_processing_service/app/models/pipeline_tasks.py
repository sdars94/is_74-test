from sqlalchemy import ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class PipelineTask(Base):
    __tablename__ = "pipeline_task"

    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, index=True
    )
    pipeline_id: Mapped[int] = mapped_column(
        ForeignKey("pipeline.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str | None] = mapped_column(String(55), nullable=True)
    filename: Mapped[str] = mapped_column(String(255))
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    def __repr__(self):
        return (
            f"<PipelineTask: id={self.id}, " f"pipeline_id={self.pipeline_id}>"
        )
