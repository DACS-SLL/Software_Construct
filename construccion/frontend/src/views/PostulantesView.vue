<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" @click="openDialog(null)">
          <v-icon left>mdi-plus</v-icon> Nuevo Postulante
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="postulantes"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.fecha_nacimiento="{ item }">
        {{ formatDate(item.fecha_nacimiento) }}
      </template>
      
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedItem.nombre_completo"
              label="Nombre Completo"
              :rules="[v => !!v || 'Nombre es requerido']"
            ></v-text-field>

            <v-text-field
              v-model="editedItem.telefono"
              label="Teléfono"
            ></v-text-field>

            <v-date-picker
              v-model="editedItem.fecha_nacimiento"
              label="Fecha de Nacimiento"
              :max="new Date().toISOString().split('T')[0]"
            ></v-date-picker>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDialog">
            Cancelar
          </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="save">
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title>¿Estás seguro de eliminar este postulante?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancelar</v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">Eliminar</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '/src/api/api'

const loading = ref(false)
const dialog = ref(false)
const dialogDelete = ref(false)
const headers = ref([
  { title: 'Nombre Completo', value: 'nombre_completo' },
  { title: 'Teléfono', value: 'telefono' },
  { title: 'Fecha Nacimiento', value: 'fecha_nacimiento' },
  { title: 'Acciones', value: 'actions', sortable: false }
])
const postulantes = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  nombre_completo: '',
  telefono: '',
  fecha_nacimiento: null
})
const defaultItem = ref({ ...editedItem.value })
const form = ref(null)

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Nuevo Postulante' : 'Editar Postulante'
})

onMounted(() => {
  fetchPostulantes()
})

async function fetchPostulantes() {
  try {
    loading.value = true
    const response = await api.getPostulantes()
    postulantes.value = response.data
  } catch (error) {
    console.error('Error al obtener postulantes:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

function openDialog(item) {
  editedIndex.value = postulantes.value.indexOf(item)
  editedItem.value = Object.assign({}, item || defaultItem.value)
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
}

function confirmDelete(item) {
  editedIndex.value = postulantes.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

function closeDelete() {
  dialogDelete.value = false
  editedIndex.value = -1
}

async function deleteItemConfirm() {
  try {
    await api.deletePostulante(editedItem.value.id)
    postulantes.value.splice(editedIndex.value, 1)
    closeDelete()
  } catch (error) {
    console.error('Error al eliminar postulante:', error)
  }
}

async function save() {
  const { valid } = await form.value.validate()
  if (!valid) return

  try {
    if (editedIndex.value > -1) {
      // Editar
      const response = await api.updatePostulante(editedItem.value.id, editedItem.value)
      Object.assign(postulantes.value[editedIndex.value], response.data)
    } else {
      // Crear
      const response = await api.createPostulante(editedItem.value)
      postulantes.value.push(response.data)
    }
    closeDialog()
  } catch (error) {
    console.error('Error al guardar postulante:', error)
  }
}
</script>