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
          <label for="nombre">Nombre:</label>
          <input
            type="text"
            id="nombre"
            v-model="form.nombre"
            class="form-control"
            required
          >
        </div>

        <div class="form-group">
          <label for="descripcion">Descripción:</label>
          <textarea
            id="descripcion"
            v-model="form.descripcion"
            class="form-control"
            rows="4"
          ></textarea>
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
  name: 'ModalGenero',
  components: { ModalBase },
  props: {
    show: Boolean,
    genero: Object
  },
  setup(props, { emit }) {
    const form = ref({
      nombre: '',
      descripcion: '',
      activo: true
    })

    watch(() => props.genero, (newGenero) => {
      if (newGenero) {
        form.value = { ...newGenero }
      } else {
        form.value = {
          nombre: '',
          descripcion: '',
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
      title: props.genero ? 'Editar Género' : 'Crear Género',
      submitText: props.genero ? 'Actualizar' : 'Crear'
    }
  }
}
</script>
