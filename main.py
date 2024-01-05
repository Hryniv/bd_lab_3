from environs import Env
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session

from models import Applicant, Eo, Pt, UkrTest, Registration

env = Env()
env.read_env('.env')

url = URL.create(
    drivername="postgresql",
    username=env.str('POSTGRES_USER'),
    password=env.str('POSTGRES_PASSWORD'),
    host=env.str('DATABASE_HOST'),
    port=5432,
    database=env.str('POSTGRES_DB'),
).render_as_string(hide_password=False)

engine = create_engine(url, echo=True)
session_pool = sessionmaker(bind=engine)
session = session_pool()


class Repo:
    def __init__(self, session: Session):
        self.session = session

    def get_applicants_by_zno_range(self, min_score: int, max_score: int):
        try:
            applicants = self.session.query(Applicant). \
                join(UkrTest, Applicant.ukr_test). \
                filter(UkrTest.ball100.between(min_score, max_score)). \
                limit(10).all()

            if applicants:
                print(f"Список абітурієнтів з балами ЗНО від {min_score} до {max_score}:")
                for applicant in applicants:
                    print(f"OUTID: {applicant.out_id}")
                    print(f"Birth: {applicant.birth}")
                    print(f"Sex Type: {applicant.sex_type_name}")
                    print(f"Class Profile: {applicant.class_profile_name}")
                    print(f"Class Lang: {applicant.class_lang_name}\n")

            else:
                print(f"Абітурієнтів з балами ЗНО від {min_score} до {max_score} не знайдено.")
        except Exception as e:
            print(f"Помилка при отриманні абітурієнтів: {e}")

    def get_applicant_by_id(self, applicant_id: str):
        try:
            applicant = self.session.query(Applicant).filter_by(out_id=applicant_id).first()

            if applicant is not None:
                print(f"Інформація про абітурієнта з ID {applicant_id}:")
                print(f"Birth: {applicant.birth}")
                print(f"Sex Type: {applicant.sex_type_name}")
                print(f"Class Profile: {applicant.class_profile_name}")
                print(f"Class Lang: {applicant.class_lang_name}")

                registration = applicant.registration
                eo = applicant.eo
                ukr_test = applicant.ukr_test
                pt = ukr_test.pt

                if registration:
                    print("Registration Info:")
                    for key, value in registration.__dict__.items():
                        if not key.startswith("_") and not key.endswith("id"):
                            print(f"{key}: {value}")

                if eo:
                    print("Eo Info:")
                    for key, value in eo.__dict__.items():
                        if not key.startswith("_") and not key.endswith("id"):
                            print(f"{key}: {value}")

                if ukr_test:
                    print("UkrTest Info:")
                    for key, value in ukr_test.__dict__.items():
                        if not key.startswith("_") and not key.endswith("id"):
                            print(f"{key}: {value}")

                if pt:
                    print("Pt Info:")
                    for key, value in pt.__dict__.items():
                        if not key.startswith("_") and not key.endswith("id"):
                            print(f"{key}: {value}")

            else:
                print(f"Абітурієнт з ID {applicant_id} не знайдений.")
        except Exception as e:
            print(f"Помилка при отриманні абітурієнта: {e}")

    def delete_student_by_out_id(self, out_id: str):
        try:
            # Знаходимо студента за out_id
            student = self.session.query(Applicant).filter_by(out_id=out_id).first()

            if student is not None:
                # Отримуємо значення зовнішніх ключів
                reg_id = student.reg_id
                eo_id = student.eo_id
                ukr_test_id = student.ukr_test_id

                # Видаляємо студента та всі пов'язані записи
                self.session.query(Applicant).filter_by(out_id=out_id).delete()
                self.session.query(Registration).filter_by(reg_id=reg_id).delete()
                self.session.query(Eo).filter_by(eo_id=eo_id).delete()
                self.session.query(UkrTest).filter_by(test_id=ukr_test_id).delete()

                self.session.commit()
                print(f"Абітурієнта із out_id={out_id} видалено.")
            else:
                print(f"Абітурієнт із out_id={out_id} не знайдений.")
        except IntegrityError as e:
            print(f"Помилка видалення: {e}")
            self.session.rollback()

    def add_registration(
            self,
            reg_name: str,
            reg_type_name: str,
            area_name: str,
            ter_name: str,
            ter_type_name: str
    ):
        registration = Registration(
            reg_name=reg_name,
            reg_type_name=reg_type_name,
            area_name=area_name,
            ter_name=ter_name,
            ter_type_name=ter_type_name
        )
        self.session.add(registration)
        self.session.commit()
        return registration

    def add_eo(
            self,
            name: str,
            type_name: str,
            parent: str,
            region_name: str,
            area_name: str,
            ter_name: str
    ):
        eo = Eo(
            name=name,
            type_name=type_name,
            parent=parent,
            region_name=region_name,
            area_name=area_name,
            ter_name=ter_name
        )
        self.session.add(eo)
        self.session.commit()
        return eo

    def add_pt(
            self,
            name: str,
            region_name: str,
            area_name: str,
            ter_name: str
    ):
        pt = Pt(
            name=name,
            region_name=region_name,
            area_name=area_name,
            ter_name=ter_name
        )
        self.session.add(pt)
        self.session.commit()
        return pt

    def add_ukr_test(
            self,
            status: str,
            language: str,
            ball100: int,
            ball12: int,
            ball: int,
            adapt_scale: int,
            pt_id: int
    ):
        ukr_test = UkrTest(
            status=status,
            language=language,
            ball100=ball100,
            ball12=ball12,
            ball=ball,
            adapt_scale=adapt_scale,
            pt_id=pt_id
        )
        self.session.add(ukr_test)
        self.session.commit()
        return ukr_test

    def add_applicant(
            self,
            out_id: str,
            birth: int,
            sex_type_name: str,
            reg_id: int,
            class_profile_name: str,
            class_lang_name: str,
            eo_id: int,
            ukr_test_id: int,
    ):
        applicant = Applicant(
            out_id=out_id,
            birth=birth,
            sex_type_name=sex_type_name,
            reg_id=reg_id,
            class_profile_name=class_profile_name,
            class_lang_name=class_lang_name,
            eo_id=eo_id,
            ukr_test_id=ukr_test_id,
        )
        self.session.add(applicant)
        self.session.commit()

    def add_record(
            self,
            reg_name: str,
            reg_type_name: str,
            area_name: str,
            ter_name: str,
            ter_type_name: str,
            eo_name: str,
            eo_type_name: str,
            eo_parent: str,
            eo_region_name: str,
            eo_area_name: str,
            eo_ter_name: str,
            pt_name: str,
            pt_region_name: str,
            pt_area_name: str,
            pt_ter_name: str,
            status: str,
            language: str,
            ball100: int,
            ball12: int,
            ball: int,
            adapt_scale: int,
            out_id: str,
            birth: int,
            sex_type_name: str,
            class_profile_name: str,
            class_lang_name: str,
    ):
        registration = self.add_registration(
            reg_name=reg_name,
            reg_type_name=reg_type_name,
            area_name=area_name,
            ter_name=ter_name,
            ter_type_name=ter_type_name)

        eo = self.add_eo(
            name=eo_name,
            type_name=eo_type_name,
            parent=eo_parent,
            region_name=eo_region_name,
            area_name=eo_area_name,
            ter_name=eo_ter_name)

        pt = self.add_pt(pt_name, pt_region_name, pt_area_name, pt_ter_name)
        ukr_test = self.add_ukr_test(status, language, ball100, ball12, ball, adapt_scale, pt.pt_id)

        self.add_applicant(out_id=out_id,
                           birth=birth,
                           sex_type_name=sex_type_name,
                           reg_id=registration.reg_id,
                           class_profile_name=class_profile_name,
                           class_lang_name=class_lang_name,
                           eo_id=eo.eo_id,
                           ukr_test_id=ukr_test.test_id)


