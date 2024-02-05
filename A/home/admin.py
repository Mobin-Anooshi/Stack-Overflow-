from django.contrib import admin
from home.models import Post , Comment,Vote
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','updated',)
    search_fields = ('slug','body')
    list_filter = ('created',)
    prepopulated_fields={'slug':('body',)}
    raw_id_fields = ('user',)




admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','created','is_reply')
    raw_id_fields = ('user','post','reply')

admin.site.register(Comment,CommentAdmin) 

class VoteAdmin(admin.ModelAdmin):
    list_display=('user' , 'post')
    raw_id_fields=('user', 'post')
admin.site.register(Vote , VoteAdmin)