<template>
  <v-container fluid class="d-flex align-center justify-center" style="min-height: 100vh; background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);">
    <v-card class="pa-8" max-width="500" width="100%" elevation="10">
      <div class="text-center mb-6">
        <v-icon size="64" color="primary">mdi-account-plus</v-icon>
        <h1 class="text-h4 mt-4">Registro</h1>
      </div>
      
      <v-form @submit.prevent="handleRegister">
        <v-text-field
          v-model="form.nombre"
          label="Nombre completo"
          variant="outlined"
          class="mb-4"
          prepend-inner-icon="mdi-account"
        ></v-text-field>
        
        <v-text-field
          v-model="form.email"
          label="Email"
          type="email"
          variant="outlined"
          class="mb-4"
          prepend-inner-icon="mdi-email"
        ></v-text-field>
        
        <v-text-field
          v-model="form.password"
          label="Contraseña"
          type="password"
          variant="outlined"
          class="mb-4"
          prepend-inner-icon="mdi-lock"
        ></v-text-field>
        
        <v-select
          v-model="form.user_type"
          :items="userTypes"
          label="Tipo de usuario"
          variant="outlined"
          class="mb-4"
          prepend-inner-icon="mdi-account-group"
        ></v-select>
        
        <v-btn
          type="submit"
          color="primary"
          block
          size="large"
          :loading="loading"
        >
          Registrarse
        </v-btn>
      </v-form>
      
      <div class="text-center mt-4">
        <v-btn variant="text" @click="$router.push('/login')">
          ¿Ya tienes cuenta? Inicia sesión
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
const loading = ref(false)

const form = ref({
  nombre: '',
  email: '',
  password: '',
  user_type: 'postulante'
})

const userTypes = [
  { title: 'Postulante', value: 'postulante' },
  { title: 'Empresa', value: 'empresa' }
]

const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})

const handleRegister = async () => {
  loading.value = true
  
  try {
    const userData = {
      email: form.value.email,
      password: form.value.password,
      nombre: form.value.nombre,
      user_type: form.value.user_type,
      rol_id: 2
    }
    
    if (form.value.user_type === 'postulante') {
      userData.nombre_completo = form.value.nombre
    } else {
      userData.nombre_empresa = form.value.nombre
    }
    
    await api.register(userData)
    
    snackbar.value = {
      show: true,
      message: 'Registro exitoso! Ahora puedes iniciar sesión',
      color: 'success'
    }
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
    
  } catch (error) {
    snackbar.value = {
      show: true,
      message: 'Error en el registro',
      color: 'error'
    }
  } finally {
    loading.value = false
  }
}
</script>