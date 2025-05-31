<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" @click="openDialog(null)">
          <v-icon left>mdi-plus</v-icon> Nueva Oferta
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="ofertas"
      :loading="loading"
      class="elevation-1"
    >
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
              v-model="editedItem.titulo"
              label="Título"
              :rules="[v => !!v || 'Título es requerido']"
            ></v-text-field>

            <v-textarea
              v-model="editedItem.descripcion"
              label="Descripción"
              rows="3"
            ></v-textarea>

            <v-text-field
              v-model="editedItem.ubicacion"
              label="Ubicación"
            ></v-text-field>

            <v-select
              v-model="editedItem.categoria_id"
              :items="categorias"
              item-title="nombre"
              item-value="id"
              label="Categoría"
              :rules="[v => !!v || 'Categoría es requerida']"
            ></v-select>

            <v-select
              v-model="editedItem.empresa_id"
              :items="empresas"
              item-title="nombre"
              item-value="id"
              label="Empresa"
              :rules="[v => !!v || 'Empresa es requerida']"
            ></v-select>

            <v-select
              v-model="editedItem.estado"
              :items="estadosOferta"
              label="Estado"
            ></v-select>
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
        <v-card-title>¿Estás seguro de eliminar esta oferta?</v-card-title>
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
  { title: 'Título', value: 'titulo' },
  { title: 'Empresa', value: 'empresa.nombre' },
  { title: 'Ubicación', value: 'ubicacion' },
  { title: 'Estado', value: 'estado' },
  { title: 'Acciones', value: 'actions', sortable: false }
])
const ofertas = ref([])
const categorias = ref([])
const empresas = ref([])
const estadosOferta = ref(['activa', 'cerrada', 'pausada'])
const editedIndex = ref(-1)
const editedItem = ref({
  titulo: '',
  descripcion: '',
  ubicacion: '',
  categoria_id: null,
  empresa_id: null,
  estado: 'activa'
})
const defaultItem = ref({ ...editedItem.value })
const form = ref(null)

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Nueva Oferta' : 'Editar Oferta'
})

onMounted(() => {
  fetchOfertas()
  fetchCategorias()
  fetchEmpresas()
})

async function fetchOfertas() {
  try {
    loading.value = true
    const response = await api.getOfertas()
    ofertas.value = response.data
  } catch (error) {
    console.error('Error al obtener ofertas:', error)
  } finally {
    loading.value = false
  }
}

async function fetchCategorias() {
  try {
    const response = await api.getCategorias()
    categorias.value = response.data
  } catch (error) {
    console.error('Error al obtener categorías:', error)
  }
}

async function fetchEmpresas() {
  try {
    const response = await api.getEmpresas()
    empresas.value = response.data
  } catch (error) {
    console.error('Error al obtener empresas:', error)
  }
}

function openDialog(item) {
  editedIndex.value = ofertas.value.indexOf(item)
  editedItem.value = Object.assign({}, item || defaultItem.value)
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
}

function confirmDelete(item) {
  editedIndex.value = ofertas.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

function closeDelete() {
  dialogDelete.value = false
  editedIndex.value = -1
}

async function deleteItemConfirm() {
  try {
    await api.deleteOferta(editedItem.value.id)
    ofertas.value.splice(editedIndex.value, 1)
    closeDelete()
  } catch (error) {
    console.error('Error al eliminar oferta:', error)
  }
}

async function save() {
  const { valid } = await form.value.validate()
  if (!valid) return

  try {
    if (editedIndex.value > -1) {
      // Editar
      const response = await api.updateOferta(editedItem.value.id, editedItem.value)
      Object.assign(ofertas.value[editedIndex.value], response.data)
    } else {
      // Crear
      const response = await api.createOferta(editedItem.value)
      ofertas.value.push(response.data)
    }
    closeDialog()
  } catch (error) {
    console.error('Error al guardar oferta:', error)
  }
}
</script>