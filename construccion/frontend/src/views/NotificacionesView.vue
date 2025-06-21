<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-6">
          <h1 class="text-h4">Notificaciones</h1>
          
          <div class="d-flex gap-2">
            <v-btn
              v-if="unreadCount > 0"
              color="primary"
              @click="markAllAsRead"
              :loading="markingAllRead"
            >
              <v-icon left>mdi-check-all</v-icon>
              Marcar todas como leídas
            </v-btn>
            
            <v-btn
              icon
              @click="loadNotifications"
              :loading="loading"
            >
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </div>
        </div>
      </v-col>
      
      <!-- Filtros -->
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <v-select
                  v-model="filter.tipo"
                  :items="tiposNotificacion"
                  label="Tipo de Notificación"
                  clearable
                  variant="outlined"
                  @update:modelValue="filterNotifications"
                >
                  <template v-slot:prepend-inner>
                    <v-icon>mdi-filter</v-icon>
                  </template>
                </v-select>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-select
                  v-model="filter.estado"
                  :items="estadosNotificacion"
                  label="Estado"
                  clearable
                  variant="outlined"
                  @update:modelValue="filterNotifications"
                >
                  <template v-slot:prepend-inner>
                    <v-icon>mdi-eye</v-icon>
                  </template>
                </v-select>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="filter.buscar"
                  label="Buscar en notificaciones"
                  clearable
                  variant="outlined"
                  @input="filterNotifications"
                >
                  <template v-slot:prepend-inner>
                    <v-icon>mdi-magnify</v-icon>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Lista de Notificaciones -->
      <v-col cols="12">
        <v-card v-if="loading && notifications.length === 0">
          <v-card-text class="text-center py-8">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-4">Cargando notificaciones...</p>
          </v-card-text>
        </v-card>
        
        <div v-else-if="filteredNotifications.length === 0" class="text-center py-8">
          <v-icon size="64" color="grey">mdi-bell-off</v-icon>
          <h3 class="text-h6 mt-4">No hay notificaciones</h3>
          <p class="text-body-2">{{ filter.buscar || filter.tipo || filter.estado ? 'No se encontraron notificaciones con los filtros aplicados' : 'No tienes notificaciones en este momento' }}</p>
        </div>
        
        <v-list v-else class="py-0">
          <template v-for="(notification, index) in paginatedNotifications" :key="notification.id">
            <v-list-item
              :class="{
                'bg-blue-lighten-5': !notification.leida,
                'notification-item': true
              }"
              @click="markAsRead(notification)"
            >
              <template v-slot:prepend>
                <v-avatar :color="getNotificationColor(notification.tipo)" size="40">
                  <v-icon color="white">{{ getNotificationIcon(notification.tipo) }}</v-icon>
                </v-avatar>
              </template>
              
              <v-list-item-title class="font-weight-medium">
                {{ getNotificationTitle(notification) }}
              </v-list-item-title>
              
              <v-list-item-subtitle>
                {{ notification.mensaje }}
              </v-list-item-subtitle>
              
              <template v-slot:append>
                <div class="d-flex flex-column align-end">
                  <span class="text-caption">{{ formatDateTime(notification.fecha_envio) }}</span>
                  
                  <div class="mt-2">
                    <v-chip
                      v-if="!notification.leida"
                      size="x-small"
                      color="primary"
                    >
                      Nueva
                    </v-chip>
                    
                    <v-btn
                      icon
                      size="small"
                      @click.stop="deleteNotification(notification.id, index)"
                      class="ml-2"
                    >
                      <v-icon size="18">mdi-delete</v-icon>
                    </v-btn>
                  </div>
                </div>
              </template>
            </v-list-item>
            
            <v-divider v-if="index < paginatedNotifications.length - 1"></v-divider>
          </template>
        </v-list>
        
        <!-- Paginación -->
        <div v-if="filteredNotifications.length > itemsPerPage" class="d-flex justify-center mt-4">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="7"
            @update:modelValue="updatePage"
          ></v-pagination>
        </div>
      </v-col>
    </v-row>
    
    <!-- Dialog de confirmación para eliminar -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Eliminar Notificación</v-card-title>
        <v-card-text>
          ¿Estás seguro de que quieres eliminar esta notificación?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn color="error" @click="confirmDelete">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '/src/api/api'

// Estados reactivos
const loading = ref(false)
const markingAllRead = ref(false)
const deleteDialog = ref(false)
const notifications = ref([])
const currentPage = ref(1)
const itemsPerPage = ref(10)
const notificationToDelete = ref(null)
const indexToDelete = ref(null)

// Filtros
const filter = ref({
  tipo: null,
  estado: null,
  buscar: ''
})

// Opciones de filtro
const tiposNotificacion = [
  { title: 'Postulación', value: 'postulacion' },
  { title: 'Entrevista', value: 'entrevista' },
  { title: 'Oferta', value: 'oferta' },
  { title: 'Sistema', value: 'sistema' },
  { title: 'Recordatorio', value: 'recordatorio' }
]

const estadosNotificacion = [
  { title: 'No leídas', value: false },
  { title: 'Leídas', value: true }
]

// Obtener