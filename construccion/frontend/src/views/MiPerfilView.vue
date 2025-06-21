<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Mi Perfil</h1>
      </v-col>
      
      <!-- Información del Usuario -->
      <v-col cols="12" md="6">
        <v-card class="elevation-2 mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-account</v-icon>
            Información Personal
            <v-spacer></v-spacer>
            <v-btn icon @click="editMode = !editMode">
              <v-icon>{{ editMode ? 'mdi-check' : 'mdi-pencil' }}</v-icon>
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-form v-if="editMode" @submit.prevent="saveProfile">
              <v-text-field
                v-model="profile.nombre"
                label="Nombre"
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-model="profile.email"
                label="Correo Electrónico"
                type="email"
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-if="userType === 'postulante'"
                v-model="profile.telefono"
                label="Teléfono"
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-if="userType === 'postulante'"
                v-model="profile.fecha_nacimiento"
                label="Fecha de Nacimiento"
                type="date"
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-if="userType === 'empresa'"
                v-model="profile.rubro"
                label="Rubro"
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-if="userType === 'empresa'"
                v-model="profile.direccion"
                label="Dirección"
                variant="outlined"
                class="mb-3"
              ></v-text-field>
              
              <v-textarea
                v-if="userType === 'empresa'"
                v-model="profile.descripcion"
                label="Descripción"
                variant="outlined"
                rows="3"
              ></v-textarea>
            </v-form>
            
            <div v-else>
              <div class="mb-4">
                <h3>{{ profile.nombre || 'Sin nombre' }}</h3>
                <p class="text-body-2 text-grey">{{ profile.email }}</p>
              </div>
              
              <div v-if="userType === 'postulante'">
                <div class="d-flex align-center mb-2">
                  <v-icon class="mr-3">mdi-phone</v-icon>
                  <span>{{ profile.telefono || 'Sin teléfono' }}</span>
                </div>
                <div class="d-flex align-center">
                  <v-icon class="mr-3">mdi-calendar</v-icon>
                  <span>{{ formatDate(profile.fecha_nacimiento) || 'Sin fecha' }}</span>
                </div>
              </div>
              
              <div v-if="userType === 'empresa'">
                <div class="d-flex align-center mb-2">
                  <v-icon class="mr-3">mdi-briefcase</v-icon>
                  <span>{{ profile.rubro || 'Sin rubro' }}</span>
                </div>
                <div class="d-flex align-center mb-2">
                  <v-icon class="mr-3">mdi-map-marker</v-icon>
                  <span>{{ profile.direccion || 'Sin dirección' }}</span>
                </div>
                <div v-if="profile.descripcion">
                  <h4 class="mb-2">Descripción</h4>
                  <p>{{ profile.descripcion }}</p>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Cambio de Contraseña -->
      <v-col cols="12" md="6">
        <v-card class="elevation-2 mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-lock</v-icon>
            Cambiar Contraseña
          </v-card-title>
          
          <v-card-text>
            <v-form ref="passwordForm" @submit.prevent="changePassword">
              <v-text-field
                v-model="passwordData.current"
                label="Contraseña Actual"
                type="password"
                variant="outlined"
                :rules="[v => !!v || 'Campo requerido']"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-model="passwordData.new"
                label="Nueva Contraseña"
                type="password"
                variant="outlined"
                :rules="passwordRules"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-model="passwordData.confirm"
                label="Confirmar Nueva Contraseña"
                type="password"
                variant="outlined"
                :rules="confirmPasswordRules"
                class="mb-3"
              ></v-text-field>
              
              <v-btn
                type="submit"
                color="primary"
                :loading="changingPassword"
                block
              >
                Cambiar Contraseña
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Estadísticas del Usuario -->
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-chart-box</v-icon>
            Estadísticas
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3" v-for="stat in stats" :key="stat.title">
                <v-card class="pa-4 text-center" color="grey-lighten-5">
                  <v-icon size="48" :color="stat.color" class="mb-2">{{ stat.icon }}</v-icon>
                  <h2 class="text-h4 font-weight-bold">{{ stat.value }}</h2>
                  <p class="text-body-2">{{ stat.title }}</p>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Actividad Reciente -->
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-history</v-icon>
            Actividad Reciente
          </v-card-title>
          
          <v-card-text>
            <v-timeline v-if="recentActivity.length > 0" side="end" align="start" density="compact">
              <v-timeline-item
                v-for="(activity, index) in recentActivity"
                :key="index"
                dot-color="primary"
                size="small"
              >
                <template v-slot:opposite>
                  <span class="text-caption">{{ formatDateTime(activity.fecha) }}</span>
                </template>
                <div>
                  <h4>{{ activity.accion }}</h4>
                  <p class="text-body-2">{{ activity.descripcion }}</p>
                </div>
              </v-timeline-item>
            </v-timeline>
            
            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey">mdi-history</v-icon>
              <p class="text-body-1 mt-4">No hay actividad reciente</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '/src/api/api'

