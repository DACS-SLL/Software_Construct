<template>
  <base-list
    title="Géneros"
    :headers="['Nombre', 'Descripción', 'Estado']"
    :items="generos"
    :loading="loading"
    :error="error"
    @create="handleCreate"
    @edit="handleEdit"
    @delete="handleDelete"
  />

  <modal-genero
    :show="modalVisible"
    :genero="selectedGenero"
    @submit="handleModalSubmit"
    @close="modalVisible = false"
  />
</template>

<script>
import BaseList from './BaseList.vue'
import ModalGenero from './ModalGenero.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Generos',
  components: { BaseList, ModalGenero },
  setup() {
    const generos = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchGeneros = async () => {
      try {
        loading.value = true
        const response = await axios.get('http://localhost:5000/api/generos')
        generos.value = response.data
        error.value = null
      } catch (err) {
        error.value = 'Error al cargar los géneros'
      } finally {
        loading.value = false
      }
    }

    const modalVisible = ref(false)
    const selectedGenero = ref(null)

    const handleCreate = () => {
      modalVisible.value = true
      selectedGenero.value = null
    }

    const handleEdit = (genero) => {
      modalVisible.value = true
      selectedGenero.value = genero
    }

    const handleDelete = async (genero) => {
      try {
        await axios.delete(`http://localhost:5000/api/generos/${genero.id}`)
        await fetchGeneros()
      } catch (err) {
        error.value = 'Error al eliminar el género'
      }
    }

    onMounted(fetchGeneros)

    const handleModalSubmit = async (formData) => {
      try {
        loading.value = true
        if (selectedGenero.value) {
          // Actualizar género
          await axios.put(`http://localhost:5000/api/generos/${selectedGenero.value.id}`, formData)
        } else {
          // Crear nuevo género
          await axios.post('http://localhost:5000/api/generos', formData)
        }
        await fetchGeneros()
      } catch (err) {
        error.value = 'Error al guardar el género'
      } finally {
        loading.value = false
      }
    }

    return {
      generos,
      loading,
      error,
      handleCreate,
      handleEdit,
      handleDelete,
      modalVisible,
      selectedGenero,
      handleModalSubmit
    }
  }
}
</script>
