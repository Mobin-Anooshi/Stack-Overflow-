from django.urls import path
from home import views



app_name = 'home'
urlpatterns = [
    path('' ,views.HomeView.as_view(),name='home'),
    path('post/<int:post_id>/<slug:post_slug>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post/delete/<int:post_id>/',views.PostDeleteView.as_view(),name='post_delete'),
    path('post/update/<int:post_id>/',views.PostUpdateView.as_view(),name='post_update'),
    path('post/create/',views.PostCreateView.as_view(),name='post_create'),
    path('post/comment/<int:post_id>/', views.UserCommentsView.as_view(),name='post_comment'),
    path('post/replycomment/<int:post_id>/<int:comment_id>/',views.UserReplyCommentView.as_view(),name='user_replycomment'),
    path('like/<int:post_id>/',views.UserPostLikeView.as_view(),name='post_like'),
]

