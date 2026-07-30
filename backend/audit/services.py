from django.db.models import Count
from django.db.models import Q
from django.utils import timezone

from .models import AuditLog


class AuditService:

    @staticmethod
    def log(
        action,
        module,
        description,
        user=None,
        object_id=None,
        request=None,
        metadata=None,
    ):

        ip = None
        agent = ""

        if request:

            x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

            if x_forwarded:
                ip = x_forwarded.split(",")[0]
            else:
                ip = request.META.get("REMOTE_ADDR")

            agent = request.META.get(
                "HTTP_USER_AGENT",
                "",
            )

        return AuditLog.objects.create(
            action=action,
            module=module,
            description=description,
            object_id=str(object_id) if object_id else "",
            user=user,
            ip_address=ip,
            user_agent=agent,
            metadata=metadata or {},
        )


class AuditReportService:

    @staticmethod
    def total_logs():

        return AuditLog.objects.count()

    @staticmethod
    def today_logs():

        today = timezone.now().date()

        return AuditLog.objects.filter(
            created_at__date=today
        ).count()

    @staticmethod
    def action_summary():

        return (
            AuditLog.objects
            .values("action")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

    @staticmethod
    def module_summary():

        return (
            AuditLog.objects
            .values("module")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

    @staticmethod
    def recent_logs(limit=50):

        return AuditLog.objects.select_related(
            "user"
        ).order_by(
            "-created_at"
        )[:limit]

    @staticmethod
    def user_logs(user):

        return AuditLog.objects.filter(
            user=user
        ).order_by(
            "-created_at"
        )

    @staticmethod
    def search(keyword):

        return AuditLog.objects.filter(
            Q(description__icontains=keyword)
            |
            Q(module__icontains=keyword)
            |
            Q(action__icontains=keyword)
        ).order_by(
            "-created_at"
        )

    @staticmethod
    def logs_between(start_date, end_date):

        return AuditLog.objects.filter(
            created_at__date__range=[
                start_date,
                end_date,
            ]
        ).order_by(
            "-created_at"
        )

    @staticmethod
    def delete_old_logs(days=365):

        cutoff = timezone.now() - timezone.timedelta(days=days)

        deleted, _ = AuditLog.objects.filter(
            created_at__lt=cutoff
        ).delete()

        return deleted

    @staticmethod
    def failed_logins():

        return AuditLog.objects.filter(
            action="LOGIN",
            metadata__status="FAILED",
        )

    @staticmethod
    def exports():

        return AuditLog.objects.filter(
            action="EXPORT"
        )

    @staticmethod
    def security_events():

        return AuditLog.objects.filter(
            action__in=[
                "LOGIN",
                "LOGOUT",
                "DELETE",
            ]
        ).order_by(
            "-created_at"
        )