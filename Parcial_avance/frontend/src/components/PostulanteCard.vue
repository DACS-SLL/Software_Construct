<template>
  <v-card hover>
    <v-card-title>{{ postulante.nombre_completo }}</v-card-title>
    
    <v-card-text>
      <div class="d-flex align-center mb-2">
        <v-icon class="mr-2">mdi-phone</v-icon>
        <span>{{ postulante.telefono || 'Sin teléfono' }}</span>
      </div>
      
      <div v-if="postulante.fecha_nacimiento" class="d-flex align-center mb-2">
        <v-icon class="mr-2">mdi-cake</v-icon>
        <span>{{ formatDate(postulante.fecha_nacimiento) }}</span>
      </div>
      
      <v-divider class="my-3"></v-divider>
      
      <div>
        <h4 class="text-subtitle-1">Habilidades:</h4>
        <v-chip-group>
          <v-chip v-for="(habilidad, index) in habilidades" :key="index" color="primary" small>
            {{ habilidad }}
          </v-chip>
        </v-chip-group>
      </div>
    </v-card-text>
    
    <v-card-actions>
      <v-btn color="primary" text @click="$router.push(`/postulantes/${postulante.id}`)">Ver Detalles</v-btn>
      <v-btn color="secondary" text @click="verCurriculum">Ver Curriculum</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  postulante: {
    type: Object,
    required: true
  }
})

// Habilidades de ejemplo (en un sistema real, esto vendría de la API)
const habilidades = computed(() => {
  return ['JavaScript', 'Vue.js', 'HTML', 'CSS', 'SQL']
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const verCurriculum = () => {
  // En un sistema real, esto abriría el curriculum del postulante
  alert('Funcionalidad de ver curriculum en desarrollo')
}
</script>