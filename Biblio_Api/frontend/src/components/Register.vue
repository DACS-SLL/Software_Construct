<template>
  <div class="register-page">
    <div class="register-container">
      <h2>Registro</h2>
      
      <div class="form-container">
        <form @submit.prevent="handleSubmit">
          <FormGroup label="Usuario:">
            <input
              type="text"
              v-model="form.username"
              class="form-control"
              required
              placeholder="Ingrese su nombre de usuario"
            >
          </FormGroup>

          <FormGroup label="Email:">
            <input
              type="email"
              v-model="form.email"
              class="form-control"
              required
              placeholder="Ingrese su email"
            >
          </FormGroup>

          <FormGroup label="Contraseña:">
            <input
              type="password"
              v-model="form.password"
              class="form-control"
              required
              placeholder="Ingrese su contraseña"
            >
          </FormGroup>

          <FormGroup label="Confirmar Contraseña:">
            <input
              type="password"
              v-model="form.confirmPassword"
              class="form-control"
              required
              placeholder="Confirme su contraseña"
            >
          </FormGroup>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary w-100">
              <span v-if="loading">Registrando...</span>
              <span v-else>Registrarse</span>
            </button>
          </div>

          <div class="text-center mt-3">
            <router-link to="/login" class="text-decoration-none">
              ¿Ya tienes cuenta? Inicia sesión
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import FormGroup from './FormGroup.vue'
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  components: { FormGroup },
  setup() {
    const router = useRouter()
    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    const loading = ref(false)

    const handleSubmit = async () => {
      if (form.value.password !== form.value.confirmPassword) {
        alert('Las contraseñas no coinciden')
        return
      }

      try {
        loading.value = true
        await axios.post('http://localhost:5000/api/auth/register', {
          username: form.value.username,
          email: form.value.email,
          password: form.value.password
        })
        
        alert('Registro exitoso! Por favor, inicia sesión.')
        router.push('/login')
      } catch (error) {
        alert(error.response?.data?.detail || 'Error al registrar el usuario')
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.register-container {
  background-color: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-container {
  margin-top: 2rem;
}

.form-actions {
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem;
  font-weight: 500;
}

.text-center {
  margin-top: 1rem;
}

.text-decoration-none {
  color: #0d6efd;
}

.text-decoration-none:hover {
  color: #0a58ca;
}
</style>
