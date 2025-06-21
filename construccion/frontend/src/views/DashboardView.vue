<template>
  <v-container fluid class="pa-6">
    <!-- Header con estadísticas principales -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h3 font-weight-bold text-primary">Dashboard</h1>
            <p class="text-h6 text-grey-darken-1">
              Bienvenido {{ userInfo?.nombre }}, aquí tienes el resumen de tu actividad
            </p>
          </div>
          
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn
                color="primary"
                v-bind="props"
                prepend-icon="mdi-calendar"
                variant="outlined"
              >
                {{ selectedPeriod }}
              </v-btn>
            </template>
            
            <v-list>
              <v-list-item
                v-for="period in periods"
                :key="period.value"
                @click="selectedPeriod = period.text"
              >
                <v-list-item-title>{{ period.text }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </v-col>
    </v-row>

    <!-- Cards de estadísticas principales -->
    <v-row class="mb-6">
      <v-col
        v-for="(stat, index) in mainStats"
        :key="index"
        cols="12"
        sm="6"
        md="3"
      >
        <v-card
          class="pa-4 dashboard-card"
          :color="stat.color + '-lighten-5'"
          hover
          @click="navigateToDetail(stat.route)"
        >
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-h3 font-weight-bold" :class="stat.color + '--text'">
                {{ stat.value }}
              </div>
              <div class="text-subtitle-1 text-grey-darken-1">
                {{ stat.title }}
              </div>
              <div class="d-flex align-center mt-2">
                <v-icon
                  size="16"
                  :color="stat.trend > 0 ? 'success' : 'error'"
                  class="mr-1"
                >
                  {{ stat.trend > 0 ? 'mdi-trending-up' : 'mdi-trending-down' }}
                </v-icon>
                <span
                  class="text-caption"
                  :class="stat.trend > 0 ? 'text-success' : 'text-error'"
                >
                  {{ Math.abs(stat.trend) }}% vs mes anterior
                </span>
              </div>
            </div>
            
            <v-avatar
              size="60"
              :color="stat.color"
              class="elevation-2"
            >
              <v-icon size="30" color="white">{{ stat.icon }}</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Gráficos y análisis -->
    <v-row class="mb-6">
      <!-- Gráfico de actividad semanal -->
      <v-col cols="12" md="8">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-3">mdi-chart-line</v-icon>
            Actividad Semanal
            <v-spacer></v-spacer>
            <v-btn-toggle v-model="chartType" mandatory>
              <v-btn value="ofertas" size="small">Ofertas</v-btn>
              <v-btn value="postulaciones" size="small">Postulaciones</v-btn>
            </v-btn-toggle>
          </v-card-title>
          
          <div class="chart-container">
            <canvas ref="weeklyChart" height="300"></canvas>
          </div>
        </v-card>
      </v-col>
      
      <!-- Distribución por categorías -->
      <v-col cols="12" md="4">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="secondary" class="mr-3">mdi-chart-donut</v-icon>
            Distribución por Categorías
          </v-card-title>
          
          <div class="chart-container">
            <canvas ref="categoryChart" height="300"></canvas>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Actividad reciente y notificaciones -->
    <v-row class="mb-6">
      <!-- Actividad reciente -->
      <v-col cols="12" md="6">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="info" class="mr-3">mdi-clock-outline</v-icon>
            Actividad Reciente
            <v-spacer></v-spacer>
            <v-btn
              icon
              size="small"
              @click="refreshActivity"
              :loading="loadingActivity"
            >
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-title>
          
          <v-list class="py-0">
            <template v-for="(activity, index) in recentActivity" :key="index">
              <v-list-item class="px-0">
                <template v-slot:prepend>
                  <v-avatar
                    size="32"
                    :color="getActivityColor(activity.type)"
                  >
                    <v-icon size="16" color="white">
                      {{ getActivityIcon(activity.type) }}
                    </v-icon>
                  </v-avatar>
                </template>
                
                <v-list-item-title class="text-body-2">
                  {{ activity.description }}
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  {{ formatDateTime(activity.timestamp) }}
                </v-list-item-subtitle>
              </v-list-item>
              
              <v-divider v-if="index < recentActivity.length - 1"></v-divider>
            </template>
          </v-list>
          
          <div v-if="recentActivity.length === 0" class="text-center py-8">
            <v-icon size="48" color="grey">mdi-history</v-icon>
            <p class="text-body-2 mt-2">No hay actividad reciente</p>
          </div>
        </v-card>
      </v-col>
      
      <!-- Notificaciones importantes -->
      <v-col cols="12" md="6">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="warning" class="mr-3">mdi-bell</v-icon>
            Notificaciones Importantes
            <v-spacer></v-spacer>
            <v-chip size="small" color="error" v-if="urgentNotifications > 0">
              {{ urgentNotifications }}
            </v-chip>
          </v-card-title>
          
          <v-list class="py-0">
            <template v-for="(notification, index) in importantNotifications" :key="index">
              <v-list-item
                class="px-0"
                @click="handleNotificationClick(notification)"
              >
                <template v-slot:prepend>
                  <v-icon
                    :color="notification.priority === 'high' ? 'error' : 'warning'"
                    size="20"
                  >
                    {{ notification.priority === 'high' ? 'mdi-alert-circle' : 'mdi-information' }}
                  </v-icon>
                </template>
                
                <v-list-item-title class="text-body-2">
                  {{ notification.title }}
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  {{ notification.message }}
                </v-list-item-subtitle>
                
                <template v-slot:append>
                  <v-btn
                    icon
                    size="small"
                    @click.stop="dismissNotification(index)"
                  >
                    <v-icon size="16">mdi-close</v-icon>
                  </v-btn>
                </template>
              </v-list-item>
              
              <v-divider v-if="index < importantNotifications.length - 1"></v-divider>
            </template>
          </v-list>
          
          <div v-if="importantNotifications.length === 0" class="text-center py-8">
            <v-icon size="48" color="success">mdi-check-circle</v-icon>
            <p class="text-body-2 mt-2">¡Todo al día!</p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Acciones rápidas -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="success" class="mr-3">mdi-flash</v-icon>
            Acciones Rápidas
          </v-card-title>
          
          <v-row>
            <v-col
              v-for="(action, index) in quickActions"
              :key="index"
              cols="12"
              sm="6"
              md="3"
            >
              <v-card
                class="pa-4 text-center quick-action-card"
                variant="outlined"
                hover
                @click="executeQuickAction(action)"
              >
                <v-avatar
                  size="48"
                  :color="action.color"
                  class="mb-3"
                >
                  <v-icon color="white">{{ action.icon }}</v-icon>
                </v-avatar>
                
                <h4 class="text-subtitle-1">{{ action.title }}</h4>
                <p class="text-body-2 text-grey">{{ action.description }}</p>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabla de elementos recientes -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-3">mdi-table</v-icon>
            Elementos Recientes
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Buscar..."
              variant="outlined"
              hide-details
              density="compact"
              style="max-width: 300px;"
            ></v-text-field>
          </v-card-title>
          
          <v-data-table
            :headers="tableHeaders"
            :items="filteredItems"
            :search="search"
            :loading="loadingTable"
            item-value="id"
            class="elevation-0"
          >
            <template v-slot:item.status="{ item }">
              <v-chip
                :color="getStatusColor(item.status)"
                size="small"
                variant="elevated"
              >
                {{ item.status }}
              </v-chip>
            </template>
            
            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                size="small"
                @click="viewItem(item)"
              >
                <v-icon>mdi-eye</v-icon>
              </v-btn>
              
              <v-btn
                icon
                size="small"
                @click="editItem(item)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estados reactivos
const selectedPeriod = ref('Últimos 7 días')
const chartType = ref('ofertas')
const search = ref('')
const loadingActivity = ref(false)
const loadingTable = ref(false)
const urgentNotifications = ref(2)

// Datos del usuario
const userInfo = ref({
  nombre: 'Daniel Casas',
  tipo: 'Empresa',
  avatar: null
})

// Períodos disponibles
const periods = [
  { text: 'Hoy', value: 'today' },
  { text: 'Últimos 7 días', value: '7days' },
  { text: 'Últimos 30 días', value: '30days' },
  { text: 'Este mes', value: 'month' },
  { text: 'Este año', value: 'year' }
]

// Estadísticas principales
const mainStats = ref([
  {
    title: 'Ofertas Activas',
    value: '24',
    icon: 'mdi-briefcase',
    color: 'primary',
    trend: 12,
    route: '/mis-ofertas'
  },
  {
    title: 'Postulaciones',
    value: '156',
    icon: 'mdi-account-group',
    color: 'success',
    trend: 8,
    route: '/postulaciones'
  },
  {
    title: 'Entrevistas',
    value: '18',
    icon: 'mdi-calendar-clock',
    color: 'warning',
    trend: -3,
    route: '/entrevistas'
  },
  {
    title: 'Contrataciones',
    value: '7',
    icon: 'mdi-check-circle',
    color: 'info',
    trend: 15,
    route: '/contrataciones'
  }
])

// Actividad reciente
const recentActivity = ref([
  {
    type: 'application',
    description: 'Nueva postulación para Desarrollador Frontend',
    timestamp: new Date(Date.now() - 3600000)
  },
  {
    type: 'interview',
    description: 'Entrevista programada con Juan Pérez',
    timestamp: new Date(Date.now() - 7200000)
  },
  {
    type: 'offer',
    description: 'Oferta "Backend Developer" publicada',
    timestamp: new Date(Date.now() - 10800000)
  },
  {
    type: 'hire',
    description: 'Ana García contratada como UX Designer',
    timestamp: new Date(Date.now() - 14400000)
  }
])

// Notificaciones importantes
const importantNotifications = ref([
  {
    title: 'Entrevista pendiente',
    message: 'Tienes una entrevista programada para mañana a las 14:00',
    priority: 'high',
    action: '/entrevistas'
  },
  {
    title: 'Oferta por expirar',
    message: 'La oferta "Desarrollador Full Stack" expira en 3 días',
    priority: 'medium',
    action: '/mis-ofertas'
  }
])

// Acciones rápidas
const quickActions = ref([
  {
    title: 'Nueva Oferta',
    description: 'Publicar una nueva oferta de trabajo',
    icon: 'mdi-plus-circle',
    color: 'primary',
    action: 'new-offer'
  },
  {
    title: 'Ver Postulaciones',
    description: 'Revisar postulaciones recientes',
    icon: 'mdi-file-document-multiple',
    color: 'success',
    action: 'view-applications'
  },
  {
    title: 'Programar Entrevista',
    description: 'Agendar nueva entrevista',
    icon: 'mdi-calendar-plus',
    color: 'warning',
    action: 'schedule-interview'
  },
  {
    title: 'Generar Reporte',
    description: 'Crear reporte de actividad',
    icon: 'mdi-chart-bar',
    color: 'info',
    action: 'generate-report'
  }
])

// Headers de la tabla
const tableHeaders = ref([
  { title: 'Título', value: 'title', sortable: true },
  { title: 'Tipo', value: 'type', sortable: true },
  { title: 'Estado', value: 'status', sortable: true },
  { title: 'Fecha', value: 'date', sortable: true },
  { title: 'Acciones', value: 'actions', sortable: false }
])

// Elementos de la tabla
const tableItems = ref([
  {
    id: 1,
    title: 'Desarrollador Frontend React',
    type: 'Oferta',
    status: 'Activa',
    date: '2025-06-20',
    applicants: 12
  },
  {
    id: 2,
    title: 'Postulación de María González',
    type: 'Postulación',
    status: 'Pendiente',
    date: '2025-06-19',
    position: 'Backend Developer'
  },
  {
    id: 3,
    title: 'Entrevista con Carlos López',
    type: 'Entrevista',
    status: 'Programada',
    date: '2025-06-22',
    time: '15:00'
  }
])

// Computadas
const filteredItems = computed(() => {
  if (!search.value) return tableItems.value
  
  return tableItems.value.filter(item =>
    item.title.toLowerCase().includes(search.value.toLowerCase()) ||
    item.type.toLowerCase().includes(search.value.toLowerCase()) ||
    item.status.toLowerCase().includes(search.value.toLowerCase())
  )
})

// Referencias para los gráficos
const weeklyChart = ref(null)
const categoryChart = ref(null)

// Métodos
const navigateToDetail = (route) => {
  if (route) {
    router.push(route)
  }
}

const refreshActivity = async () => {
  loadingActivity.value = true
  // Simular carga de datos
  await new Promise(resolve => setTimeout(resolve, 1000))
  loadingActivity.value = false
}

const handleNotificationClick = (notification) => {
  if (notification.action) {
    router.push(notification.action)
  }
}

const dismissNotification = (index) => {
  importantNotifications.value.splice(index, 1)
  urgentNotifications.value = Math.max(0, urgentNotifications.value - 1)
}

const executeQuickAction = (action) => {
  switch (action.action) {
    case 'new-offer':
      router.push('/ofertas/nueva')
      break
    case 'view-applications':
      router.push('/postulaciones')
      break
    case 'schedule-interview':
      router.push('/entrevistas/nueva')
      break
    case 'generate-report':
      // Simular generación de reporte
      window.showSnackbar('Generando reporte...', 'info')
      break
  }
}

const getActivityColor = (type) => {
  const colors = {
    application: 'primary',
    interview: 'warning',
    offer: 'success',
    hire: 'info'
  }
  return colors[type] || 'grey'
}

const getActivityIcon = (type) => {
  const icons = {
    application: 'mdi-file-send',
    interview: 'mdi-account-voice',
    offer: 'mdi-briefcase-plus',
    hire: 'mdi-handshake'
  }
  return icons[type] || 'mdi-circle'
}

const getStatusColor = (status) => {
  const colors = {
    'Activa': 'success',
    'Pendiente': 'warning',
    'Programada': 'info',
    'Cerrada': 'error',
    'Completada': 'success'
  }
  return colors[status] || 'grey'
}

const formatDateTime = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const viewItem = (item) => {
  window.showSnackbar(`Viendo detalles de: ${item.title}`, 'info')
}

const editItem = (item) => {
  window.showSnackbar(`Editando: ${item.title}`, 'info')
}

// Inicializar gráficos (simulado)
const initCharts = async () => {
  await nextTick()
  
  // Aquí inicializarías Chart.js o cualquier otra librería de gráficos
  console.log('Inicializando gráficos...')
  
  // Ejemplo de configuración de Chart.js (comentado porque no está importado)
  /*
  if (weeklyChart.value) {
    new Chart(weeklyChart.value, {
      type: 'line',
      data: {
        labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        datasets: [{
          label: 'Ofertas',
          data: [3, 7, 4, 8, 6, 9, 5],
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      }
    })
  }
  */
}

// Watchers
watch(chartType, () => {
  // Actualizar gráfico cuando cambie el tipo
  console.log(`Actualizando gráfico a: ${chartType.value}`)
})

// Lifecycle
onMounted(() => {
  initCharts()
  
  // Simular carga inicial de datos
  setTimeout(() => {
    loadingTable.value = false
  }, 1000)
})
</script>

<style scoped>
.dashboard-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.quick-action-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.quick-action-card:hover {
  transform: translateY(-2px);
  border-color: rgb(var(--v-theme-primary)) !important;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

.chart-container canvas {
  max-height: 100%;
  width: 100% !important;
}

/* Animaciones para las cards */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.v-card {
  animation: fadeInUp 0.6s ease-out;
}

/* Efectos de hover mejorados */
.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
  transition: background-color 0.2s ease;
}

/* Responsive improvements */
@media (max-width: 960px) {
  .text-h3 {
    font-size: 1.8rem !important;
  }
  
  .pa-6 {
    padding: 16px !important;
  }
}

/* Dark mode support */
.v-theme--dark .dashboard-card {
  border: 1px solid rgba(255,255,255,0.1);
}

.v-theme--dark .quick-action-card:hover {
  border-color: rgb(var(--v-theme-primary)) !important;
  background-color: rgba(var(--v-theme-primary), 0.1);
}

/* Scrollbar personalizado */
.v-list::-webkit-scrollbar {
  width: 4px;
}

.v-list::-webkit-scrollbar-track {
  background: transparent;
}

.v-list::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.3);
  border-radius: 4px;
}

.v-list::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.5);
}
</style>