from rest_framework.routers import DefaultRouter
from branches import viewsets as branches
from templates.api import viewsets as template_viewset
from users.api import profiles, viewsets as user_viewset

router = DefaultRouter()

router.register("user", user_viewset.UserViewSet)
router.register("profile", profiles.ProfileViewSet)


router.register("features", branches.FeatureViewSet)
router.register("branches", branches.BranchViewSet)
router.register("fiscal-year", branches.FiscalYearViewSet)
router.register("departments", branches.SakhaViewSet)

router.register("paper", template_viewset.PaperViewSet)

router.register("faq", template_viewset.FAQViewset)
