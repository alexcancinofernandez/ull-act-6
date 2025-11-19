from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import (
    Canal, Video, Playlist,
    Usuario, Comentario, Suscripcion
)
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import IntegrityError

# -------------------------------
# CRUD para MODELO: VIDEO
# -------------------------------
from .models import Video, Canal

def agregar_video(request):
    canales = Canal.objects.all()
    if request.method == 'POST':
        canal_id = request.POST.get('canal')
        canal = Canal.objects.get(id=canal_id)
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        duracion_horas = int(request.POST.get('duracion_horas') or 0)
        duracion_min = int(request.POST.get('duracion_min') or 0)
        duracion_seg = int(request.POST.get('duracion_seg') or 0)
        vistas = int(request.POST.get('vistas') or 0)
        publico = bool(request.POST.get('publico'))
        url_miniatura = request.POST.get('url_miniatura')
        likes = request.POST.get('likes')

        from datetime import timedelta
        duracion = timedelta(hours=duracion_horas, minutes=duracion_min, seconds=duracion_seg)

        Video.objects.create(
            canal=canal,
            titulo=titulo,
            descripcion=descripcion,
            duracion=duracion,
            vistas=vistas,
            publico=publico,
            url_miniatura=url_miniatura,
            likes=likes
        )
        return redirect('ver_video')
    return render(request, 'video/agregar_video.html', {'canales': canales})


def ver_video(request):
    videos = Video.objects.select_related('canal').all()
    return render(request, 'video/ver_video.html', {'videos': videos})


def actualizar_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    canales = Canal.objects.all()
    if request.method == 'POST':
        canal_id = request.POST.get('canal')
        video.canal = Canal.objects.get(id=canal_id)
        video.titulo = request.POST.get('titulo')
        video.descripcion = request.POST.get('descripcion')
        duracion_horas = int(request.POST.get('duracion_horas') or 0)
        duracion_min = int(request.POST.get('duracion_min') or 0)
        duracion_seg = int(request.POST.get('duracion_seg') or 0)
        from datetime import timedelta
        video.duracion = timedelta(hours=duracion_horas, minutes=duracion_min, seconds=duracion_seg)
        video.vistas = int(request.POST.get('vistas') or 0)
        video.publico = bool(request.POST.get('publico'))
        video.url_miniatura = request.POST.get('url_miniatura')
        video.likes = request.POST.get('likes')
        video.save()
        return redirect('ver_video')
    return render(request, 'video/actualizar_video.html', {'video': video, 'canales': canales})


def borrar_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('ver_video')
    return render(request, 'video/borrar_video.html', {'video': video})


def inicio_YouTube(request):
    # página principal del sistema
    return render(request, 'inicio.html', {'titulo': 'Sistema de Administración YouTube'})

def agregar_canal(request):
    if request.method == 'POST':
        # sin validación (según indicación)
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_creacion = request.POST.get('fecha_creacion')  # YYYY-MM-DD
        suscriptores = request.POST.get('suscriptores') or 0
        url_personalizada = request.POST.get('url_personalizada')
        pais = request.POST.get('pais')
        categoria_principal = request.POST.get('categoria_principal')

        Canal.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion,
            suscriptores=int(suscriptores),
            url_personalizada=url_personalizada,
            pais=pais,
            categoria_principal=categoria_principal
        )
        return redirect('ver_canal')
    return render(request, 'canal/agregar_canal.html')


def ver_canal(request):
    canales = Canal.objects.all().order_by('id')
    return render(request, 'canal/ver_canal.html', {'canales': canales})


def actualizar_canal(request, canal_id):
    canal = get_object_or_404(Canal, pk=canal_id)
    if request.method == 'POST':
        # aquí también podrías redirigir a una función separada, pero usaremos POST directo
        canal.nombre = request.POST.get('nombre')
        canal.descripcion = request.POST.get('descripcion')
        canal.fecha_creacion = request.POST.get('fecha_creacion')
        canal.suscriptores = int(request.POST.get('suscriptores') or 0)
        canal.url_personalizada = request.POST.get('url_personalizada')
        canal.pais = request.POST.get('pais')
        canal.categoria_principal = request.POST.get('categoria_principal')
        canal.save()
        return redirect('ver_canal')
    return render(request, 'canal/actualizar_canal.html', {'canal': canal})


def borrar_canal(request, canal_id):
    canal = get_object_or_404(Canal, pk=canal_id)
    if request.method == 'POST':
        canal.delete()
        return redirect('ver_canal')
    return render(request, 'canal/borrar_canal.html', {'canal': canal})
# -------------------------------
# CRUD para MODELO: PLAYLIST
# -------------------------------


