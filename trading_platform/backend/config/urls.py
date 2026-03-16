from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/strategies/', include('strategies.urls')),
    path('api/backtests/', include('backtesting.urls')),
    path('api/marketplace/', include('marketplace.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/orders/', include('execution.urls')),
]
