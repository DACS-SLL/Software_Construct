<template>
  <v-container fill-height>
    <v-row justify="center" align="center">
      <v-col cols="12" md="8" lg="6" class="text-center">
        <v-card class="pa-8" elevation="4">
          <!-- Icono grande de error -->
          <v-icon 
            size="120" 
            color="error" 
            class="mb-4"
          >
            mdi-alert-circle-outline
          </v-icon>
          
          <!-- Título principal -->
          <h1 class="text-h2 font-weight-bold mb-4 text-error">
            404
          </h1>
          
          <!-- Mensaje de error -->
          <h2 class="text-h4 mb-4">
            Página No Encontrada
          </h2>
          
          <p class="text-h6 mb-6 text-grey-darken-1">
            Lo sentimos, la página que estás buscando no existe o ha sido movida.
          </p>
          
          <!-- Sugerencias útiles -->
          <v-card 
            variant="outlined" 
            class="pa-4 mb-6 text-left"
          >
            <v-card-title class="text-h6 pa-0 mb-3">
              <v-icon color="info" class="mr-2">mdi-lightbulb-outline</v-icon>
              ¿Qué puedes hacer?
            </v-card-title>
            
            <v-list density="compact" class="pa-0">
              <v-list-item class="pa-0 mb-2">
                <template v-slot:prepend>
                  <v-icon size="small" color="primary">mdi-check</v-icon>
                </template>
                <v-list-item-title class="text-body-1">
                  Verifica que la URL esté escrita correctamente
                </v-list-item-title>
              </v-list-item>
              
              <v-list-item class="pa-0 mb-2">
                <template v-slot:prepend>
                  <v-icon size="small" color="primary">mdi-check</v-icon>
                </template>
                <v-list-item-title class="text-body-1">
                  Utiliza el menú de navegación para encontrar lo que buscas
                </v-list-item-title>
              </v-list-item>
              
              <v-list-item class="pa-0 mb-2">
                <template v-slot:prepend>
                  <v-icon size="small" color="primary">mdi-check</v-icon>
                </template>
                <v-list-item-title class="text-body-1">
                  Regresa a la página principal y navega desde allí
                </v-list-item-title>
              </v-list-item>
              
              <v-list-item class="pa-0">
                <template v-slot:prepend>
                  <v-icon size="small" color="primary">mdi-check</v-icon>
                </template>
                <v-list-item-title class="text-body-1">
                  Contáctanos si crees que esto es un error
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card>
          
          <!-- Botones de acción -->
          <div class="d-flex flex-column flex-sm-row justify-center gap-3">
            <v-btn
              color="primary"
              size="large"
              @click="goHome"
              prepend-icon="mdi-home"
            >
              Ir al Inicio
            </v-btn>
            
            <v-btn
              color="secondary"
              variant="outlined"
              size="large"
              @click="goBack"
              prepend-icon="mdi-arrow-left"
            >
              Volver Atrás
            </v-btn>
            
            <v-btn
              color="info"
              variant="outlined"
              size="large"
              @click="$router.push('/contact')"
              prepend-icon="mdi-help-circle"
            >
              Ayuda
            </v-btn>
          </div>
          
          <!-- Enlaces útiles -->
          <v-divider class="my-6"></v-divider>
          
          <div>
            <h3 class="text-h6 mb-4">Enlaces Útiles</h3>
            <div class="d-flex flex-wrap justify-center gap-2">
              <v-chip
                v-for="link in quickLinks"
                :key="link.name"
                :to="link.route"
                color="primary"
                variant="outlined"
                class="ma-1"
                clickable
              >
                <v-icon start>{{ link.icon }}</v-icon>
                {{ link.name }}
              </v-chip>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// Enlaces rápidos útiles
const quickLinks = [
  { name: 'Ofertas', route: '/ofertas', icon: 'mdi-briefcase' },
  { name: 'Empresas', route: '/empresas', icon: 'mdi-domain' },
  { name: 'Postulantes', route: '/postulantes', icon: 'mdi-account-group' },
  { name: 'Acerca de', route: '/about', icon: 'mdi-information' },
  { name: 'Contacto', route: '/contact', icon: 'mdi-email' }
]

// Métodos de navegación
const goHome = () => {
  router.push('/')
}

const goBack = () => {
  // Si hay historial, ir atrás, sino ir al inicio
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.gap-3 > * {
  margin: 4px;
}

@media (max-width: 600px) {
  .gap-3 {
    flex-direction: column;
  }
  
  .gap-3 > * {
    margin: 8px 0;
    width: 100%;
  }
}

.v-chip {
  transition: transform 0.2s ease;
}

.v-chip:hover {
  transform: translateY(-2px);
}
</style>