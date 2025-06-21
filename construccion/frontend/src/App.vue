<template>
  <v-app>
    <!-- App Bar - Solo mostrar si no es una página de auth -->
    <v-app-bar 
      v-if="!hideNavigation" 
      color="primary" 
      prominent
      elevation="2"
      class="app-header"
    >
      <v-app-bar-nav-icon 
        v-if="isMobile" 
        @click="drawer = !drawer"
      />
      
      <v-toolbar-title 
        @click="navigateHome" 
        class="cursor-pointer d-flex align-center"
      >
        <v-icon size="28" class="mr-2">mdi-briefcase</v-icon>
        <span class="hidden-sm-and-down">Plataforma de Empleo</span>
        <span class="hidden-md-and-up">Empleos</span>
      </v-toolbar-title>
      
      <!-- Navegación desktop -->
      <div v-if="!isMobile" class="ml-8">
        <v-btn
          v-for="item in mainMenuItems"
          :key="item.route"
          :to="item.route"
          variant="text"
          :prepend-icon="item.icon"
          class="mr-2"
        >
          {{ item.title }}
        </v-btn>
      </div>
      
      <v-spacer />
      
      <!-- Acciones de usuario -->
      <div class="d-flex align-center">
        <!-- Búsqueda rápida (desktop) -->
        <v-text-field
          v-if="!isMobile && isAuthenticated"
          v-model="searchQuery"
          density="compact"
          variant="solo"
          hide-details
          single-line
          placeholder="Buscar..."
          class="mr-4 search-field"
          style="max-width: 200px"
          @keyup.enter="performSearch"
        >
          <template v-slot:append-inner>
            <v-icon @click="performSearch">mdi-magnify</v-icon>
          </template>
        </v-text-field>
        
        <!-- Notificaciones -->
        <v-btn
          v-if="isAuthenticated"
          icon
          @click="navigateTo('/notificaciones')"
          class="mr-1"
        >
          <v-badge
            :model-value="unreadNotifications > 0"
            :content="unreadNotifications"
            color="error"
            overlap
          >
            <v-icon>mdi-bell</v-icon>
          </v-badge>
        </v-btn>
        
        <!-- Mensajes -->
        <v-btn
          v-if="isAuthenticated"
          icon
          @click="navigateTo('/mensajes')"
          class="mr-2"
        >
          <v-badge
            :model-value="unreadMessages > 0"
            :content="unreadMessages"
            color="error"
            overlap
          >
            <v-icon>mdi-message</v-icon>
          </v-badge>
        </v-btn>
        
        <!-- Menú de usuario o botones de auth -->
        <div v-if="isAuthenticated">
          <v-menu
            v-model="userMenu"
            :close-on-content-click="false"
            location="bottom"
            min-width="250"
          >
            <template v-slot:activator="{ props }">
              <v-btn
                icon
                v-bind="props"
              >
                <v-avatar 
                  size="36" 
                  :color="getUserAvatarColor()"
                >
                  <span v-if="!userAvatar" class="text-h6">
                    {{ getUserInitials() }}
                  </span>
                  <v-img v-else :src="userAvatar" />
                </v-avatar>
              </v-btn>
            </template>
            
            <v-card>
              <v-list>
                <v-list-item class="px-4 py-3">
                  <div class="d-flex align-center">
                    <v-avatar 
                      size="48" 
                      :color="getUserAvatarColor()"
                      class="mr-3"
                    >
                      <span v-if="!userAvatar" class="text-h6">
                        {{ getUserInitials() }}
                      </span>
                      <v-img v-else :src="userAvatar" />
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold">
                        {{ user?.nombre || user?.email?.split('@')[0] || 'Usuario' }}
                      </div>
                      <div class="text-caption text-grey">
                        {{ getUserTypeLabel() }}
                      </div>
                      <div class="text-caption text-grey">
                        {{ user?.email }}
                      </div>
                    </div>
                  </div>
                </v-list-item>
                
                <v-divider />
                
                <v-list-item
                  v-for="item in userMenuItems"
                  :key="item.route || item.title"
                  :to="item.route"
                  @click="handleMenuItemClick(item)"
                  :prepend-icon="item.icon"
                >
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card>
          </v-menu>
        </div>
        
        <div v-else class="d-flex gap-2">
          <v-btn
            variant="outlined"
            @click="navigateTo('/login')"
            size="small"
            class="hidden-xs"
          >
            Iniciar Sesión
          </v-btn>
          <v-btn
            color="secondary"
            @click="navigateTo('/register')"
            size="small"
          >
            <span class="hidden-xs">Registro</span>
            <v-icon class="hidden-sm-and-up">mdi-account-plus</v-icon>
          </v-btn>
        </div>
      </div>
    </v-app-bar>
    
    <!-- Navigation Drawer para móvil -->
    <v-navigation-drawer 
      v-if="!hideNavigation && isMobile"
      v-model="drawer" 
      temporary
      width="280"
    >
      <v-list>
        <!-- Header del usuario en drawer -->
        <v-list-item
          v-if="isAuthenticated"
          class="px-4 py-3 bg-primary"
        >
          <div class="d-flex align-center">
            <v-avatar 
              size="56"
              :color="getUserAvatarColor()"
              class="mr-3"
            >
              <span v-if="!userAvatar" class="text-h5">
                {{ getUserInitials() }}
              </span>
              <v-img v-else :src="userAvatar" />
            </v-avatar>
            <div>
              <div class="font-weight-bold text-white">
                {{ user?.nombre || user?.email?.split('@')[0] || 'Usuario' }}
              </div>
              <div class="text-caption" style="opacity: 0.8">
                {{ getUserTypeLabel() }}
              </div>
            </div>
          </div>
        </v-list-item>
        
        <!-- Búsqueda en móvil -->
        <v-list-item v-if="isAuthenticated" class="pa-3">
          <v-text-field
            v-model="searchQuery"
            density="compact"
            variant="outlined"
            hide-details
            placeholder="Buscar..."
            @keyup.enter="performSearch"
          >
            <template v-slot:append-inner>
              <v-icon @click="performSearch">mdi-magnify</v-icon>
            </template>
          </v-text-field>
        </v-list-item>
        
        <v-divider v-if="isAuthenticated" />
        
        <!-- Items del menú -->
        <v-list-item
          v-for="item in allMenuItems"
          :key="item.route || item.title"
          :to="item.route"
          @click="handleMenuItemClick(item)"
          :prepend-icon="item.icon"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
          
          <!-- Badges para notificaciones y mensajes -->
          <template v-slot:append>
            <v-badge
              v-if="item.route === '/notificaciones' && unreadNotifications > 0"
              :content="unreadNotifications"
              color="error"
              inline
            />
            <v-badge
              v-if="item.route === '/mensajes' && unreadMessages > 0"
              :content="unreadMessages"
              color="error"
              inline
            />
          </template>
        </v-list-item>
        
        <!-- Botones de auth para móvil si no está autenticado -->
        <div v-if="!isAuthenticated" class="pa-4">
          <v-btn
            color="primary"
            block
            @click="navigateTo('/login')"
            class="mb-2"
          >
            Iniciar Sesión
          </v-btn>
          <v-btn
            color="secondary"
            variant="outlined"
            block
            @click="navigateTo('/register')"
          >
            Registro
          </v-btn>
        </div>
      </v-list>
    </v-navigation-drawer>
    
    <!-- Contenido principal -->
    <v-main>
      <!-- Barra de progreso para carga -->
      <v-progress-linear
        v-if="loading"
        indeterminate
        color="primary"
        class="position-absolute"
        style="z-index: 999"
      />
      
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>
    
    <!-- Footer simplificado -->
    <v-footer 
      v-if="!hideNavigation" 
      app 
      color="primary" 
      class="text-white"
    >
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" class="text-center">
            <div class="mb-2">
              <v-icon size="24" class="mr-2">mdi-briefcase</v-icon>
              <span class="font-weight-medium">Plataforma de Empleo</span>
            </div>
            <div class="text-caption">
              © {{ new Date().getFullYear() }} - Todos los derechos reservados
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
    
    <!-- Snackbar para notificaciones -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="top right"
      multi-line
    >
      <div class="d-flex align-center">
        <v-icon v-if="snackbar.icon" class="mr-2">
          {{ snackbar.icon }}
        </v-icon>
        {{ snackbar.message }}
      </div>
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Dialog de confirmación global -->
    <v-dialog
      v-model="confirmDialog.show"
      max-width="400"
      persistent
    >
      <v-card>
        <v-card-title class="text-h6">
          {{ confirmDialog.title }}
        </v-card-title>
        <v-card-text>
          {{ confirmDialog.message }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            text
            @click="confirmDialog.show = false; confirmDialog.reject()"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            @click="confirmDialog.show = false; confirmDialog.resolve()"
          >
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, provide } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import api from '/src/api/api'

