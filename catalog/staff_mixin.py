from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class UserIsStaffRequired(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated :
            return self.handle_no_permission()
        else:
            if not request.user.is_staff :
                return HttpResponseForbidden('У вас нету доступа к этой странице')

        return super().dispatch(request, *args, **kwargs)