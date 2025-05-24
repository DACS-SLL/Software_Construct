<template>
  <base-list
    title="Libros Activos"
    :headers="['Titulo', 'Autores', 'Generos', 'Anio_Publicacion', 'ISBN', 'Paginas', 'Estado']"
    :items="librosActivos"
    :loading="loading"
    :error="error"
    :action-label="'Desactivar'"
    :create-label="'Crear Nuevo'"
    @create="handleCreate"
    @edit="handleEdit"
    @delete="handleDeactivate"
  />

  <base-list
    title="Libros No disponibles"
    :headers="['Titulo', 'Autores', 'Generos', 'Anio_Publicacion', 'ISBN', 'Paginas', 'Estado']"
    :items="librosInactivos"
    :loading="loading"
    :error="null"
    :action-label="'Reactivar'"
    :create-label="'Reactivar Libro'"
    :show-create="false"
    @edit="handleEdit"
    @delete="handleReactivate"
  />

  <modal-libro
    :show="modalVisible"
    :libro="selectedLibro"
    :autoresActivos="autoresActivos"
    :generosDisponibles="generosDisponibles"
    @submit="handleModalSubmit"
    @close="modalVisible = false"
  />
</template>

<script>
import BaseList from './BaseList.vue'
import ModalLibro from './ModalLibro.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isAuthenticated = () => !!localStorage.getItem('token')

export default {
  name: 'Libros',
  components: { BaseList, ModalLibro },
  setup() {
    const libros = ref([])
    const librosActivos = ref([])
    const librosInactivos = ref([])
    const loading = ref(false)
    const error = ref(null)

    const autoresActivos = ref([])
    const generosDisponibles = ref([])
    const modalVisible = ref(false)
    const selectedLibro = ref(null)

    const fetchAutoresActivos = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/autores?activo=true')
        autoresActivos.value = response.data.data
        console.log('Autores activos:', autoresActivos.value)
      } catch (err) {
        console.error('Error al cargar autores activos:', err)
      }
    }

    const obtenerLibrosInactivos = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/libros?activo=false', {
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('token')
      }
    })
    const data = response.data.data
    console.log('Libros inactivos:', data) // Depuración
    librosInactivos.value = data.map(libro => ({
      ...libro,
      autores: libro.autores?.map(a => `${a.nombre} ${a.apellido}`).join(', ') || '',
      generos: libro.generos?.map(g => g.nombre).join(', ') || '',
      estado: libro.activo ? 'Activo' : 'Inactivo'
    }))
  } catch (error) {
    console.error('Error al cargar libros inactivos:', error)
    error.value = 'Error al cargar libros inactivos'
  }
}

    const fetchGenerosDisponibles = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/generos/')
        generosDisponibles.value = response.data.data
        console.log('Géneros disponibles:', generosDisponibles.value)
      } catch (err) {
        console.error('Error al cargar géneros disponibles:', err)
      }
    }

    const fetchLibros = async () => {
      try {
        if (!isAuthenticated()) {
          error.value = 'No estás autenticado'
          return
        }

        loading.value = true
        const res = await axios.get('http://localhost:5000/api/libros/', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        })

        const data = res.data.data.map(libro => ({
          ...libro,
          autores: libro.autores?.map(a => `${a.nombre} ${a.apellido}`).join(', ') || '',
          generos: libro.generos?.map(g => g.nombre).join(', ') || '',
          estado: libro.activo ? 'Activo' : 'Inactivo'
        }))

        libros.value = data
        librosActivos.value = data.filter(l => l.activo)
        librosInactivos.value = data.filter(l => !l.activo)
        error.value = null
      } catch (err) {
        error.value =
          err.response?.status === 401
            ? 'Sesión expirada. Por favor, inicia sesión nuevamente'
            : 'Error al cargar los libros'
      } finally {
        loading.value = false
      }
    }

    const handleCreate = async () => {
      await fetchAutoresActivos()
      await fetchGenerosDisponibles()
      selectedLibro.value = null
      modalVisible.value = true
    }

    const handleEdit = async (libro) => {
      await fetchAutoresActivos()
      await fetchGenerosDisponibles()
      selectedLibro.value = { ...libro }
      modalVisible.value = true
    }

    const handleDeactivate = async (libro) => {
      try {
        await axios.delete(`http://localhost:5000/api/libros/${libro.id}`, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        })
        await fetchLibros()
      } catch {
        error.value = 'Error al desactivar el libro'
      }
    }

    const handleReactivate = async (libro) => {
      try {
        await axios.put(
          `http://localhost:5000/api/libros/${libro.id}`,
          { activo: true },
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem('token')
            }
          }
        )
        await fetchLibros()
      } catch (err) {
        error.value = 'Error al reactivar el libro'
      }
    }

    const handleModalSubmit = async (formData) => {
      console.log('Datos recibidos del modal:', formData)
      try {
        loading.value = true

        // Normalización si es necesario
        if (formData.anio_publicacion) {
          formData.anio_publicacion = parseInt(formData.anio_publicacion)
        }

        const config = {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token'),
            'Content-Type': 'application/json'
          }
        }

        if (selectedLibro.value) {
          // EDITAR
          await axios.put(
            `http://localhost:5000/api/libros/${selectedLibro.value.id}`,
            formData,
            config
          )
        } else {
          // CREAR
          await axios.post(
            'http://localhost:5000/api/libros/',
            formData,
            config
          )
        }

        await fetchLibros()
        console.log('Datos enviados:', formData)
        modalVisible.value = false
      } catch (err) {
        if (err.response?.data?.detail?.includes('llave duplicada')) {
          error.value = 'Ya existe un libro con ese ISBN'
        } else if (err.response?.status === 400) {
          error.value = 'Datos inválidos o incompletos'
        } else {
          error.value = 'Error al guardar el libro'
        }
        modalVisible.value = true
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchAutoresActivos()
      fetchGenerosDisponibles()  
      fetchLibros()
      obtenerLibrosInactivos()
    })

    return {
      libros,
      librosActivos,
      librosInactivos,
      loading,
      error,
      modalVisible,
      selectedLibro,
      autoresActivos,
      generosDisponibles, 
      handleCreate,
      handleEdit,
      handleDeactivate,
      handleReactivate,
      handleModalSubmit
    }
  }
}
</script>

