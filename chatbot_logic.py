"""
Lightweight rule/keyword based chatbot engine for the college enquiry bot.

Design:
1. Normalize the incoming message.
2. Check for greetings / small talk.
3. Try to match against FAQ keywords stored in the DB (category-tagged).
4. For fee / course / accommodation intents, also try to pull live data
   from the Course / Accommodation tables so answers stay accurate even
   if the admin hasn't written a matching FAQ.
5. Fallback to a "didn't understand" message with suggestions.
"""
import re
from django.db.models import Q
from .models import FAQ, Course, Accommodation, Department


GREETING_WORDS = {"hi", "hello", "hey", "good morning", "good evening", "good afternoon"}
THANKS_WORDS = {"thanks", "thank you", "thankyou", "ty"}
BYE_WORDS = {"bye", "goodbye", "see you", "exit", "quit"}

FEE_KEYWORDS = {"fee", "fees", "cost", "tuition", "price", "charges", "expense"}
ACCOMMODATION_KEYWORDS = {"hostel", "accommodation", "room", "stay", "mess", "dorm", "residence"}
COURSE_KEYWORDS = {"course", "courses", "program", "programs", "department", "branch", "subjects"}
ADMISSION_KEYWORDS = {"admission", "apply", "application", "eligibility", "entrance", "join"}
SCHOLARSHIP_KEYWORDS = {"scholarship", "financial aid", "discount", "waiver"}
CONTACT_KEYWORDS = {"contact", "phone", "email", "address", "location", "reach"}


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text: str, keyword_set) -> bool:
    return any(kw in text for kw in keyword_set)


def match_faq(norm_text: str):
    """Return the best-matching FAQ row based on keyword overlap, or None."""
    best_match = None
    best_score = 0
    for faq in FAQ.objects.all():
        score = sum(1 for kw in faq.keyword_list() if kw and kw in norm_text)
        if score > best_score:
            best_score = score
            best_match = faq
    return best_match if best_score > 0 else None


def build_fee_answer(norm_text: str) -> str:
    """Try to find a specific course mentioned in the text; else list all."""
    courses = Course.objects.select_related("department").all()
    matched = [c for c in courses if c.name.lower() in norm_text]

    if matched:
        lines = []
        for c in matched:
            lines.append(
                f"{c.name} ({c.department.name}) - Tuition: Rs.{c.tuition_fee_per_year}/year, "
                f"Admission fee: Rs.{c.admission_fee}, Exam fee: Rs.{c.exam_fee_per_year}/year, "
                f"Total for {c.duration_years} years: Rs.{c.total_course_fee()}"
            )
        return "Here is the fee structure you asked about:\n" + "\n".join(lines)

    if not courses.exists():
        return "Fee details haven't been added yet. Please contact the admission office."

    lines = [
        f"- {c.name}: Rs.{c.tuition_fee_per_year}/year (Total course fee: Rs.{c.total_course_fee()})"
        for c in courses[:8]
    ]
    return (
        "Here is our fee structure (per course, per year):\n" + "\n".join(lines) +
        "\n\nTell me a specific course name for a detailed breakdown."
    )


def build_accommodation_answer(norm_text: str) -> str:
    hostels = Accommodation.objects.all()
    if not hostels.exists():
        return "Accommodation details haven't been added yet. Please contact the hostel office."

    lines = []
    for h in hostels[:8]:
        lines.append(
            f"- {h.hostel_name} ({h.get_hostel_type_display()}, {h.get_room_type_display()}): "
            f"Rs.{h.fee_per_year}/year + Mess Rs.{h.mess_fee_per_year}/year "
            f"= Total Rs.{h.total_accommodation_fee()}/year. Amenities: {h.amenities or 'N/A'}"
        )
    return "Here are our accommodation options:\n" + "\n".join(lines)


def build_courses_answer(norm_text: str) -> str:
    departments = Department.objects.prefetch_related("courses").all()
    if not departments.exists():
        return "Course/department information hasn't been added yet."

    lines = []
    for d in departments:
        course_names = ", ".join(c.name for c in d.courses.all())
        if course_names:
            lines.append(f"- {d.name}: {course_names}")
    return "We offer the following departments and courses:\n" + "\n".join(lines)


def get_bot_response(message: str):
    """
    Main entry point. Returns (response_text, matched_category).
    """
    norm_text = normalize(message)

    if not norm_text:
        return "Could you please type your question?", "GENERAL"

    if contains_any(norm_text, GREETING_WORDS):
        return (
            "Hello! 👋 I'm the College Enquiry Assistant. You can ask me about "
            "fee structure, courses, accommodation/hostel, admission process, "
            "scholarships, or contact details.",
            "GENERAL",
        )

    if contains_any(norm_text, THANKS_WORDS):
        return "You're welcome! Let me know if you have any other questions.", "GENERAL"

    if contains_any(norm_text, BYE_WORDS):
        return "Goodbye! Feel free to come back if you have more questions about the college.", "GENERAL"

    # 1. Try FAQ table first (admin-curated, most precise answers)
    faq = match_faq(norm_text)
    if faq:
        return faq.answer, faq.category

    # 2. Fall back to live-data intents
    if contains_any(norm_text, FEE_KEYWORDS):
        return build_fee_answer(norm_text), "FEES"

    if contains_any(norm_text, ACCOMMODATION_KEYWORDS):
        return build_accommodation_answer(norm_text), "ACCOMMODATION"

    if contains_any(norm_text, COURSE_KEYWORDS):
        return build_courses_answer(norm_text), "COURSES"

    if contains_any(norm_text, ADMISSION_KEYWORDS):
        return (
            "For admission, you generally need to fill out the online application form, "
            "submit your academic transcripts, and meet the course eligibility criteria. "
            "Ask me about a specific course to see its eligibility.",
            "ADMISSION",
        )

    if contains_any(norm_text, SCHOLARSHIP_KEYWORDS):
        return (
            "We offer merit-based and need-based scholarships. Please contact the "
            "scholarship cell or ask your admission counselor for eligibility criteria.",
            "SCHOLARSHIP",
        )

    if contains_any(norm_text, CONTACT_KEYWORDS):
        return (
            "You can reach the admission office at admissions@college.edu or "
            "call +91-9999999999. Address: College Campus, Main Road, Your City.",
            "CONTACT",
        )

    # 3. Fallback
    return (
        "Sorry, I didn't quite understand that. You can ask me about: "
        "fee structure, courses/departments, hostel & accommodation, "
        "admission process, scholarships, or contact details.",
        "UNKNOWN",
    )
