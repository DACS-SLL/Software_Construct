<template>
  <modal-base
    :show="show"
    :title="title"
    :submitText="submitText"
    @close="$emit('close')"
    @submit="handleSubmit"
  >
    <template #body>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="titulo">Título:</label>
          <input
            type="text"
            id="titulo"
            v-model="form.titulo"
            class="form-control"
            required
          >
        </div>

        <div class="form-group">
          <label for="isbn">ISBN:</label>
          <input
            type="text"
            id="isbn"
            v-model="form.isbn"
            class="form-control"
          >
        </div>

        <div class="form-group">
          <label for="anio_publicacion">Año de Publicación:</label>
          <input
            type="number"
            id="anio_publicacion"
            v-model="form.anio_publicacion"
            class="form-control"
          >
        </div>

        <div class="form-group">
          <label for="sinopsis">Sinopsis:</label>
          <textarea
            id="sinopsis"
            v-model="form.sinopsis"
            class="form-control"
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="paginas">Páginas:</label>
          <input
            type="number"
            id="paginas"
            v-model="form.paginas"
            class="form-control"
          >
        </div>

        <div class="form-group">
          <label>Estado:</label>
          <div class="form-control">
            <label>
              <input
                type="radio"
                v-model="form.activo"
                :value="true"
              >
              Activo
            </label>
            <label>
              <input
                type="radio"
                v-model="form.activo"
                :value="false"
              >
              Inactivo
            </label>
          </div>
        </div>
      </form>
    </template>
  </modal-base>
</template>

<script>
import ModalBase from './ModalBase.vue'
import { ref, watch } from 'vue'

export default {
  name: 'ModalLibro',
  components: { ModalBase },
  props: {
    show: Boolean,
    libro: Object
  },
  setup(props, { emit }) {
    const form = ref({
      titulo: '',
      isbn: '',
      anio_publicacion: '',
      sinopsis: '',
      paginas: '',
      activo: true
    })

    watch(() => props.libro, (newLibro) => {
      if (newLibro) {
        form.value = { ...newLibro }
      } else {
        form.value = {
          titulo: '',
          isbn: '',
          anio_publicacion: '',
          sinopsis: '',
          paginas: '',
          activo: true
        }
      }
    }, { immediate: true })

    const handleSubmit = () => {
      emit('submit', form.value)
      emit('close')
    }

    return {
      form,
      handleSubmit,
      title: props.libro ? 'Editar Libro' : 'Crear Libro',
      submitText: props.libro ? 'Actualizar' : 'Crear'
    }
  }
}
</script>
