<template>
  <v-app>
    <v-app-bar color="primary" prominent>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      
      <v-toolbar-title>Plataforma de Empleo</v-toolbar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>
    
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <v-list-item
          v-for="(item, i) in menuItems"
          :key="i"
          :value="item"
          :to="item.route"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
    <v-main>
      <router-view />
    </v-main>
    
    <v-footer app color="primary">
      <span class="text-white">Plataforma de Empleo &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const drawer = ref(false)
const menuItems = [
  { title: 'Inicio', route: '/' },
  { title: 'Ofertas Laborales', route: '/ofertas' },
  { title: 'Empresas', route: '/empresas' },
  { title: 'Postulantes', route: '/postulantes' },
]
</script>