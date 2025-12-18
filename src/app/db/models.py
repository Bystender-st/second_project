from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    DateTime,
    func,
    Boolean,
)
from sqlalchemy.orm import relationship

from .base import Base


class PackageType(Base):
    __tablename__ = "package_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(128), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    weight_kg = Column(Numeric(8, 3), nullable=False)

    type_id = Column(
        Integer,
        ForeignKey("package_types.id"),
        nullable=False,
        index=True,
    )

    content_price_usd = Column(Numeric(12, 2), nullable=False, default=0)
    delivery_price_rub = Column(Numeric(14, 2), nullable=True, index=True)
    delivery_calculated = Column(Boolean, default=False, nullable=False, index=True)

    company_id = Column(Integer, nullable=True, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    type = relationship("PackageType", lazy="joined")
