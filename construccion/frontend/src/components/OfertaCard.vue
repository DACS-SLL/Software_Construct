<template>
  <v-card hover>
    <v-card-title>{{ oferta.titulo }}</v-card-title>
    <v-card-subtitle>{{ oferta.ubicacion }}</v-card-subtitle>
    
    <v-card-text>
      <div class="d-flex align-center mb-2">
        <v-chip color="primary">{{ oferta.estado }}</v-chip>
        <v-spacer></v-spacer>
        <span class="text-caption">{{ formatDate(oferta.fecha_publicacion) }}</span>
      </div>
      
      <p>{{ truncateDescription(oferta.descripcion) }}</p>
    </v-card-text>
    
    <v-card-actions>
      <v-btn color="primary" text @click="$router.push(`/ofertas/${oferta.id}`)">Ver Detalles</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  oferta: {
    type: Object,
    required: true
  }
})

const truncateDescription = (text, maxLength = 100) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}
</script>