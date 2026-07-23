from rest_framework import serializers
from .models import Department, Course, Accommodation, FAQ, ChatLog


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source="department.name")
    total_fee = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "name", "department", "department_name", "level",
            "duration_years", "total_seats", "eligibility",
            "tuition_fee_per_year", "admission_fee", "exam_fee_per_year",
            "other_charges", "total_fee",
        ]

    def get_total_fee(self, obj):
        return obj.total_course_fee()


class AccommodationSerializer(serializers.ModelSerializer):
    total_fee = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        fields = [
            "id", "hostel_name", "hostel_type", "room_type", "capacity",
            "fee_per_year", "mess_fee_per_year", "amenities", "total_fee",
        ]

    def get_total_fee(self, obj):
        return obj.total_accommodation_fee()


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = "__all__"
        read_only_fields = ["bot_response", "matched_category", "created_at"]


class ChatRequestSerializer(serializers.Serializer):
    """Input serializer for the /api/chat/ endpoint."""
    message = serializers.CharField(max_length=500)
    session_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
