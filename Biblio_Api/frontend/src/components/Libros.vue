<template>
  <base-list
    title="Libros"
    :headers="['Título', 'Autores', 'Géneros', 'Año Publicación', 'ISBN', 'Páginas', 'Estado']"
    :items="libros"
    :loading="loading"
    :error="error"
    @create="handleCreate"
    @edit="handleEdit"
    @delete="handleDelete"
  />

  <modal-libro
    :show="modalVisible"
    :libro="selectedLibro"
    @submit="handleModalSubmit"
    @close="modalVisible = false"
  />
</template>

<script>
import BaseList from './BaseList.vue'
import ModalLibro from './ModalLibro.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Libros',
  components: { BaseList, ModalLibro },
  setup() {
    const libros = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchLibros = async () => {
      try {
        loading.value = true
        const response = await axios.get('http://localhost:5000/api/libros')
        libros.value = response.data.data.map(libro => ({
          ...libro,
          autores: libro.autores ? libro.autores.map(autor => `${autor.nombre} ${autor.apellido}`).join(', ') : '',
          generos: libro.generos ? libro.generos.map(genero => genero.nombre).join(', ') : '',
          estado: libro.activo ? 'Activo' : 'Inactivo'
        }))
        error.value = null
      } catch (err) {
        error.value = 'Error al cargar los libros'
      } finally {
        loading.value = false
      }
    }

    const modalVisible = ref(false)
    const selectedLibro = ref(null)

    const handleCreate = () => {
      modalVisible.value = true
      selectedLibro.value = null
    }

    const handleEdit = (libro) => {
      modalVisible.value = true
      selectedLibro.value = libro
    }

    const handleDelete = async (libro) => {
      try {
        await axios.delete(`http://localhost:5000/api/libros/${libro.id}`)
        await fetchLibros()
      } catch (err) {
        error.value = 'Error al eliminar el libro'
      }
    }

    onMounted(fetchLibros)

    const handleModalSubmit = async (formData) => {
      try {
        loading.value = true
        if (selectedLibro.value) {
          // Actualizar libro
          await axios.put(`http://localhost:5000/api/libros/${selectedLibro.value.id}`, formData)
        } else {
          // Crear nuevo libro
          await axios.post('http://localhost:5000/api/libros', formData)
        }
        await fetchLibros()
      } catch (err) {
        error.value = 'Error al guardar el libro'
      } finally {
        loading.value = false
      }
    }

    return {
      libros,
      loading,
      error,
      handleCreate,
      handleEdit,
      handleDelete,
      modalVisible,
      selectedLibro,
      handleModalSubmit
    }
  }
}
</script>
