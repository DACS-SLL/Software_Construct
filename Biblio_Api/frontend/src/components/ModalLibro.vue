<template>
  <modal-base
    :show="show"
    :title="modalTitle"
    :submit-text="submitText"
    :disabled="!isFormValid"
    @close="handleClose"
    @submit="handleSubmit"
  >
    <template #body>
      <div class="modal-scroll-container">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <FormGroup label="Título:" required>
            <input type="text" v-model="form.titulo" class="form-control" required />
          </FormGroup>

          <FormGroup label="ISBN:">
            <input type="text" v-model="form.isbn" class="form-control" />
          </FormGroup>

          <FormGroup label="Año de Publicación:">
            <input type="number" v-model="form.anio_publicacion" class="form-control" />
          </FormGroup>

          <FormGroup label="Sinopsis:">
            <textarea v-model="form.sinopsis" rows="4" class="form-control"></textarea>
          </FormGroup>

          <FormGroup label="Páginas:">
            <input type="number" v-model="form.paginas" class="form-control" />
          </FormGroup>

          <FormGroup label="Autores:" required>
            <select v-model="form.autores" class="form-control" multiple size="4">
              <option v-for="a in autoresActivos" :key="a.id" :value="{ id: a.id }">
                {{ a.nombre }} {{ a.apellido }}
              </option>
            </select>
          </FormGroup>

          <FormGroup label="Géneros:">
            <select v-model="form.generos" class="form-control" multiple size="4">
              <option v-for="g in generosDisponibles" :key="g.id" :value="g.id">
                {{ g.nombre }}
              </option>
            </select>
          </FormGroup>

          <FormGroup label="Disponibilidad:" required>
            <div class="flex gap-4">
              <label class="flex items-center gap-1">
                <input type="radio" v-model="form.activo" :value="true" />
                Sí
              </label>
              <label class="flex items-center gap-1">
                <input type="radio" v-model="form.activo" :value="false" />
                No
              </label>
            </div>
          </FormGroup>
        </form>
      </div>
    </template>
  </modal-base>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import ModalBase from './ModalBase.vue'
import FormGroup from './FormGroup.vue'

const props = defineProps({
  show: Boolean,
  libro: Object,
  autoresActivos: Array,
  generosDisponibles: Array
})
const emit = defineEmits(['submit', 'close'])

const currentYear = new Date().getFullYear()
const form = ref(defaultForm())
const errors = ref(defaultErrors())

watch(() => props.libro, (libro) => {
  form.value = libro ? { ...defaultForm(), ...libro } : defaultForm()
  errors.value = defaultErrors()
}, { immediate: true })

const modalTitle = computed(() => props.libro ? 'Editar Libro' : 'Crear Libro')
const submitText = computed(() => props.libro ? 'Actualizar' : 'Crear')

const isFormValid = computed(() =>
  form.value.titulo.trim() && form.value.autores.length > 0 &&
  !Object.values(errors.value).some(e => e)
)

function defaultForm() {
  return { titulo: '', isbn: '', anio_publicacion: null, sinopsis: '', paginas: null, activo: true, autores: [], generos: [] }
}
function defaultErrors() {
  return { titulo: '', isbn: '', anio_publicacion: '', paginas: '', autores: '', generos: '' }
}

function validate(field) {
  const f = form.value
  const e = errors.value

  switch (field) {
    case 'titulo':
      e.titulo = f.titulo.trim() ? '' : 'El título es obligatorio'
      console.log('Validando título:', f.titulo, e.titulo)
      break
    case 'isbn':
      e.isbn = !f.isbn || /^(?:\d{9}[\dXx]|\d{13})$/.test(f.isbn) ? '' : 'ISBN no válido'
      console.log('Validando ISBM:', f.isbn, e.isbn)
      break
    case 'anio_publicacion':
      e.anio_publicacion = (f.anio_publicacion >= 1000 && f.anio_publicacion <= currentYear) ? '' : `Año inválido (1000–${currentYear})`
      console.log('Validando publi', f.anio_publicacion, e.anio_publicacion)
      break
    case 'paginas':
      e.paginas = f.paginas > 0 ? '' : 'Debe ser mayor a 0'
      console.log('Validando pagina:', f.paginas, e.paginas)
      break
    case 'autores':
      e.autores = f.autores.length ? '' : 'Seleccione al menos un autor'
      console.log('Validando autor:', f.autores, e.autores)
      break
    case 'genero':
      e.generos = f.generos.length ? '' : 'Seleccione al menos un Genero'
      console.log('Validando genero:', f.generos, e.generos)
      break
  }
}

function handleClose() {
  form.value = defaultForm()
  errors.value = defaultErrors()
  emit('close')
}

function handleSubmit() {
  ['titulo', 'isbn', 'anio_publicacion', 'paginas', 'autores', 'genero'].forEach(validate)
  if (isFormValid.value) {
    console.log('Datos enviados:', form.value)
    emit('submit', { ...form.value })
  } else {
    console.log('Formulario no válido:', errors.value)
  }
}

watch(() => props.autoresActivos, (newAutores) => {
  console.log('Autores activos en el modal:', newAutores)
}, { immediate: true })

watch(() => props.generosDisponibles, (newGeneros) => {
  console.log('Géneros disponibles en el modal:', newGeneros)
}, { immediate: true })
</script>

<style scoped>
.modal-scroll-container {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 1rem;
}
@media (max-width: 768px) {
  .modal-container {
    max-width: 100%;
    max-height: 90%;
    padding: 1rem;
  }

  .form-control {
    font-size: 14px;
  }
}
</style>
