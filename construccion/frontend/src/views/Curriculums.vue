<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" @click="openDialog(null)">
          <v-icon left>mdi-plus</v-icon> Nuevo Currículum
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="curriculums"
      :loading="loading"
      class="elevation-1"
    >
        <template v-slot:item.ruta_archivo="{ item }">
        <a :href="item.ruta_archivo" target="_blank" rel="noopener noreferrer">
            Ver archivo
        </a>
        </template>

      <template v-slot:item.postulante="{ item }">
        {{ item.postulante?.nombre }} {{ item.postulante?.apellido }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Diálogo de Crear / Editar -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form">
            <v-text-field
            v-model="editedItem.ruta_archivo"
            label="Ruta del archivo (URL)"
            :rules="[
                v => !!v || 'Requerido',
                v => /^(https?:\/\/)[\w\-]+(\.[\w\-]+)+[/#?]?.*$/.test(v) || 'Debe ser una URL válida'
            ]"
            />

            <v-select
              v-model="editedItem.postulante_id"
              :items="postulantes"
              item-title="nombre_completo"
              item-value="id"
              label="Postulante"
              :rules="[v => !!v || 'Requerido']"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" color="grey" @click="closeDialog">Cancelar</v-btn>
          <v-btn variant="text" color="primary" @click="save">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Diálogo de Eliminar -->
    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title>¿Eliminar currículum?</v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" color="grey" @click="closeDelete">Cancelar</v-btn>
          <v-btn variant="text" color="red" @click="deleteItemConfirm">Eliminar</v-btn>
          <v-spacer />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api/api'

const loading = ref(false)
const dialog = ref(false)
const dialogDelete = ref(false)

const headers = [
  { title: 'ID', value: 'id' },
  { title: 'Postulante', value: 'postulante' },
  { title: 'Ruta Archivo', value: 'ruta_archivo' },
  { title: 'Fecha Subida', value: 'fecha_subida' },
  { title: 'Acciones', value: 'actions', sortable: false }
]

const curriculums = ref([])
const postulantes = ref([])

const editedIndex = ref(-1)
const editedItem = ref({
  postulante_id: null,
  ruta_archivo: ''
})
const defaultItem = ref({ ...editedItem.value })
const form = ref(null)

const formTitle = computed(() => (editedIndex.value === -1 ? 'Nuevo Currículum' : 'Editar Currículum'))

onMounted(() => {
  fetchCurriculums()
  fetchPostulantes()
})

async function fetchCurriculums() {
  try {
    loading.value = true
    const response = await api.getCurriculums()
    curriculums.value = response.data
  } catch (error) {
    console.error('Error al obtener currículums:', error)
  } finally {
    loading.value = false
  }
}

async function fetchPostulantes() {
  try {
    const response = await api.getPostulantes()
    postulantes.value = response.data.map(p => ({
      ...p,
      nombre_completo: `${p.nombre} ${p.apellido}`
    }))
  } catch (error) {
    console.error('Error al obtener postulantes:', error)
  }
}

function openDialog(item) {
  editedIndex.value = curriculums.value.indexOf(item)
  editedItem.value = Object.assign({}, item || defaultItem.value)
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
}

function confirmDelete(item) {
  editedIndex.value = curriculums.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

function closeDelete() {
  dialogDelete.value = false
  editedIndex.value = -1
}

async function deleteItemConfirm() {
  try {
    await api.deleteCurriculum(editedItem.value.id)
    curriculums.value.splice(editedIndex.value, 1)
    closeDelete()
  } catch (error) {
    console.error('Error al eliminar currículum:', error)
  }
}

async function save() {
  const { valid } = await form.value.validate()
  if (!valid) return

  try {
    if (editedIndex.value > -1) {
      const response = await api.updateCurriculum(editedItem.value.id, editedItem.value)
      Object.assign(curriculums.value[editedIndex.value], response.data)
    } else {
      const response = await api.createCurriculum(editedItem.value)
      curriculums.value.push(response.data)
    }
    closeDialog()
  } catch (error) {
    console.error('Error al guardar currículum:', error)
  }
}
</script>
