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
          <label for="username">Usuario:</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            class="form-control"
            required
            placeholder="Ingrese su nombre de usuario"
          >
        </div>

        <div class="form-group">
          <label for="email">Email:</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            class="form-control"
            required
            placeholder="Ingrese su email"
          >
        </div>

        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            class="form-control"
            required
            placeholder="Ingrese su contraseña"
          >
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirmar Contraseña:</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="form.confirmPassword"
            class="form-control"
            required
            placeholder="Confirme su contraseña"
          >
        </div>
      </form>
    </template>
  </modal-base>
</template>

<script>
import ModalBase from './ModalBase.vue'
import { ref, watch } from 'vue'

export default {
  name: 'ModalRegister',
  components: { ModalBase },
  props: {
    show: Boolean
  },
  setup(props, { emit }) {
    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const title = 'Registro de Usuario'
    const submitText = 'Registrar'

    const handleSubmit = () => {
      if (form.value.password !== form.value.confirmPassword) {
        alert('Las contraseñas no coinciden')
        return
      }

      emit('submit', form.value)
    }

    return {
      form,
      title,
      submitText,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

.form-control {
  border-radius: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ced4da;
}

.form-control:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}
</style>