const route = useRoute()
const router = useRouter()
const { mobile } = useDisplay()

// Estados reactivos
const drawer = ref(false)
const userMenu = ref(false)
const user = ref(null)
const userAvatar = ref(null)
const unreadNotifications = ref(0)
const unreadMessages = ref(0)
const searchQuery = ref('')
const loading = ref(false)

// Intervalos para actualización
let notificationInterval = null
let messageInterval = null

// Snackbar para notificaciones
const snackbar = ref({
  show: false,
  message: '',
  color: 'success',
  timeout: 4000,
  icon: null
})

// Dialog de confirmación
const confirmDialog = ref({
  show: false,
  title: '',
  message: '',
  resolve: () => {},
  reject: () => {}
})

// Computadas
const isMobile = computed(() => mobile.value)
const hideNavigation = computed(() => route.meta?.hideNavigation || false)
const isAuthenticated = computed(() => {
  const token = localStorage.getItem('token')
  const userData = localStorage.getItem('user')
  return !!(token && userData)
})

// Menús de navegación
const mainMenuItems = computed(() => [
  { title: 'Ofertas', route: '/ofertas', icon: 'mdi-briefcase' },
  { title: 'Empresas', route: '/empresas', icon: 'mdi-domain' },
  { title: 'Postulantes', route: '/postulantes', icon: 'mdi-account-group' },
  { title: 'Curriculum', route: '/curriculum', icon: 'mdi-file-document' }
])

