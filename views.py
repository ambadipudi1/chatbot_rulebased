from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Course, Accommodation, FAQ, ChatLog
from .serializers import (
    DepartmentSerializer, CourseSerializer, AccommodationSerializer,
    FAQSerializer, ChatLogSerializer, ChatRequestSerializer,
)
from .chatbot_logic import get_bot_response


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("department").all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["department", "level"]


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["hostel_type", "room_type"]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class ChatLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatLog.objects.all().order_by("-created_at")
    serializer_class = ChatLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["session_id", "matched_category"]


class ChatAPIView(APIView):
    """
    POST /api/chat/
    Body: { "message": "what is the hostel fee", "session_id": "optional" }
    Returns: { "response": "...", "category": "ACCOMMODATION" }
    """

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id", "")

        bot_response, category = get_bot_response(message)

        ChatLog.objects.create(
            session_id=session_id,
            user_message=message,
            bot_response=bot_response,
            matched_category=category,
        )

        return Response(
            {"response": bot_response, "category": category},
            status=status.HTTP_200_OK,
        )
