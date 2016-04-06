from django.contrib import admin
from BaseInfo.models import PlatForm,DeviceType,Device,Release,KpiType,KpiPriority,Domain,Unit,KPI,KpiDomain,Target,TestResult

admin.site.register(PlatForm)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(Release)
admin.site.register(KpiType)
admin.site.register(KpiPriority)
admin.site.register(Domain)
admin.site.register(Unit)
admin.site.register(KPI)
admin.site.register(KpiDomain)
admin.site.register(Target)
admin.site.register(TestResult)