const userMenuItems = computed(() => {
  const baseItems = [
    { title: 'Mi Perfil', route: '/mi-perfil', icon: 'mdi-account' },
    { title: 'Configuración', route: '/configuracion', icon: 'mdi-cog' }
  ]
  
  const userType = user.value?.user_type || user.value?.rol
  
  if (userType === 'postulante' || userType === 'usuario') {
    baseItems.unshift(
      { title: 'Mi Currículum', route: '/curriculum', icon: 'mdi-file-document' },
      { title: 'Mis Postulaciones', route: '/mis-postulaciones', icon: 'mdi-file-send' }
    )
  }
  
  if (userType === 'empresa' || userType === 'admin') {
    baseItems.unshift(
      { title: 'Mis Ofertas', route: '/mis-ofertas', icon: 'mdi-briefcase-plus' },
      { title: 'Dashboard', route: '/dashboard', icon: 'mdi-view-dashboard' }
    )
  }
  
  baseItems.push(
    { title: 'divider' },
    { title: 'Cerrar Sesión', action: logout, icon: 'mdi-logout', color: 'error' }
  )
  
  return baseItems
})

const allMenuItems = computed(() => {
  if (!isAuthenticated.value) {
    return mainMenuItems.value
  }
  
  const items = [
    ...mainMenuItems.value,
    { title: 'divider' },
    { title: 'Notificaciones', route: '/notificaciones', icon: 'mdi-bell' },
    { title: 'Mensajes', route: '/mensajes', icon: 'mdi-message' },
    { title: 'divider' }
  ]
  
  // Filtrar items del menú de usuario, excluyendo dividers
  const userItems = userMenuItems.value.filter(item => item.title !== 'divider')
  items.push(...userItems)
  
  return items
})

// Métodos auxiliares
const getUserInitials = () => {
  const name = user.value?.nombre || user.value?.email || 'U'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getUserAvatarColor = () => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning']
  const name = user.value?.nombre || user.value?.email || ''
  const index = name.charCodeAt(0) % colors.length
  return colors[index]
}

const getUserTypeLabel = () => {
  const type = user.value?.user_type || user.value?.rol
  const labels = {
    'postulante': 'Postulante',
    'empresa': 'Empresa',
    'admin': 'Administrador',
    'usuario': 'Usuario'
  }
  return labels[type] || 'Usuario'
}

// Métodos principales
const loadUser = () => {
  const userData = localStorage.getItem('user')
  if (userData) {
    try {
      user.value = JSON.parse(userData)
      // Cargar avatar si existe
      if (user.value?.avatar_url) {
        userAvatar.value = user.value.avatar_url
      }
    } catch (error) {
      console.error('Error parsing user data:', error)
      localStorage.removeItem('user')
    }
  }
}

const logout = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    if (token) {
      await api.addTokenToBlacklist(token)
    }
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
  } finally {
    // Limpiar datos locales
    api.logout()
    user.value = null
    userAvatar.value = null
    unreadNotifications.value = 0
    unreadMessages.value = 0
    
    // Limpiar intervalos
    clearIntervals()
    
    loading.value = false
    showSnackbar('Sesión cerrada correctamente', 'info', 'mdi-logout')
    router.push('/login')
  }
}

const loadNotifications = async () => {
  if (!isAuthenticated.value || !user.value?.id) return
  
  try {
    const response = await api.getNotificacionesByUsuario(user.value.id, false)
    unreadNotifications.value = response.data.length
  } catch (error) {
    console.error('Error cargando notificaciones:', error)
  }
}

const loadMessages = async () => {
  if (!isAuthenticated.value || !user.value?.id) return
  
  try {
    // Aquí deberías tener un endpoint para mensajes no leídos
    // Por ahora simularemos con mensajes recibidos
    const response = await api.getMensajes(null, user.value.id)
    // Filtrar mensajes no leídos
    unreadMessages.value = response.data.filter(m => !m.leido).length
  } catch (error) {
    console.error('Error cargando mensajes:', error)
  }
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/ofertas',
      query: { q: searchQuery.value }
    })
    searchQuery.value = ''
    if (isMobile.value) {
      drawer.value = false
    }
  }
}

