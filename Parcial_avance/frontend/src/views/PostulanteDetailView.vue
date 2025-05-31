<template>
  <v-container>
    <v-btn @click="$router.go(-1)" color="secondary" class="mb-4">
      <v-icon left>mdi-arrow-left</v-icon> Volver
    </v-btn>
    
    <v-card v-if="postulante">
      <v-card-title class="text-h4">{{ postulante.nombre_completo }}</v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-list>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-phone</v-icon>
                </template>
                <v-list-item-title>{{ postulante.telefono || 'Sin teléfono' }}</v-list-item-title>
              </v-list-item>
              
              <v-list-item v-if="postulante.fecha_nacimiento">
                <template v-slot:prepend>
                  <v-icon>mdi-cake</v-icon>
                </template>
                <v-list-item-title>{{ formatDate(postulante.fecha_nacimiento) }} ({{ edad }} años)</v-list-item-title>
              </v-list-item>
              
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-email</v-icon>
                </template>
                <v-list-item-title>{{ usuarioEmail }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card outlined>
              <v-card-title>Habilidades</v-card-title>
              <v-card-text>
                <v-chip-group>
                  <v-chip v-for="(habilidad, index) in habilidades" :key="index" color="primary">
                    {{ habilidad }}
                  </v-chip>
                </v-chip-group>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-divider class="my-4"></v-divider>
        
        <h3 class="text-h5 mb-2">Experiencia Laboral</h3>
        <v-timeline v-if="experiencias.length > 0" side="end" align="start">
          <v-timeline-item
            v-for="(exp, index) in experiencias"
            :key="index"
            dot-color="primary"
            size="small"
          >
            <template v-slot:opposite>
              {{ formatDate(exp.fecha_inicio) }} - {{ exp.fecha_fin ? formatDate(exp.fecha_fin) : 'Actual' }}
            </template>
            <v-card>
              <v-card-title>{{ exp.empresa }}</v-card-title>
              <v-card-subtitle>{{ exp.cargo }}</v-card-subtitle>
              <v-card-text>{{ exp.descripcion }}</v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
        
        <v-alert v-else type="info" outlined>
          No se encontró experiencia laboral registrada
        </v-alert>
        
        <h3 class="text-h5 mb-2 mt-6">Educación</h3>
        <v-timeline v-if="educaciones.length > 0" side="end" align="start">
          <v-timeline-item
            v-for="(edu, index) in educaciones"
            :key="index"
            dot-color="secondary"
            size="small"
          >
            <template v-slot:opposite>
              {{ formatDate(edu.fecha_inicio) }} - {{ edu.fecha_fin ? formatDate(edu.fecha_fin) : 'Actual' }}
            </template>
            <v-card>
              <v-card-title>{{ edu.institucion }}</v-card-title>
              <v-card-subtitle>{{ edu.titulo }}</v-card-subtitle>
            </v-card>
          </v-timeline-item>
        </v-timeline>
        
        <v-alert v-else type="info" outlined>
          No se encontró educación registrada
        </v-alert>
      </v-card-text>
      
      <v-card-actions>
        <v-btn color="primary" @click="descargarCurriculum">
          <v-icon left>mdi-download</v-icon> Descargar Curriculum
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <v-progress-circular v-else indeterminate color="primary"></v-progress-circular>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '/src/api/api'

const route = useRoute()
const postulante = ref(null)
const experiencias = ref([])
const educaciones = ref([])
const usuario = ref(null)

const habilidades = ['JavaScript', 'Vue.js', 'HTML', 'CSS', 'SQL', 'Node.js']

onMounted(async () => {
  try {
    const response = await api.getPostulante(route.params.id)
    postulante.value = response.data
    
    experiencias.value = [
      {
        empresa: 'Tech Solutions S.A.',
        cargo: 'Desarrollador Frontend',
        descripcion: 'Desarrollo de aplicaciones web con Vue.js y Vuetify',
        fecha_inicio: '2020-06-01',
        fecha_fin: '2023-12-31'
      },
      {
        empresa: 'Innovatech',
        cargo: 'Practicante Desarrollo Web',
        descripcion: 'Desarrollo de componentes UI y mantenimiento de sitios web',
        fecha_inicio: '2019-01-15',
        fecha_fin: '2020-05-30'
      }
    ]
    
    educaciones.value = [
      {
        institucion: 'Universidad Tecnológica Nacional',
        titulo: 'Ingeniería en Sistemas',
        fecha_inicio: '2018-03-01',
        fecha_fin: '2022-12-15'
      },
      {
        institucion: 'Platzi',
        titulo: 'Curso Avanzado de Vue.js',
        fecha_inicio: '2021-05-01',
        fecha_fin: '2021-08-15'
      }
    ]
    
  } catch (error) {
    console.error('Error al cargar postulante:', error)
  }
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'short' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const edad = computed(() => {
  if (!postulante.value?.fecha_nacimiento) return 'N/A'
  const birthDate = new Date(postulante.value.fecha_nacimiento)
  const today = new Date()
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return age
})

const usuarioEmail = computed(() => {
  return postulante.value?.usuario_id ? `usuario${postulante.value.usuario_id}@ejemplo.com` : 'Sin email'
})

const descargarCurriculum = () => {
  alert('Funcionalidad de descarga de curriculum en desarrollo')
}
</script>