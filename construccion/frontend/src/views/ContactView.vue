<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h3 text-center mb-6">
            Contáctanos
          </v-card-title>
          
          <v-row>
            <!-- Información de contacto -->
            <v-col cols="12" md="6">
              <v-card variant="outlined" class="pa-4 h-100">
                <v-card-title class="text-h5 mb-4">
                  <v-icon color="primary" class="mr-2">mdi-information</v-icon>
                  Información de Contacto
                </v-card-title>
                
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-map-marker</v-icon>
                    </template>
                    <v-list-item-title>Dirección</v-list-item-title>
                    <v-list-item-subtitle>
                      Av. Ejército 123, Cercado<br>
                      Arequipa, Perú
                    </v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-phone</v-icon>
                    </template>
                    <v-list-item-title>Teléfono</v-list-item-title>
                    <v-list-item-subtitle>+51 54 123-4567</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-email</v-icon>
                    </template>
                    <v-list-item-title>Email</v-list-item-title>
                    <v-list-item-subtitle>contacto@plataformaempleo.com</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-clock</v-icon>
                    </template>
                    <v-list-item-title>Horario de Atención</v-list-item-title>
                    <v-list-item-subtitle>
                      Lunes a Viernes: 9:00 AM - 6:00 PM<br>
                      Sábados: 9:00 AM - 1:00 PM
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
                
                <v-divider class="my-4"></v-divider>
                
                <div class="text-h6 mb-3">Síguenos en Redes Sociales</div>
                <div class="d-flex gap-2">
                  <v-btn icon color="primary" variant="outlined">
                    <v-icon>mdi-facebook</v-icon>
                  </v-btn>
                  <v-btn icon color="info" variant="outlined">
                    <v-icon>mdi-twitter</v-icon>
                  </v-btn>
                  <v-btn icon color="blue" variant="outlined">
                    <v-icon>mdi-linkedin</v-icon>
                  </v-btn>
                  <v-btn icon color="red" variant="outlined">
                    <v-icon>mdi-instagram</v-icon>
                  </v-btn>
                </div>
              </v-card>
            </v-col>
            
            <!-- Formulario de contacto -->
            <v-col cols="12" md="6">
              <v-card variant="outlined" class="pa-4">
                <v-card-title class="text-h5 mb-4">
                  <v-icon color="primary" class="mr-2">mdi-message</v-icon>
                  Envíanos un Mensaje
                </v-card-title>
                
                <v-form ref="form" @submit.prevent="sendMessage">
                  <v-text-field
                    v-model="form.nombre"
                    label="Nombre completo"
                    variant="outlined"
                    :rules="[v => !!v || 'El nombre es requerido']"
                    class="mb-3"
                  ></v-text-field>
                  
                  <v-text-field
                    v-model="form.email"
                    label="Correo electrónico"
                    type="email"
                    variant="outlined"
                    :rules="emailRules"
                    class="mb-3"
                  ></v-text-field>
                  
                  <v-text-field
                    v-model="form.telefono"
                    label="Teléfono (opcional)"
                    variant="outlined"
                    class="mb-3"
                  ></v-text-field>
                  
                  <v-select
                    v-model="form.asunto"
                    :items="asuntos"
                    label="Asunto"
                    variant="outlined"
                    :rules="[v => !!v || 'El asunto es requerido']"
                    class="mb-3"
                  ></v-select>
                  
                  <v-textarea
                    v-model="form.mensaje"
                    label="Mensaje"
                    variant="outlined"
                    rows="4"
                    :rules="[v => !!v || 'El mensaje es requerido']"
                    class="mb-3"
                  ></v-textarea>
                  
                  <v-checkbox
                    v-model="form.acepta_terminos"
                    :rules="[v => !!v || 'Debe aceptar los términos']"
                    class="mb-3"
                  >
                    <template v-slot:label>
                      <span class="text-body-2">
                        Acepto los 
                        <router-link to="/terms" class="text-primary">términos y condiciones</router-link>
                        y la 
                        <router-link to="/privacy" class="text-primary">política de privacidad</router-link>
                      </span>
                    </template>
                  </v-checkbox>
                  
                  <v-btn
                    type="submit"
                    color="primary"
                    size="large"
                    block
                    :loading="loading"
                  >
                    <v-icon left>mdi-send</v-icon>
                    Enviar Mensaje
                  </v-btn>
                </v-form>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Snackbar para confirmación -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="4000"
      location="top right"
    >
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

// Estado del formulario
const form = ref({
  nombre: '',
  email: '',
  telefono: '',
  asunto: '',
  mensaje: '',
  acepta_terminos: false
})

const loading = ref(false)
const formRef = ref(null)

// Snackbar para mensajes
const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})

// Opciones de asunto
const asuntos = [
  'Consulta General',
  'Soporte Técnico',
  'Información sobre Servicios',
  'Sugerencias',
  'Reportar un Problema',
  'Oportunidades de Negocio',
  'Otros'
]

// Reglas de validación
const emailRules = [
  v => !!v || 'El email es requerido',
  v => /.+@.+\..+/.test(v) || 'El email debe ser válido'
]

// Método para enviar mensaje
const sendMessage = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return
  
  loading.value = true
  
  try {
    // Simular envío de mensaje
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mostrar mensaje de éxito
    snackbar.value = {
      show: true,
      message: 'Mensaje enviado correctamente. Te contactaremos pronto.',
      color: 'success'
    }
    
    // Limpiar formulario
    form.value = {
      nombre: '',
      email: '',
      telefono: '',
      asunto: '',
      mensaje: '',
      acepta_terminos: false
    }
    
    formRef.value.reset()
    
  } catch (error) {
    snackbar.value = {
      show: true,
      message: 'Error al enviar el mensaje. Inténtalo de nuevo.',
      color: 'error'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.gap-2 > * {
  margin-right: 8px;
}

.gap-2 > *:last-child {
  margin-right: 0;
}
</style>