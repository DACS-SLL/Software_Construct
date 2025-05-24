<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Biblioteca API</h2>
      <div class="login-form">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            class="form-control"
            required
            autofocus
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
          >
        </div>

        <div class="form-group">
          <button class="btn btn-primary" @click="handleLogin" :disabled="loading">
            <span v-if="loading">Iniciando sesión...</span>
            <span v-else>Iniciar Sesión</span>
          </button>
        </div>

        <div class="alert alert-danger" v-if="error">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const form = ref({
      username: '',
      password: ''
    })
    const loading = ref(false)
    const error = ref(null)

    const handleLogin = async () => {
      try {
        loading.value = true
        error.value = null

        const response = await axios.post('http://localhost:5000/api/auth/login', {
          username: form.value.username,
          password: form.value.password
        })

        // Guardar el token en localStorage
        localStorage.setItem('token', response.data.data.token)
localStorage.setItem('user', JSON.stringify(response.data.data.usuario))
        // Redirigir al dashboard
        router.push('/dashboard')
      } catch (err) {
        error.value = err.response?.data?.message || 'Error al iniciar sesión'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--background-color);
}

.login-box {
  background-color: white;
  padding: 2rem;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  width: 100%;
  max-width: 400px;
}

.login-box h2 {
  text-align: center;
  color: var(--primary-color);
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
}

.form-group button {
  width: 100%;
  padding: 0.75rem;
}

.alert {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: var(--border-radius);
}
</style>
