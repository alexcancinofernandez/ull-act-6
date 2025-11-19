from django.contrib import admin
from .models import Canal, Video, Playlist, Usuario, Comentario, Suscripcion

# ---------------- CANAL ----------------
@admin.register(Canal)
class CanalAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "pais", "categoria_principal", "suscriptores", "url_personalizada")
    search_fields = ("nombre", "pais", "categoria_principal")


# ---------------- VIDEO ----------------
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "canal", "duracion", "vistas", "likes", "publico")
    search_fields = ("titulo", "canal__nombre")
    list_filter = ("publico",)
    ordering = ("-vistas",)


# ---------------- PLAYLIST ----------------
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "canal_creador", "publica", "n_videos")
    search_fields = ("nombre", "canal_creador__nombre")
    list_filter = ("publica",)


# ---------------- USUARIO ----------------
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_usuario", "correo", "pais", "es_verificado", "fecha_registro")
    search_fields = ("nombre_usuario", "correo")
    list_filter = ("es_verificado",)


# ---------------- COMENTARIO ----------------
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "video", "fecha_publicacion", "likes", "visible", "editado")
    search_fields = ("usuario__nombre_usuario", "contenido")
    list_filter = ("visible", "editado")


# ---------------- SUSCRIPCIÓN ----------------
@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "canal", "nivel_suscripcion", "fecha_suscripcion", "activo")
    search_fields = ("usuario__nombre_usuario", "canal__nombre")
    list_filter = ("nivel_suscripcion", "activo")
