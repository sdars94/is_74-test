from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Pipeline(Base):
    __tablename__ = "pipeline"

    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )

    steps = relationship(
        "PipelineStep",
        secondary="pipeline_step_association",
        back_populates="pipelines",
        order_by="PipelineStepAssociation.step_order",

    )

    def __repr__(self):
        return f"<Pipeline: id={self.id}, title={self.title}>"


class PipelineStep(Base):
    __tablename__ = "pipeline_step"

    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    handler: Mapped[str] = mapped_column(String(255), nullable=False)

    pipelines = relationship(
        "Pipeline",
        secondary="pipeline_step_association",
        back_populates="steps",
    )

    def __repr__(self):
        return f"<PipelineStep: id={self.id}, title={self.title}>"


class PipelineStepAssociation(Base):
    __tablename__ = "pipeline_step_association"

    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, index=True
    )
    pipeline_id: Mapped[int] = mapped_column(
        ForeignKey("pipeline.id", ondelete="CASCADE"), nullable=False
    )
    pipeline_step_id: Mapped[int] = mapped_column(
        ForeignKey("pipeline_step.id", ondelete="RESTRICT"), nullable=False
    )
    step_order: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("pipeline_id", "pipeline_step_id", "step_order"),
        CheckConstraint("step_order > 0"),
    )

    def __repr__(self):
        return (
            f"<PipelineStepAssociation: id={self.id}, "
            f"pipeline_id={self.pipeline_id}, "
            f"pipeline_step_id={self.pipeline_step_id}>"
        )
