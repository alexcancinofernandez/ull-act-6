from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_YouTube, name='inicio_YouTube'),
    path('canal/agregar/', views.agregar_canal, name='agregar_canal'),
    path('canal/ver/', views.ver_canal, name='ver_canal'),
    path('canal/actualizar/<int:canal_id>/', views.actualizar_canal, name='actualizar_canal'),
    path('canal/borrar/<int:canal_id>/', views.borrar_canal, name='borrar_canal'),

    # RUTAS PARA VIDEO
    path('video/agregar/', views.agregar_video, name='agregar_video'),
    path('video/ver/', views.ver_video, name='ver_video'),
    path('video/actualizar/<int:video_id>/', views.actualizar_video, name='actualizar_video'),
    path('video/borrar/<int:video_id>/', views.borrar_video, name='borrar_video'),

# RUTAS PARA PLAYLIST
    path('playlist/agregar/', views.agregar_playlist, name='agregar_playlist'),
    path('playlist/ver/', views.ver_playlist, name='ver_playlist'),
    path('playlist/actualizar/<int:playlist_id>/', views.actualizar_playlist, name='actualizar_playlist'),
    path('playlist/borrar/<int:playlist_id>/', views.borrar_playlist, name='borrar_playlist'),
# ========== 👤 USUARIO ==========
# ========== 👤 USUARIO ==========
    # ========== 👤 USUARIO ==========
    path('usuario/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuario/ver/', views.ver_usuarios, name='ver_usuarios'),
    path('usuario/actualizar/<int:id>/', views.actualizar_usuario, name='actualizar_usuario'),  # 🔥 CAMBIADO
    path('usuario/borrar/<int:id>/', views.borrar_usuario, name='borrar_usuario'),  # 🔥 CAMBIADO

# ========== 💬 COMENTARIO ==========
    path('comentario/agregar/', views.agregar_comentario, name='agregar_comentario'),
    path('comentario/ver/', views.ver_comentarios, name='ver_comentarios'),
    path('comentario/actualizar/<int:id>/', views.actualizar_comentario, name='actualizar_comentario'),
    path('comentario/borrar/<int:id>/', views.borrar_comentario, name='borrar_comentario'),

# ========== ⭐ SUSCRIPCION ==========
    path('suscripcion/agregar/', views.agregar_suscripcion, name='agregar_suscripcion'),
    path('suscripcion/ver/', views.ver_suscripciones, name='ver_suscripciones'),
    path('suscripcion/actualizar/<int:id>/', views.actualizar_suscripcion, name='actualizar_suscripcion'),
    path('suscripcion/borrar/<int:id>/', views.borrar_suscripcion, name='borrar_suscripcion'),
]