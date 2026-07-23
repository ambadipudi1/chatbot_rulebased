from django.core.management.base import BaseCommand
from chatbot.models import Department, Course, Accommodation, FAQ


class Command(BaseCommand):
    help = "Seed the database with sample college enquiry data"

    def handle(self, *args, **options):
        cse, _ = Department.objects.get_or_create(
            name="Computer Science & Engineering",
            defaults={"hod_name": "Dr. A. Sharma", "description": "CSE Department"},
        )
        ece, _ = Department.objects.get_or_create(
            name="Electronics & Communication",
            defaults={"hod_name": "Dr. R. Iyer", "description": "ECE Department"},
        )
        mech, _ = Department.objects.get_or_create(
            name="Mechanical Engineering",
            defaults={"hod_name": "Dr. S. Rao", "description": "Mechanical Department"},
        )

        Course.objects.get_or_create(
            name="B.Tech Computer Science", department=cse,
            defaults=dict(level="UG", duration_years=4, total_seats=120,
                          eligibility="10+2 with PCM, min 60%",
                          tuition_fee_per_year=120000, admission_fee=15000,
                          exam_fee_per_year=3000, other_charges=5000),
        )
        Course.objects.get_or_create(
            name="B.Tech Electronics", department=ece,
            defaults=dict(level="UG", duration_years=4, total_seats=90,
                          eligibility="10+2 with PCM, min 60%",
                          tuition_fee_per_year=110000, admission_fee=15000,
                          exam_fee_per_year=3000, other_charges=5000),
        )
        Course.objects.get_or_create(
            name="B.Tech Mechanical", department=mech,
            defaults=dict(level="UG", duration_years=4, total_seats=90,
                          eligibility="10+2 with PCM, min 60%",
                          tuition_fee_per_year=100000, admission_fee=15000,
                          exam_fee_per_year=3000, other_charges=5000),
        )
        Course.objects.get_or_create(
            name="M.Tech Computer Science", department=cse,
            defaults=dict(level="PG", duration_years=2, total_seats=30,
                          eligibility="B.Tech/BE with min 60%",
                          tuition_fee_per_year=140000, admission_fee=20000,
                          exam_fee_per_year=3500, other_charges=5000),
        )

        Accommodation.objects.get_or_create(
            hostel_name="Sunrise Boys Hostel", hostel_type="BOYS", room_type="DOUBLE",
            defaults=dict(capacity=200, fee_per_year=60000, mess_fee_per_year=40000,
                          amenities="WiFi, Laundry, 24x7 Water, Gym"),
        )
        Accommodation.objects.get_or_create(
            hostel_name="Rose Girls Hostel", hostel_type="GIRLS", room_type="DOUBLE",
            defaults=dict(capacity=180, fee_per_year=62000, mess_fee_per_year=40000,
                          amenities="WiFi, Laundry, CCTV Security, Common Room"),
        )
        Accommodation.objects.get_or_create(
            hostel_name="Premium Single Suites", hostel_type="CO-ED", room_type="SINGLE",
            defaults=dict(capacity=50, fee_per_year=95000, mess_fee_per_year=45000,
                          amenities="WiFi, AC, Attached Bathroom, Laundry"),
        )

        FAQ.objects.get_or_create(
            question="What is the admission process?",
            defaults=dict(
                category="ADMISSION",
                keywords="admission,apply,application,process,how to join",
                answer=(
                    "The admission process involves: 1) Filling the online application form, "
                    "2) Uploading academic documents, 3) Entrance exam / merit-based shortlisting, "
                    "4) Counseling & seat allotment, 5) Fee payment & document verification."
                ),
            ),
        )
        FAQ.objects.get_or_create(
            question="Are scholarships available?",
            defaults=dict(
                category="SCHOLARSHIP",
                keywords="scholarship,financial aid,discount,waiver,merit",
                answer=(
                    "Yes, we offer merit-based scholarships (up to 50% tuition waiver for top rankers) "
                    "and need-based financial aid. Contact the scholarship cell for details."
                ),
            ),
        )
        FAQ.objects.get_or_create(
            question="What are the college timings?",
            defaults=dict(
                category="GENERAL",
                keywords="timing,timings,hours,college hours,working hours",
                answer="The college operates from 9:00 AM to 4:30 PM, Monday through Saturday.",
            ),
        )

        self.stdout.write(self.style.SUCCESS("Sample data seeded successfully!"))
