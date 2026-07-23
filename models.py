from django.db import models


class Department(models.Model):
    """Academic department, e.g. Computer Science, Mechanical, etc."""
    name = models.CharField(max_length=150, unique=True)
    hod_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """A course/program offered, with academic + fee details."""

    LEVEL_CHOICES = (
        ("UG", "Undergraduate"),
        ("PG", "Postgraduate"),
        ("DIPLOMA", "Diploma"),
    )

    name = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="courses"
    )
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="UG")
    duration_years = models.PositiveSmallIntegerField(default=4)
    total_seats = models.PositiveIntegerField(default=60)
    eligibility = models.TextField(blank=True, null=True)

    # Fee structure fields
    tuition_fee_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exam_fee_per_year = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def total_course_fee(self):
        return (self.tuition_fee_per_year * self.duration_years) + \
               self.admission_fee + \
               (self.exam_fee_per_year * self.duration_years) + \
               self.other_charges

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class Accommodation(models.Model):
    """Hostel / accommodation options."""

    HOSTEL_TYPE_CHOICES = (
        ("BOYS", "Boys Hostel"),
        ("GIRLS", "Girls Hostel"),
        ("CO-ED", "Co-ed Hostel"),
    )

    ROOM_TYPE_CHOICES = (
        ("SINGLE", "Single Sharing"),
        ("DOUBLE", "Double Sharing"),
        ("TRIPLE", "Triple Sharing"),
        ("DORM", "Dormitory"),
    )

    hostel_name = models.CharField(max_length=150)
    hostel_type = models.CharField(max_length=10, choices=HOSTEL_TYPE_CHOICES)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField(help_text="Total beds available")
    fee_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    mess_fee_per_year = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amenities = models.TextField(
        blank=True, null=True, help_text="Comma separated e.g. WiFi, Laundry, Gym"
    )

    def total_accommodation_fee(self):
        return self.fee_per_year + self.mess_fee_per_year

    def __str__(self):
        return f"{self.hostel_name} - {self.room_type}"


class FAQ(models.Model):
    """General enquiry Q&A used by the chatbot's keyword matcher."""

    CATEGORY_CHOICES = (
        ("FEES", "Fee Structure"),
        ("ACCOMMODATION", "Accommodation"),
        ("ADMISSION", "Admission Process"),
        ("COURSES", "Courses / Academics"),
        ("SCHOLARSHIP", "Scholarship"),
        ("CONTACT", "Contact / Location"),
        ("GENERAL", "General"),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="GENERAL")
    question = models.CharField(max_length=300)
    keywords = models.CharField(
        max_length=300,
        help_text="Comma separated keywords used for matching, e.g. 'fee,fees,cost,tuition'"
    )
    answer = models.TextField()

    def keyword_list(self):
        return [k.strip().lower() for k in self.keywords.split(",") if k.strip()]

    def __str__(self):
        return self.question


class ChatLog(models.Model):
    """Stores each chatbot interaction for analytics / audit."""

    session_id = models.CharField(max_length=100, blank=True, null=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    matched_category = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.user_message[:50]}"
