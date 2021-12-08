from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):                        # superclass=IsAdminUser
    
    def has_permission(self, request, view):
        admin_permission=super().has_permission(request, view)          # calling super class's method
        return request.method == 'GET' or admin_permission
        # anonymous users can perfom only 'GET' operations while admin can do all the operations
        
        
class IsReviewUserOrReadOnly(permissions.BasePermission):               # superclass = BasePermission
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:               # SAFE_METHODS is like 'GET' method
            # Check permissions for read-only request
            return True                                         # anonymous users can perform only GET operaions
        else:
            # Check permissions for write request
            current_user= (obj.review_user==request.user)      # return bool value = True
            # cheking if current user is review_user
            return current_user or request.user.is_staff       # only current user or admin or staff can access it