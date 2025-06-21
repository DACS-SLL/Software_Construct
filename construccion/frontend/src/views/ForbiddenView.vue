<template>
  <v-container class="fill-height">
    <v-row class="fill-height" align="center" justify="center">
      <v-col cols="12" md="8" lg="6" class="text-center">
        <!-- Error Icon -->
        <div class="mb-8">
          <v-icon 
            size="200" 
            color="error"
            class="error-icon"
          >
            mdi-shield-alert
          </v-icon>
        </div>
        
        <!-- Error Message -->
        <h1 class="text-h1 font-weight-bold text-error mb-4">403</h1>
        <h2 class="text-h4 mb-4">Acceso Prohibido</h2>
        <p class="text-h6 text-grey-darken-1 mb-8">
          No tienes permisos para acceder a esta página.
        </p>
        
        <!-- Explanation Card -->
        <v-card class="pa-6 mb-8" elevation="2">
          <h3 class="text-h5 mb-4">¿Por qué veo este error?</h3>
          <v-row>
            <v-col cols="12" md="6">
              <div class="d-flex align-center mb-4">
                <v-icon color="warning" size="24" class="mr-3">mdi-account-lock</v-icon>
                <div>
                  <h4 class="text-subtitle-1">Permisos insuficientes</h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Tu cuenta no tiene los permisos necesarios para esta sección.
                  </p>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <div class="d-flex align-center mb-4">
                <v-icon color="info" size="24" class="mr-3">mdi-account-question</v-icon>
                <div>
                  <h4 class="text-subtitle-1">Tipo de cuenta</h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Esta función puede estar limitada a ciertos tipos de usuarios.
                  </p>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <div class="d-flex align-center mb-4">
                <v-icon color="error" size="24" class="mr-3">mdi-clock-alert</v-icon>
                <div>
                  <h4 class="text-subtitle-1">Sesión expirada</h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Tu sesión puede haber expirado. Intenta iniciar sesión nuevamente.
                  </p>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <div class="d-flex align-center mb-4">
                <v-icon color="success" size="24" class="mr-3">mdi-account-check</v-icon>
                <div>
                  <h4 class="text-subtitle-1">Cuenta no verificada</h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Puede que necesites verificar tu cuenta primero.
                  </p>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card>
        
        <!-- User Info Card -->
        <v-card v-if="userInfo" class="pa-6 mb-8" color="grey-lighten-5">
          <h3 class="text-h6 mb-4">Información de tu cuenta:</h3>
          <v-row>
            <v-col cols="12" sm="6">
              <div class="text-left">
                <p><strong>Usuario:</strong> {{ userInfo.email }}</p>
                <p><strong>Tipo:</strong> {{ userInfo.user_type || userInfo.rol }}</p>
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-left">
                <p><strong>Estado:</strong> 
                  <v-chip 
                    :color="userInfo.activo ? 'success' : 'error'" 
                    size="small"
                  >
                    {{ userInfo.activo ? 'Activo' : 'Inactivo' }}
                  </v-chip>
                </p>
              </div>
            </v-col>
          </v-row>
        </v-card>
        
        <!-- Action Buttons -->
        <v-card class="pa-6 mb-8" elevation="1">
          <h3 class="text-h6 mb-4">¿Qué puedes hacer?</h3>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-btn
                color="primary"
                size="large"
                block
                @click="$router.push('/')"
                prepend-icon="mdi-home"
              >
                Ir al Inicio
              </v-btn>
            </v-col>
            
            <v-col cols="12" sm="6" md="3">
              <v-btn
                color="success"
                variant="outlined"
                size="large"
                block
                @click="refreshLogin"
                prepend-icon="mdi-refresh"
              >
                Actualizar Sesión
              </v-btn>
            </v-col>
            
            <v-col cols="12" sm="6" md="3">
              <v-btn
                color="warning"
                variant="outlined"
                size="large"
                block
                @click="$router.push('/mi-perfil')"
                prepend-icon="mdi-account"
              >
                Mi Perfil
              </v-btn>
            </v-col>
            
            <v-col cols="12" sm="6" md="3">
              <v-btn
                color="info"
                variant="outlined"
                size="large"
                block
                @click="$router.push('/contact')"
                prepend-icon="mdi-help"
              >
                Ayuda
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
        
        <!-- Access Level Information -->
        <v-expansion-panels class="mb-8">
          <v-expansion-panel>
            <v-expansion-panel-title>
              <strong>Niveles de acceso en la plataforma</strong>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-row>
                <v-col cols="12" md="4">
                  <v-card class="pa-4" outlined>
                    <h4 class="text-h6 mb-2 text-success">Postulante</h4>
                    <ul class="text-body-2">
                      <li>Ver ofertas de trabajo</li>
                      <li>Postular a empleos</li>
                      <li>Gestionar CV</li>
                      <li>Ver mis postulaciones</li>
                    </ul>
                  </v-card>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-card class="pa-4" outlined>
                    <h4 class="text-h6 mb-2 text-primary">Empresa</h4>
                    <ul class="text-body-2">
                      <li>Publicar ofertas</li>
                      <li>Ver postulantes</li>
                      <li>Gestionar entrevistas</li>
                    <ul class="text-body-2">
                      <li>Publicar ofertas</li>
                      <li>Ver postulantes</li>
                      <li>Gestionar entrevistas</li>
                      <li>Dashboard de empresa</li>
                    </ul>
                  </v-card>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-card class="pa-4" outlined>
                    <h4 class="text-h6 mb-2 text-warning">Administrador</h4>
                    <ul class="text-body-2">
                      <li>Gestión completa</li>
                      <li>Moderar contenido</li>
                      <li>Ver estadísticas</li>
                      <li>Administrar usuarios</li>
                    </ul>
                  </v-card>
                </v-col>
              </v-row>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
        
        <!-- Back Button -->
        <div class="d-flex gap-4 justify-center">
          <v-btn
            size="large"
            variant="outlined"
            @click="$router.go(-1)"
            prepend-icon="mdi-arrow-left"
          >
            Volver Atrás
          </v-btn>
          
          <v-btn
            size="large"
            color="primary"
            @click="$router.push('/')"
            prepend-icon="mdi-home"
          >
            Ir al Inicio
          </v-btn>
        </div>
        
        <!-- Help Section -->
        <div class="mt-8 pt-8" style="border-top: 1px solid #e0e0e0;">
          <p class="text-body-2 text-grey-darken-1 mb-4">
            Si crees que esto es un error, contáctanos y te ayudaremos.
          </p>
          <v-btn
            variant="text"
            color="primary"
            @click="$router.push('/contact')"
          >
            Contactar Soporte
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userInfo = ref(null)

const refreshLogin = () => {
  // Limpiar datos de sesión y redirigir al login
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  // Intentar obtener información del usuario actual
  const userData = localStorage.getItem('user')
  if (userData) {
    try {
      userInfo.value = JSON.parse(userData)
    } catch (error) {
      console.error('Error parsing user data:', error)
    }
  }
})
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.error-icon {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.gap-4 {
  gap: 16px;
}

ul {
  padding-left: 20px;
}

li {
  margin-bottom: 4px;
}
</style>