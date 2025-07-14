// static/js/app.js
function agregarGenero() {
    const nombre = document.getElementById("nombreGenero").value;
    fetch('/genero/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
        .then(response => response.json())
        .then(data => {
            alert("Género agregado con éxito");
            window.location.reload();
        });
}

function agregarPelicula() {
    const datos = {
        codigo: document.getElementById("codigo").value,
        titulo: document.getElementById("titulo").value,
        descripcion: document.getElementById("descripcion").value,
        duracion: document.getElementById("duracion").value,
        protagonista: document.getElementById("protagonista").value,
        genero: document.getElementById("genero").value,
    };

    fetch("/pelicula/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                document.getElementById("mensaje").innerText = "✅ Película agregada correctamente.";
                document.getElementById("formPelicula").reset();
            } else {
                document.getElementById("mensaje").innerText = "❌ Error: " + data.mensaje;
            }
        })
        .catch(err => {
            document.getElementById("mensaje").innerText = "❌ Error de red: " + err;
        });
}

// funcionalidad de los botones
function eliminarGenero(id) {
    if (!confirm("¿Estás seguro de eliminar este género?")) return;

    fetch(`/genero/${id}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                alert("✅ Género eliminado");
                // Borra la fila visualmente
                document.getElementById(`fila-genero-${id}`).remove();
            } else {
                alert("❌ Error: " + data.mensaje);
            }
        })
        .catch(error => {
            alert("❌ Error al eliminar: " + error);
        });
}

function eliminarPelicula(id) {
    if (!confirm("¿Estás seguro de eliminar esta película?")) return;

    fetch(`/pelicula/${id}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                alert("✅ Película eliminada");
                document.getElementById(`fila-pelicula-${id}`).remove();
            } else {
                alert("❌ Error: " + data.mensaje);
            }
        })
        .catch(error => {
            alert("❌ Error al eliminar: " + error);
        });
}

function editarPelicula(id) {
    alert(`🔧 Aquí se editaría la película con ID: ${id}`);
    // Más adelante puedes redirigir a /pelicula/editar/<id> o abrir un formulario modal
}

function cancelarGenero() {
    if (confirm("¿Seguro que deseas cancelar?")) {
        window.location.href = "/genero/listar";
    }
}

function cancelarPelicula() {
    if (confirm("¿Seguro que deseas cancelar?")) {
        window.location.href = "/pelicula/listar";
    }
}

// editar
let idGeneroEditar = null;

function editarGenero(id, nombreActual) {
    idGeneroEditar = id;
    document.getElementById("nuevo-nombre-genero").value = nombreActual;
    document.getElementById("panel-editar-genero").style.display = "block";
}

function cancelarEdicionGenero() {
    idGeneroEditar = null;
    document.getElementById("panel-editar-genero").style.display = "none";
}

function confirmarEdicionGenero() {
    const nuevoNombre = document.getElementById("nuevo-nombre-genero").value;

    fetch(`/genero/${idGeneroEditar}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre: nuevoNombre })
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                alert("✅ Género actualizado");
                window.location.reload();
            } else {
                alert("❌ Error: " + data.mensaje);
            }
        })
        .catch(error => {
            alert("❌ Error de red: " + error);
        });
}


let idPeliculaEditar = null;

function editarPelicula(id, titulo, descripcion, duracion, protagonista) {
    idPeliculaEditar = id;
    document.getElementById("tituloEditar").value = titulo;
    document.getElementById("descripcionEditar").value = descripcion;
    document.getElementById("duracionEditar").value = duracion;
    document.getElementById("protagonistaEditar").value = protagonista;
    document.getElementById("panel-editar-pelicula").style.display = "block";
}

function cancelarEdicionPelicula() {
    idPeliculaEditar = null;
    document.getElementById("panel-editar-pelicula").style.display = "none";
}

function confirmarEdicionPelicula() {
    const datos = {
        titulo: document.getElementById("tituloEditar").value,
        descripcion: document.getElementById("descripcionEditar").value,
        duracion: parseInt(document.getElementById("duracionEditar").value),
        protagonista: document.getElementById("protagonistaEditar").value,
    };

    fetch(`/pelicula/${idPeliculaEditar}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                alert("✅ Película actualizada");
                window.location.reload();
            } else {
                alert("❌ Error: " + data.mensaje);
            }
        })
        .catch(error => {
            alert("❌ Error de red: " + error);
        });
}

// iniciar sesion
function iniciarSesion() {
    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, password })
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                document.getElementById("modalExito").style.display = "flex";
                setTimeout(() => {
                    window.location.href = "/";  
                }, 2000);
            } else {
                document.getElementById("mensajeLogin").textContent = data.mensaje;
            }
        })
        .catch(err => {
            document.getElementById("mensajeLogin").textContent = "❌ Error al procesar login.";
            console.error(err);
        });
}

// registrarse
function registrarUsuario() {
    const datos = {
        usuario: document.getElementById("usuario").value,
        password: document.getElementById("password").value,
        nombre_completo: document.getElementById("nombre_completo").value,
        correo: document.getElementById("correo").value
    };

    fetch("/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(data => {
            if (data.estado) {
                alert(data.mensaje);
                window.location.href = "/login";
            } else {
                document.getElementById("mensajeRegistro").innerText = data.mensaje;
            }
        })
        .catch(() => {
            document.getElementById("mensajeRegistro").innerText = "❌ Error de red.";
        });
}
