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
          <label for="apellido">Apellido:</label>
          <input
            type="text"
            id="apellido"
            v-model="form.apellido"
            class="form-control"
            required
          >
        </div>

        <div class="form-group">
          <label for="fecha_nacimiento">Fecha de Nacimiento:</label>
          <input
            type="date"
            id="fecha_nacimiento"
            v-model="form.fecha_nacimiento"
            class="form-control"
          >
        </div>

        <div class="form-group">
          <label for="nacionalidad">Nacionalidad:</label>
          <input
            type="text"
            id="nacionalidad"
            v-model="form.nacionalidad"
            class="form-control"
          >
        </div>

        <div class="form-group">
          <label for="biografia">Biografía:</label>
          <textarea
            id="biografia"
            v-model="form.biografia"
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
import { ref, watch, computed } from 'vue'

export default {
  name: 'ModalAutor',
  components: { ModalBase },
  props: {
    show: Boolean,
    autor: Object
  },
  setup(props, { emit }) {
    const form = ref({
      nombre: '',
      apellido: '',
      fecha_nacimiento: '',
      nacionalidad: '',
      biografia: '',
      activo: true
    })

    watch(() => props.autor, (newAutor) => {
      if (newAutor) {
        form.value = {
          ...newAutor,
          fecha_nacimiento: newAutor.fecha_nacimiento && !isNaN(Date.parse(newAutor.fecha_nacimiento))
            ? new Date(newAutor.fecha_nacimiento).toISOString().split('T')[0]
            : ''
        }
      } else {
        form.value = {
          nombre: '',
          apellido: '',
          fecha_nacimiento: '',
          nacionalidad: '',
          biografia: '',
          activo: true
        }
      }
    }, { immediate: true })

    const handleSubmit = () => {
      if (!form.value.nombre || !form.value.apellido) {
        return alert('Nombre y apellido son obligatorios');
      }

      const datosEnviados = { ...form.value };
      delete datosEnviados.estado;
      delete datosEnviados.fecha_actualizacion;
      delete datosEnviados.fecha_creacion;
      delete datosEnviados.id; // God

      console.log('Datos enviados:', datosEnviados);
      emit('submit', datosEnviados);
      emit('close')

    }

    const title = computed(() => (props.autor ? 'Editar Autor' : 'Crear Autor'));

    return {
      form,
      handleSubmit,
      title,
      submitText: computed(() => (props.autor ? 'Actualizar' : 'Crear'))
    }
  }
}
</script>
