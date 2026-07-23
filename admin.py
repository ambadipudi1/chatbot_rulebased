from django.contrib import admin
from .models import Department, Course, Accommodation, FAQ, ChatLog


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "hod_name")
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "level", "duration_years", "tuition_fee_per_year", "total_seats")
    list_filter = ("department", "level")
    search_fields = ("name",)


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("hostel_name", "hostel_type", "room_type", "capacity", "fee_per_year")
    list_filter = ("hostel_type", "room_type")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category")
    list_filter = ("category",)
    search_fields = ("question", "keywords")


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ("user_message", "matched_category", "created_at")
    list_filter = ("matched_category",)
    readonly_fields = ("user_message", "bot_response", "matched_category", "created_at")