// Estados reactivos
const editMode = ref(false)
const changingPassword = ref(false)
const loading = ref(false)

const profile = ref({
  nombre: '',
  email: '',
  telefono: '',
  fecha_nacimiento: '',
  rubro: '',
  direccion: '',
  descripcion: ''
})

const passwordData = ref({
  current: '',
  new: '',
  confirm: ''
})

const stats = ref([])
const recentActivity = ref([])

// Obtener tipo de usuario
const user = JSON.parse(localStorage.getItem('user') || '{}')
const userType = computed(() => user.user_type || user.rol === 'admin' ? 'empresa' : 'postulante')

// Validaciones
const passwordRules = [
  v => !!v || 'La nueva contraseña es requerida',
  v => v.length >= 6 || 'La contraseña debe tener al menos 6 caracteres'
]

const confirmPasswordRules = [
  v => !!v || 'Confirmar contraseña es requerido',
  v => v === passwordData.value.new || 'Las contraseñas no coinciden'
]

// Métodos
const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const formatDateTime = (dateString) => {
  if (!dateString) return ''
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const loadProfile = async () => {
  try {
    loading.value = true
    
    if (userType.value === 'postulante') {
      // Buscar postulante por usuario_id
      const response = await api.getPostulantes()
      const postulante = response.data.find(p => p.usuario_id === user.id)
      
      if (postulante) {
        profile.value = {
          nombre: postulante.nombre_completo,
          email: user.email,
          telefono: postulante.telefono,
          fecha_nacimiento: postulante.fecha_nacimiento
        }
      }
    } else {
      // Buscar empresa por usuario_id
      const response = await api.getEmpresas()
      const empresa = response.data.find(e => e.usuario_id === user.id)
      
      if (empresa) {
        profile.value = {
          nombre: empresa.nombre,
          email: user.email,
          rubro: empresa.rubro,
          direccion: empresa.direccion,
          descripcion: empresa.descripcion
        }
      }
    }
  } catch (error) {
    console.error('Error cargando perfil:', error)
  } finally {
    loading.value = false
  }
}

const saveProfile = async () => {
  try {
    loading.value = true
    
    if (userType.value === 'postulante') {
      const response = await api.getPostulantes()
      const postulante = response.data.find(p => p.usuario_id === user.id)
      
      if (postulante) {
        await api.updatePostulante(postulante.id, {
          nombre_completo: profile.value.nombre,
          telefono: profile.value.telefono,
          fecha_nacimiento: profile.value.fecha_nacimiento,
          usuario_id: user.id
        })
      }
    } else {
      const response = await api.getEmpresas()
      const empresa = response.data.find(e => e.usuario_id === user.id)
      
      if (empresa) {
        await api.updateEmpresa(empresa.id, {
          nombre: profile.value.nombre,
          rubro: profile.value.rubro,
          direccion: profile.value.direccion,
          descripcion: profile.value.descripcion,
          usuario_id: user.id
        })
      }
    }
    
    editMode.value = false
    window.showSnackbar('Perfil actualizado correctamente')
  } catch (error) {
    console.error('Error guardando perfil:', error)
    window.showSnackbar('Error al actualizar perfil', 'error')
  } finally {
    loading.value = false
  }
}

const changePassword = async () => {
  try {
    changingPassword.value = true
    // En un sistema real, aquí harías la llamada para cambiar la contraseña
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simular delay
    
    passwordData.value = {
      current: '',
      new: '',
      confirm: ''
    }
    
    window.showSnackbar('Contraseña cambiada correctamente')
  } catch (error) {
    console.error('Error cambiando contraseña:', error)
    window.showSnackbar('Error al cambiar contraseña', 'error')
  } finally {
    changingPassword.value = false
  }
}

const loadStats = async () => {
  try {
    if (userType.value === 'postulante') {
      const postulantesResponse = await api.getPostulantes()
      const postulante = postulantesResponse.data.find(p => p.usuario_id === user.id)
      
      if (postulante) {
        const postulacionesResponse = await api.getPostulacionesByPostulante(postulante.id)
        const postulaciones = postulacionesResponse.data
        
        stats.value = [
          {
            title: 'Postulaciones',
            value: postulaciones.length,
            icon: 'mdi-file-send',
            color: 'primary'
          },
          {
            title: 'Pendientes',
            value: postulaciones.filter(p => p.estado === 'pendiente').length,
            icon: 'mdi-clock',
            color: 'warning'
          },
          {
            title: 'Entrevistas',
            value: postulaciones.filter(p => p.estado === 'entrevista').length,
            icon: 'mdi-account-voice',
            color: 'info'
          },
          {
            title: 'Aceptadas',
            value: postulaciones.filter(p => p.estado === 'aceptada').length,
            icon: 'mdi-check-circle',
            color: 'success'
          }
        ]
      }
    } else {
      const empresasResponse = await api.getEmpresas()
      const empresa = empresasResponse.data.find(e => e.usuario_id === user.id)
      
      if (empresa) {
        const ofertasResponse = await api.getOfertasByEmpresa(empresa.id)
        const ofertas = ofertasResponse.data
        
        let totalPostulaciones = 0
        for (const oferta of ofertas) {
          const postulantesResponse = await api.getPostulantesByOferta(oferta.id)
          totalPostulaciones += postulantesResponse.data.length
        }
        
        stats.value = [
          {
            title: 'Ofertas Publicadas',
            value: ofertas.length,
            icon: 'mdi-briefcase',
            color: 'primary'
          },
          {
            title: 'Ofertas Activas',
            value: ofertas.filter(o => o.estado === 'activa').length,
            icon: 'mdi-briefcase-check',
            color: 'success'
          },
          {
            title: 'Total Postulaciones',
            value: totalPostulaciones,
            icon: 'mdi-account-group',
            color: 'info'
          },
          {
            title: 'Ofertas Cerradas',
            value: ofertas.filter(o => o.estado === 'cerrada').length,
            icon: 'mdi-briefcase-remove',
            color: 'error'
          }
        ]
      }
    }
  } catch (error) {
    console.error('Error cargando estadísticas:', error)
    stats.value = []
  }
}

const loadRecentActivity = () => {
  // Simular actividad reciente
  recentActivity.value = [
    {
      accion: 'Perfil actualizado',
      descripcion: 'Información personal modificada',
      fecha: new Date().toISOString()
    },
    {
      accion: userType.value === 'postulante' ? 'Nueva postulación' : 'Nueva oferta publicada',
      descripcion: userType.value === 'postulante' ? 'Postulación enviada para Desarrollador Full Stack' : 'Oferta "Desarrollador Frontend" publicada',
      fecha: new Date(Date.now() - 86400000).toISOString() // Ayer
    },
    {
      accion: 'Sesión iniciada',
      descripcion: 'Acceso desde navegador web',
      fecha: new Date(Date.now() - 172800000).toISOString() // Hace 2 días
    }
  ]
}

// Lifecycle
onMounted(() => {
  loadProfile()
  loadStats()
  loadRecentActivity()
})
</script>

<style scoped>
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>