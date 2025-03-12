from rest_framework.permissions import BasePermission

class IsRouteOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f"User: {request.user}")
        print(f"User groups: {request.user.groups.all()}")
        print(f"Is admin: {request.user.groups.filter(name='admin').exists()}")
        print(f"Is owner: {request.user in obj.owners.all()}")
        print(f"Object owners: {obj}")
        return request.user in obj.owners.all() or request.user.groups.filter(name='admin').exists()


