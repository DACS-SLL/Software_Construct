<template>
  <v-container fluid class="d-flex align-center justify-center" style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <v-card class="pa-8" max-width="400" width="100%" elevation="10">
      <div class="text-center mb-6">
        <v-icon size="64" color="primary">mdi-briefcase</v-icon>
        <h1 class="text-h4 mt-4">Iniciar Sesión</h1>
      </div>
      
      <v-form @submit.prevent="handleLogin">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          variant="outlined"
          class="mb-4"
          prepend-inner-icon="mdi-email"
        ></v-text-field>
        
        <v-text-field
          v-model="password"
          label="Contraseña"
          type="password"
          variant="outlined"
          class="mb-4"
          prepend-inner-icon="mdi-lock"
        ></v-text-field>
        
        <v-btn
          type="submit"
          color="primary"
          block
          size="large"
          :loading="loading"
        >
          Iniciar Sesión
        </v-btn>
      </v-form>
      
      <div class="text-center mt-4">
        <v-btn variant="text" @click="$router.push('/register')">
          ¿No tienes cuenta? Regístrate
        </v-btn>
      </div>
    </v-card>
    
    <v-snackbar v-model="snackbar.show" :color="snackbar.color">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '/src/api/api'

const router = useRouter()
const email = ref('daniel@example.com')
const password = ref('123456')
const loading = ref(false)

const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})

const handleLogin = async () => {
  loading.value = true
  
  try {
    const response = await api.login({
      email: email.value,
      password: password.value
    })
    
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    snackbar.value = {
      show: true,
      message: 'Login exitoso!',
      color: 'success'
    }
    
    setTimeout(() => {
      router.push('/')
    }, 1000)
    
  } catch (error) {
    snackbar.value = {
      show: true,
      message: 'Error en el login',
      color: 'error'
    }
  } finally {
    loading.value = false
  }
}
</script>