const navigateTo = (path) => {
  router.push(path)
  userMenu.value = false
  if (isMobile.value) {
    drawer.value = false
  }
}

const navigateHome = () => {
  router.push('/')
}

const handleMenuItemClick = (item) => {
  if (item.action) {
    item.action()
  }
  userMenu.value = false
  drawer.value = false
}

const showSnackbar = (message, color = 'success', icon = null, timeout = 4000) => {
  snackbar.value = {
    show: true,
    message,
    color,
    icon,
    timeout
  }
}

const showConfirmDialog = (title, message) => {
  return new Promise((resolve, reject) => {
    confirmDialog.value = {
      show: true,
      title,
      message,
      resolve,
      reject
    }
  })
}

const clearIntervals = () => {
  if (notificationInterval) {
    clearInterval(notificationInterval)
    notificationInterval = null
  }
  if (messageInterval) {
    clearInterval(messageInterval)
    messageInterval = null
  }
}

const setupIntervals = () => {
  // Actualizar notificaciones cada 30 segundos
  notificationInterval = setInterval(() => {
    if (isAuthenticated.value) {
      loadNotifications()
    }
  }, 30000)
  
  // Actualizar mensajes cada 45 segundos
  messageInterval = setInterval(() => {
    if (isAuthenticated.value) {
      loadMessages()
    }
  }, 45000)
}

// Watchers
watch(() => route.path, () => {
  // Cerrar drawer en móvil al cambiar de ruta
  if (isMobile.value) {
    drawer.value = false
  }
})

watch(isAuthenticated, (newVal) => {
  if (newVal) {
    loadUser()
    loadNotifications()
    loadMessages()
    setupIntervals()
  } else {
    user.value = null
    userAvatar.value = null
    unreadNotifications.value = 0
    unreadMessages.value = 0
    clearIntervals()
  }
})

// Escuchar eventos de actualización
window.addEventListener('user-updated', () => {
  loadUser()
})

window.addEventListener('notification-received', () => {
  loadNotifications()
})

// Lifecycle
onMounted(() => {
  if (isAuthenticated.value) {
    loadUser()
    loadNotifications()
    loadMessages()
    setupIntervals()
  }
})

onUnmounted(() => {
  clearIntervals()
})

// Proveer métodos globalmente
provide('showSnackbar', showSnackbar)
provide('showConfirmDialog', showConfirmDialog)

// Exponer métodos globalmente para compatibilidad
window.showSnackbar = showSnackbar
window.showConfirmDialog = showConfirmDialog
</script>

<style scoped>
/* Transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Utilidades */
.cursor-pointer {
  cursor: pointer;
}

.gap-2 > * + * {
  margin-left: 8px;
}

/* Header */
.app-header {
  backdrop-filter: blur(10px);
  background-color: rgba(var(--v-theme-primary), 0.95) !important;
}

.v-toolbar-title {
  font-weight: bold;
  font-size: 1.25rem;
  user-select: none;
}

/* Búsqueda */
.search-field :deep(.v-field) {
  background-color: rgba(255, 255, 255, 0.1);
}

.search-field :deep(.v-field__input) {
  color: white;
  padding-top: 8px;
  padding-bottom: 8px;
}

.search-field :deep(.v-field__input::placeholder) {
  color: rgba(255, 255, 255, 0.7);
}

.search-field :deep(.v-icon) {
  color: rgba(255, 255, 255, 0.8);
}

/* Navigation drawer */
.v-navigation-drawer {
  background: linear-gradient(to bottom, var(--v-theme-surface), var(--v-theme-background));
}

.bg-primary {
  background-color: rgb(var(--v-theme-primary)) !important;
  color: white;
}

/* Footer */
.v-footer {
  margin-top: auto;
  background: linear-gradient(135deg, var(--v-theme-primary), var(--v-theme-primary-darken-1));
}

/* Badges mejorados */
:deep(.v-badge__badge) {
  font-size: 10px;
  height: 18px;
  min-width: 18px;
  padding: 0 4px;
}

/* Avatar con hover */
.v-avatar {
  transition: transform 0.2s;
}

.v-btn:hover .v-avatar {
  transform: scale(1.1);
}

/* Botones con mejor hover */
.v-btn {
  transition: all 0.3s;
}

/* Progress bar */
.v-progress-linear {
  top: 0;
  left: 0;
  right: 0;
}

/* Responsive */
@media (max-width: 600px) {
  .v-toolbar-title {
    font-size: 1.1rem;
  }
  
  .search-field {
    max-width: 150px !important;
  }
}
</style>