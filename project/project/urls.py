from django.urls import path
from django.conf import settings
from django.urls.conf import include
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from utilities.exceptions import page_not_found, server_error_handler
from users.api import viewsets as auth
from branches import viewsets as nagarpalika
from templates.api import reports
from .routers import router

handler500 = server_error_handler
handler404 = page_not_found


urlpatterns = [
    # for swagger docs
    path("api/v1/docs/", include_docs_urls(title="Project API Documentation")),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/jwt/create/", auth.ObtainTokenView.as_view()),
    path("api/v1/active-fiscal-year/", nagarpalika.active_fiscal_year),
    path("api/v1/dashboard-stats", nagarpalika.dashboard),
    path("api/v1/settings-stats", nagarpalika.settings_stats),
    path("api/v1/dashboard-graph/", nagarpalika.ito_admin_graph_api),
    path("api/v1/report/stats/", reports.report_stats_api),
    path("api/v1/report/list/", reports.report_list_api),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