def agregar_playlist(request):
    videos = Video.objects.all()
    canales = Canal.objects.all()  # para seleccionar canal_creador
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_creacion = request.POST.get('fecha_creacion')
        publica = bool(request.POST.get('publica'))
        canal_id = request.POST.get('canal_creador')
        n_videos = request.POST.get('n_videos') or 0

        # crea el objeto Playlist con canal y demás campos
        playlist = Playlist.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion,
            publica=publica,
            canal_creador_id=canal_id,
            orden_videos={},  # vacío por defecto (JSONField)
            n_videos=n_videos
        )

        # asocia videos seleccionados
        videos_ids = request.POST.getlist('videos')
        for vid in videos_ids:
            video = Video.objects.get(id=vid)
            playlist.videos.add(video)

        # guarda cambios finales
        playlist.save()
        return redirect('ver_playlist')

    return render(request, 'playlist/agregar_playlist.html', {
        'videos': videos,
        'canales': canales
    })


def ver_playlist(request):
    playlists = Playlist.objects.select_related('canal_creador').prefetch_related('videos').all()
    return render(request, 'playlist/ver_playlist.html', {'playlists': playlists})


def actualizar_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    videos = Video.objects.all()
    canales = Canal.objects.all()

    if request.method == 'POST':
        playlist.nombre = request.POST.get('nombre')
        playlist.descripcion = request.POST.get('descripcion')
        playlist.fecha_creacion = request.POST.get('fecha_creacion')
        playlist.publica = bool(request.POST.get('publica'))
        playlist.canal_creador_id = request.POST.get('canal_creador')
        playlist.n_videos = request.POST.get('n_videos') or 0
        playlist.orden_videos = {}  # puedes luego actualizarlo según el orden real
        playlist.save()

        # actualizar los videos asociados
        playlist.videos.clear()
        videos_ids = request.POST.getlist('videos')
        for vid in videos_ids:
            video = Video.objects.get(id=vid)
            playlist.videos.add(video)

        return redirect('ver_playlist')

    return render(request, 'playlist/actualizar_playlist.html', {
        'playlist': playlist,
        'videos': videos,
        'canales': canales
    })


def borrar_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if request.method == 'POST':
        playlist.delete()
        return redirect('ver_playlist')
    return render(request, 'playlist/borrar_playlist.html', {'playlist': playlist})

def ver_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios})






# -------------------------------
# CRUD para MODELO: USUARIO
# -------------------------------



from django.contrib import messages
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage

def agregar_usuario(request):
    if request.method == 'POST':
        try:
            # Validar que no exista el nombre de usuario
            nombre_usuario = request.POST['nombre_usuario']
            if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                messages.error(request, f'El nombre de usuario "{nombre_usuario}" ya existe. Por favor elige otro.')
                return render(request, 'usuario/agregar_usuario.html')
            
            # Validar que no exista el correo
            correo = request.POST['correo']
            if Usuario.objects.filter(correo=correo).exists():
                messages.error(request, f'El correo "{correo}" ya está registrado. Por favor usa otro.')
                return render(request, 'usuario/agregar_usuario.html')
            
            # Hashear la contraseña
            contraseña_hasheada = make_password(request.POST['contraseña'])
            
            # Crear usuario
            usuario = Usuario(
                nombre_usuario=nombre_usuario,
                correo=correo,
                contraseña=contraseña_hasheada,
                pais=request.POST.get('pais', ''),
                biografia=request.POST.get('biografia', ''),
                es_verificado='es_verificado' in request.POST,
                fecha_registro=timezone.now()
            )
            
            # Manejar la imagen
            if 'foto_perfil' in request.FILES:
                foto = request.FILES['foto_perfil']
                fs = FileSystemStorage()
                filename = fs.save(f'perfiles/{foto.name}', foto)
                usuario.foto_perfil = filename
            
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente!')
            return redirect('ver_usuarios')
            
        except IntegrityError as e:
            messages.error(request, f'Error de base de datos: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
    
    return render(request, 'usuario/agregar_usuario.html')

def actualizar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        try:
            # Validar nombre de usuario único (excluyendo el actual)
            nuevo_nombre = request.POST['nombre_usuario']
            if Usuario.objects.filter(nombre_usuario=nuevo_nombre).exclude(id=usuario.id).exists():
                messages.error(request, f'El nombre de usuario "{nuevo_nombre}" ya existe.')
                return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})
            
            # Validar correo único (excluyendo el actual)
            nuevo_correo = request.POST['correo']
            if Usuario.objects.filter(correo=nuevo_correo).exclude(id=usuario.id).exists():
                messages.error(request, f'El correo "{nuevo_correo}" ya está registrado.')
                return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})
            
            # Actualizar campos
            usuario.nombre_usuario = nuevo_nombre
            usuario.correo = nuevo_correo
            usuario.pais = request.POST.get('pais', '')
            usuario.biografia = request.POST.get('biografia', '')
            usuario.es_verificado = 'es_verificado' in request.POST
            
            # Manejar nueva contraseña
            nueva_contraseña = request.POST.get('contraseña')
            if nueva_contraseña:
                usuario.contraseña = make_password(nueva_contraseña)
            
            # Manejar nueva imagen
            if 'foto_perfil' in request.FILES:
                # Eliminar imagen anterior si existe
                if usuario.foto_perfil:
                    usuario.foto_perfil.delete(save=False)
                
                foto = request.FILES['foto_perfil']
                fs = FileSystemStorage()
                filename = fs.save(f'perfiles/{foto.name}', foto)
                usuario.foto_perfil = filename
            
            usuario.save()
            messages.success(request, 'Usuario actualizado exitosamente!')
            return redirect('ver_usuarios')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {str(e)}')
    
    return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})



