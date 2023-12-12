"""
URL configuration for Amrulo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import notifications.urls
from amruloapp import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('amruloapp.urls')),
    path('mark_as_read/<int:notification_pk>', views.notifications, name='notif'),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = 'CDL Administration'
#admin.site.index_title = 'CDL Database'

#####################################********
######## Admin.site views ###########********
#####################################      **
#                                       *  **  *
#                                        * ** *
#                                          **
# Admin custom login
admin.site.login_template = 'amruloapp/backend/admin-login.html'
# Admin custom logout
admin.site.logout_template = 'amruloapp/backend/admin-logged-out.html'
# Admin custom index
admin.site.index_template = 'amruloapp/backend/admin-index.html'
# Admin custom app_index
admin.site.app_index_template = 'amruloapp/backend/admin-app_index.html'
# Admin custom password_change_form
admin.site.password_change_template = 'amruloapp/backend/admin-password_change_form.html'
# Admin custom password_change_done
admin.site.password_change_done_template = 'amruloapp/backend/admin-password_change_done.html'




#####################################********
######## Admin.ModelAdmin views #####********
#####################################      **
#                                       *  **  *
#                                        * ** *
#                                          **
# Admin custom change_list
admin.ModelAdmin.change_list_template = 'amruloapp/backend/admin-change_list.html'
# Admin custom change_form
admin.ModelAdmin.change_form_template = 'amruloapp/backend/admin-change_form.html'
# Admin custom add_form
admin.ModelAdmin.add_form_template = 'amruloapp/backend/admin-add_form.html'
# Admin custom delete_selected_confirmation
admin.ModelAdmin.delete_selected_confirmation_template = 'amruloapp/backend/admin-delete_selected_confirmation.html'
# Admin custom delete_confirmation
admin.ModelAdmin.delete_confirmation_template = 'amruloapp/backend/admin-delete_confirmation.html'
# Admin custom object_history
admin.ModelAdmin.object_history_template = 'amruloapp/backend/admin-object_history.html'
# Admin custom popup_response
admin.ModelAdmin.popup_response_template = 'amruloapp/backend/admin-popup_response.html'