repo = Repo(session)
# repo.add_record(out_id="xxxx", birth=2002, sex_type_name="чоловік", class_profile_name="математичний",
#                 class_lang_name="українська",
#                 reg_name="Сумська область", reg_type_name="випускник", area_name="м.Суми",
#                 ter_name="Ковпаківський район міста", ter_type_name="місто",
#                 eo_name="Комун. уст. Сумська заг.осв школа №8", eo_type_name="сер. заг. ш",
#                 eo_parent="Упр. осв. наук. Сум. м.ради",
#                 eo_region_name="Сум. обл.", eo_area_name="м. Суми, Ковп. район", eo_ter_name="Ковп. район мыста",
#                 pt_name="Технологічний", pt_region_name="Сум. обл", pt_area_name="м. Суми",
#                 pt_ter_name="Ковпаківський район міста",
#                 status="Зарах", language="ukr", ball100=158, ball12=9, ball=63, adapt_scale=0,
#                 )
# repo.get_applicant_by_id("xxxx")
repo.get_applicants_by_zno_range(min_score=160, max_score=165)
# repo.delete_student_by_out_id(out_id="xxxx")

# SQL-ін'єкція
applicant_id = "'; DROP TABLE applicant; --"
repo.get_applicant_by_id(applicant_id)
# repo.add_record(out_id=applicant_id, birth=2002, sex_type_name="чоловік", class_profile_name="математичний",
#                 class_lang_name="українська",
#                 reg_name="Сумська область", reg_type_name="випускник", area_name="м.Суми",
#                 ter_name="Ковпаківський район міста", ter_type_name="місто",
#                 eo_name="Комун. уст. Сумська заг.осв школа №8", eo_type_name="сер. заг. ш",
#                 eo_parent="Упр. осв. наук. Сум. м.ради",
#                 eo_region_name="Сум. обл.", eo_area_name="м. Суми, Ковп. район", eo_ter_name="Ковп. район мыста",
#                 pt_name="Технологічний", pt_region_name="Сум. обл", pt_area_name="м. Суми",
#                 pt_ter_name="Ковпаківський район міста",
#                 status="Зарах", language="ukr", ball100=158, ball12=9, ball=63, adapt_scale=0,
#                 )
repo.get_applicant_by_id(applicant_id)
