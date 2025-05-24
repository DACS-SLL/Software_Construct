<template>
  <base-list
    title="Autores Activos"
    :headers="['Nombre', 'Apellido', 'Nacionalidad', 'Fecha Nacimiento', 'Estado']"
    :items="autoresActivos"
    :loading="loading"
    :error="error"
    :action-label="'Desactivar'"
    :create-label="'Crear Nuevo'"
    @create="handleCreate"
    @edit="handleEdit"
    @delete="handleDeactivate"
  />

  <base-list
    title="Autores Inactivos"
    :headers="['Nombre', 'Apellido', 'Nacionalidad', 'Fecha Nacimiento', 'Estado']"
    :items="autoresInactivos"
    :loading="loading"
    :error="null"
    :action-label="'Reactivar'"
    :create-label="'Reactivar Autor'"
    :show-create="false"
    @edit="handleEdit"
    @delete="handleReactivate"
  />

  <modal-autor
    :show="modalVisible"
    :autor="selectedAutor"
    @submit="handleModalSubmit"
    @close="modalVisible = false"
  />
</template>

<script>
import BaseList from './BaseList.vue'
import ModalAutor from './ModalAutor.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isAuthenticated = () => !!localStorage.getItem('token')

export default {
  name: 'Autores',
  components: { BaseList, ModalAutor },
  setup() {
    const autores = ref([])
    const loading = ref(false)
    const error = ref(null)

    const autoresActivos = ref([])
    const autoresInactivos = ref([])

    const modalVisible = ref(false)
    const selectedAutor = ref(null)

    const fetchAutores = async () => {
      try {
        if (!isAuthenticated()) {
          error.value = 'No estás autenticado'
          return
        }

        loading.value = true
        const res = await axios.get('http://localhost:5000/api/autores/', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        })

        // Función para formatear fechas
        const formatFecha = (fecha) => {
          if (!fecha) return ''
          try {
            // Intentar parsear la fecha en diferentes formatos
            const date = new Date(fecha)
            if (isNaN(date.getTime())) {
              // Si no se puede parsear, intentar con formato YYYY-MM-DD
              const parts = fecha.split('-')
              if (parts.length === 3) {
                return new Date(parts[0], parts[1] - 1, parts[2])
              }
              return ''
            }
            return date.toLocaleDateString('es-ES', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit'
            })
          } catch (error) {
            console.error('Error formateando fecha:', error)
            return ''
          }
        }

        const data = res.data.data.map(autor => ({
          ...autor,
          fecha_nacimiento: formatFecha(autor.fecha_nacimiento),
          estado: autor.activo ? 'Activo' : 'Inactivo'
        }))

        autores.value = data
        autoresActivos.value = data.filter(a => a.activo)
        autoresInactivos.value = data.filter(a => !a.activo)
        error.value = null
      } catch (err) {
        error.value =
          err.response?.status === 401
            ? 'Sesión expirada. Por favor, inicia sesión nuevamente'
            : 'Error al cargar los autores'
      } finally {
        loading.value = false
      }
    }

    const handleCreate = () => {
      selectedAutor.value = null
      modalVisible.value = true
    }

    const handleEdit = (autor) => {
      selectedAutor.value = { ...autor }
      modalVisible.value = true
    }

    const handleDeactivate = async (autor) => {
      try {
        await axios.delete(
          `http://localhost:5000/api/autores/${autor.id}`,
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem('token')
            }
          }
        )
        await fetchAutores()
      } catch {
        error.value = 'Error al desactivar el autor'
      }
    }

    const handleReactivate = async (autor) => {
      try {
        await axios.put(
          'http://localhost:5000/api/autores/${autor.id}',
          { ...autor, activo: true },
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem('token')
            }
          }
        )
        await fetchAutores()
      } catch {
        error.value = 'Error al reactivar el autor'
      }
    }

    const handleModalSubmit = async (formData) => {
      try {
        loading.value = true

        // Normaliza la fecha a formato YYYY-MM-DD
        if (formData.fecha_nacimiento) {
          const date = new Date(formData.fecha_nacimiento)
          formData.fecha_nacimiento = date.toISOString().split('T')[0]
        } else {
          // Si no hay fecha, enviar null
          formData.fecha_nacimiento = null
        }

        const config = {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token'),
            'Content-Type': 'application/json'
          }
        }

        if (selectedAutor.value) {
          // EDITAR AUTOR EXISTENTE
          await axios.put(
            'http://localhost:5000/api/autores/${selectedAutor.value.id}',
            { ...formData },
            config
          )
        } else {
          // CREAR AUTOR NUEVO
          await axios.post('http://localhost:5000/api/autores/', formData, config)
        }

        await fetchAutores()
        modalVisible.value = false
      } catch (err) {
        if (err.response?.data?.detail?.includes('llave duplicada')) {
          error.value = 'Ya existe un autor con ese nombre'
        } else if (err.response?.status === 400) {
          error.value = 'Datos inválidos o incompletos'
        } else {
          error.value = 'Error al guardar el autor'
        }
        modalVisible.value = true
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchAutores)

    return {
      autores,
      autoresActivos,
      autoresInactivos,
      loading,
      error,
      modalVisible,
      selectedAutor,
      handleCreate,
      handleEdit,
      handleDeactivate,
      handleReactivate,
      handleModalSubmit
    }
  }
}
</script>