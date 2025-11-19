from django.db import models
from django.utils import timezone

# ======================= CANAL =======================
class Canal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateField()
    suscriptores = models.IntegerField(default=0)
    url_personalizada = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=50)
    categoria_principal = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# ======================= VIDEO =======================
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name='videos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    duracion = models.DurationField()
    vistas = models.IntegerField(default=0)
    publico = models.BooleanField(default=True)
    url_miniatura = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)   # 🔥 lo arreglé, antes era CharField

    def __str__(self):
        return f"{self.titulo} ({self.canal.nombre})"


# ======================= PLAYLIST =======================
class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_creacion = models.DateField()
    publica = models.BooleanField(default=True)
    canal_creador = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name='playlists')
    videos = models.ManyToManyField(Video, related_name='playlists')
    orden_videos = models.JSONField()
    n_videos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.canal_creador.nombre}"


# ======================= USUARIO =======================
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)  # 🔥 AGREGADO
    nombre_usuario = models.CharField(max_length=100, unique=True)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(default=timezone.now)
    pais = models.CharField(max_length=50, blank=True)
    biografia = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    es_verificado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_usuario


# ======================= COMENTARIO =======================
class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    respuesta_a = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respuestas')
    editado = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"Comentario de {self.usuario} en {self.video}"


# ======================= SUSCRIPCION =======================
class Suscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='suscripciones')
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name='suscripciones')  # 🔥 ARREGLADO
    fecha_suscripcion = models.DateTimeField(default=timezone.now)
    notificaciones_activadas = models.BooleanField(default=True)
    nivel_suscripcion = models.CharField(max_length=50, choices=[
        ('Gratis', 'Gratis'),
        ('Premium', 'Premium'),
        ('VIP', 'VIP')
    ], default='Gratis')
    comentarios_habilitados = models.BooleanField(default=True)
    puntos_fidelidad = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario} suscrito a {self.canal}"
