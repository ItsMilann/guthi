from rest_framework.routers import DefaultRouter
from branches import viewsets as nagarpalika_viewset
from templates.api import viewsets as template_viewset
from users.api import profiles, viewsets as user_viewset

router = DefaultRouter()

router.register("user", user_viewset.UserViewSet)
router.register("profile/ito", profiles.ITOProfileViewSet)
router.register("profile/ward-user", profiles.WardUserProfileViewSet)
router.register("profile/mayor", profiles.MayorProfileViewSet)
router.register("profile", profiles.ProfileViewSet)


router.register("features", nagarpalika_viewset.FeatureViewSet)
router.register("fiscal-year", nagarpalika_viewset.FiscalYearViewSet)
router.register("sakha", nagarpalika_viewset.SakhaViewSet)

router.register("paper", template_viewset.PaperViewSet)

router.register("faq", template_viewset.FAQViewset)