def borrar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)


    if request.method == 'POST':
        usuario.delete()
        return redirect('ver_usuarios')


    return render(request, 'usuario/borrar_usuario.html', {'usuario': usuario})
# ========================= COMENTARIOS =========================


def ver_comentarios(request):
    comentarios = Comentario.objects.select_related('usuario', 'video')
    return render(request, 'comentario/ver_comentarios.html', {'comentarios': comentarios})




def agregar_comentario(request):
    usuarios = Usuario.objects.all()
    videos = Video.objects.all()
    comentarios = Comentario.objects.all()  # Para el campo respuesta_a

    if request.method == 'POST':
        Comentario.objects.create(
            usuario_id=request.POST['usuario'],
            video_id=request.POST['video'],
            contenido=request.POST['contenido'],
            likes=request.POST.get('likes', 0),
            respuesta_a_id=request.POST.get('respuesta_a') or None,
            editado='editado' in request.POST,
            visible='visible' in request.POST
        )
        return redirect('ver_comentarios')

    return render(request, 'comentario/agregar_comentario.html', {
        'usuarios': usuarios,
        'videos': videos,
        'comentarios': comentarios  # Pasar para el select de respuesta_a
    })

def actualizar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    usuarios = Usuario.objects.all()
    videos = Video.objects.all()
    comentarios = Comentario.objects.all()

    if request.method == 'POST':
        comentario.usuario_id = request.POST['usuario']
        comentario.video_id = request.POST['video']
        comentario.contenido = request.POST['contenido']
        comentario.likes = request.POST.get('likes', 0)
        comentario.respuesta_a_id = request.POST.get('respuesta_a') or None
        comentario.editado = 'editado' in request.POST
        comentario.visible = 'visible' in request.POST
        comentario.save()
        return redirect('ver_comentarios')

    return render(request, 'comentario/actualizar_comentario.html', {
        'comentario': comentario,
        'usuarios': usuarios,
        'videos': videos,
        'comentarios': comentarios
    })


def borrar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)


    if request.method == 'POST':
        comentario.delete()
        return redirect('ver_comentarios')


    return render(request, 'comentario/borrar_comentario.html', {'comentario': comentario})
# ========================= SUSCRIPCIONES =========================


def ver_suscripciones(request):
    suscripciones = Suscripcion.objects.select_related('usuario', 'canal')
    return render(request, 'suscripcion/ver_suscripciones.html', {'suscripciones': suscripciones})




def agregar_suscripcion(request):
    usuarios = Usuario.objects.all()
    canales = Canal.objects.all()

    if request.method == 'POST':
        Suscripcion.objects.create(
            usuario_id=request.POST['usuario'],
            canal_id=request.POST['canal'],
            nivel_suscripcion=request.POST['nivel_suscripcion'],
            notificaciones_activadas='notificaciones_activadas' in request.POST,
            comentarios_habilitados='comentarios_habilitados' in request.POST,
            puntos_fidelidad=request.POST.get('puntos_fidelidad', 0),
            activo='activo' in request.POST
        )
        return redirect('ver_suscripciones')

    return render(request, 'suscripcion/agregar_suscripcion.html', {
        'usuarios': usuarios,
        'canales': canales
    })

def actualizar_suscripcion(request, id):
    suscripcion = get_object_or_404(Suscripcion, id=id)
    usuarios = Usuario.objects.all()
    canales = Canal.objects.all()

    if request.method == 'POST':
        suscripcion.usuario_id = request.POST['usuario']
        suscripcion.canal_id = request.POST['canal']
        suscripcion.nivel_suscripcion = request.POST['nivel_suscripcion']
        suscripcion.notificaciones_activadas = 'notificaciones_activadas' in request.POST
        suscripcion.comentarios_habilitados = 'comentarios_habilitados' in request.POST
        suscripcion.puntos_fidelidad = request.POST.get('puntos_fidelidad', 0)
        suscripcion.activo = 'activo' in request.POST
        suscripcion.save()
        return redirect('ver_suscripciones')

    return render(request, 'suscripcion/actualizar_suscripcion.html', {
        'suscripcion': suscripcion,
        'usuarios': usuarios,
        'canales': canales
    })



def borrar_suscripcion(request, id):
    suscripcion = get_object_or_404(Suscripcion, id=id)


    if request.method == 'POST':
        suscripcion.delete()
        return redirect('ver_suscripciones')


    return render(request, 'suscripcion/borrar_suscripcion.html', {'suscripcion': suscripcion})


