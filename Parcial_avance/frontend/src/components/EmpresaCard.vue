<template>
  <v-card hover>
    <v-card-title>{{ empresa.nombre }}</v-card-title>
    
    <v-card-text>
      <div class="d-flex align-center mb-2">
        <v-chip color="secondary">{{ empresa.rubro }}</v-chip>
      </div>
      
      <p>{{ empresa.descripcion || 'Sin descripción disponible' }}</p>
    </v-card-text>
    
    <v-card-actions>
      <v-btn color="primary" text @click="$router.push(`/empresas/${empresa.id}`)">Ver Detalles</v-btn>
      <v-btn color="secondary" text @click="$router.push(`/empresas/${empresa.id}/ofertas`)">Ver Ofertas</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  empresa: {
    type: Object,
    required: true
  }
})
</script>