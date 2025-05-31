<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="text-center">
        <h1 class="text-h3 mb-6">Plataforma de Empleo</h1>
        <p class="text-h6">Conectando empresas con talento</p>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4" hover>
          <v-card-title class="text-h5">
            <v-icon large class="mr-2">mdi-briefcase</v-icon>
            Ofertas Laborales
          </v-card-title>
          <v-card-text>
            Explora las últimas oportunidades laborales disponibles
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" to="/ofertas">Ver ofertas</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4" hover>
          <v-card-title class="text-h5">
            <v-icon large class="mr-2">mdi-domain</v-icon>
            Empresas
          </v-card-title>
          <v-card-text>
            Descubre las empresas que están contratando
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" to="/empresas">Ver empresas</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4" hover>
          <v-card-title class="text-h5">
            <v-icon large class="mr-2">mdi-account-group</v-icon>
            Postulantes
          </v-card-title>
          <v-card-text>
            Encuentra talento para tu organización
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" to="/postulantes">Ver postulantes</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <v-divider class="my-8"></v-divider>
    
    <v-row>
      <v-col cols="12">
        <h2 class="text-h4 mb-4">Últimas Ofertas</h2>
        <v-row v-if="loading">
          <v-col v-for="n in 3" :key="n" cols="12" md="4">
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-col>
        </v-row>
        <v-row v-else>
          <v-col v-for="oferta in ofertas" :key="oferta.id" cols="12" md="4">
            <OfertaCard :oferta="oferta" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import OfertaCard from '/src/components/OfertaCard.vue'
import api from '/src/api/api'

const ofertas = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.getOfertas(0, 3)
    ofertas.value = response.data
  } catch (error) {
    console.error('Error al obtener ofertas:', error)
  } finally {
    loading.value = false
  }
})
</script>