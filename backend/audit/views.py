from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import AuditLog
from .serializers import AuditLogSerializer
from .filters import AuditLogFilter
from .services import AuditReportService


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = (
        AuditLog.objects
        .select_related("user")
        .order_by("-created_at")
    )

    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_class = AuditLogFilter

    search_fields = (
        "description",
        "module",
        "action",
        "user__username",
    )

    ordering_fields = (
        "created_at",
        "action",
        "module",
    )

    ordering = ("-created_at",)

    @action(detail=False, methods=["get"])
    def summary(self, request):

        return Response({
            "total_logs": AuditReportService.total_logs(),
            "today_logs": AuditReportService.today_logs(),
            "actions": AuditReportService.action_summary(),
            "modules": AuditReportService.module_summary(),
        })

    @action(detail=False, methods=["get"])
    def recent(self, request):

        serializer = self.get_serializer(
            AuditReportService.recent_logs(),
            many=True,
        )

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def security(self, request):

        serializer = self.get_serializer(
            AuditReportService.security_events(),
            many=True,
        )

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def exports(self, request):

        serializer = self.get_serializer(
            AuditReportService.exports(),
            many=True,
        )

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def failed_logins(self, request):

        serializer = self.get_serializer(
            AuditReportService.failed_logins(),
            many=True,
        )

        return Response(serializer.data)