from sqlalchemy import BIGINT, FLOAT, VARCHAR, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


# Система таблиць
class Registration(Base):
    __tablename__ = 'registration'

    reg_id: Mapped[int] = mapped_column(
        BIGINT, autoincrement=True, primary_key=True
    )
    reg_name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    reg_type_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    area_name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    ter_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    ter_type_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )

    applicant = relationship("Applicant", back_populates="registration")


class Eo(Base):
    __tablename__ = 'eo'

    eo_id: Mapped[int] = mapped_column(
        BIGINT, autoincrement=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    type_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    parent: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    region_name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    area_name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    ter_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )

    applicant = relationship("Applicant", back_populates="eo")


class Pt(Base):
    __tablename__ = 'pt'

    pt_id: Mapped[int] = mapped_column(
        BIGINT, autoincrement=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    region_name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    area_name: Mapped[str] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    ter_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )

    ukr_test = relationship("UkrTest", back_populates="pt")


class UkrTest(Base):
    __tablename__ = 'ukr_test'

    test_id: Mapped[int] = mapped_column(
        BIGINT, autoincrement=True, primary_key=True
    )
    status: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    language: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    ball100: Mapped[int] = mapped_column(
        FLOAT, nullable=True
    )
    ball12: Mapped[int] = mapped_column(
        BIGINT, nullable=True
    )
    ball: Mapped[int] = mapped_column(
        BIGINT, nullable=True
    )
    adapt_scale: Mapped[int] = mapped_column(
        BIGINT, nullable=True
    )
    pt_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey(Pt.pt_id), nullable=True
    )

    applicant = relationship("Applicant", back_populates="ukr_test")
    pt = relationship("Pt", back_populates="ukr_test")


class Applicant(Base):
    __tablename__ = 'applicant'

    out_id: Mapped[str] = mapped_column(
        VARCHAR(36), primary_key=True
    )
    birth: Mapped[str] = mapped_column(
        BIGINT, nullable=True
    )
    sex_type_name: Mapped[str] = mapped_column(
        VARCHAR(50), nullable=True
    )
    reg_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey(Registration.reg_id), nullable=True
    )
    class_profile_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    class_lang_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=True
    )
    eo_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey(Eo.eo_id), nullable=True
    )
    ukr_test_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey(UkrTest.test_id), nullable=True
    )

    # In Applicant class
    registration = relationship("Registration", back_populates="applicant")
    eo = relationship("Eo", back_populates="applicant")
    ukr_test = relationship("UkrTest", back_populates="applicant")
