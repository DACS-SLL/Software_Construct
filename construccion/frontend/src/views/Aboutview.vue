<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6">
          <v-card-title class="text-h3 text-center mb-6">
            Acerca de Nosotros
          </v-card-title>
          
          <v-card-text>
            <div class="text-h5 mb-4">Nuestra Misión</div>
            <p class="text-body-1 mb-6">
              En Plataforma de Empleo, nos dedicamos a conectar a los mejores talentos 
              con las empresas que buscan crecer. Creemos que cada persona merece encontrar 
              el trabajo perfecto que no solo cubra sus necesidades económicas, sino que 
              también le permita desarrollarse profesional y personalmente.
            </p>
            
            <div class="text-h5 mb-4">Nuestra Visión</div>
            <p class="text-body-1 mb-6">
              Ser la plataforma líder en el mercado laboral, facilitando conexiones 
              significativas entre empleadores y candidatos, promoviendo el crecimiento 
              profesional y contribuyendo al desarrollo económico de nuestra región.
            </p>
            
            <div class="text-h5 mb-4">Nuestros Valores</div>
            <v-row>
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4 mb-4">
                  <v-card-title class="text-h6">
                    <v-icon color="primary" class="mr-2">mdi-handshake</v-icon>
                    Transparencia
                  </v-card-title>
                  <v-card-text>
                    Facilitamos procesos claros y honestos entre empresas y candidatos.
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4 mb-4">
                  <v-card-title class="text-h6">
                    <v-icon color="success" class="mr-2">mdi-rocket</v-icon>
                    Innovación
                  </v-card-title>
                  <v-card-text>
                    Utilizamos tecnología de vanguardia para mejorar la experiencia de todos.
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4 mb-4">
                  <v-card-title class="text-h6">
                    <v-icon color="warning" class="mr-2">mdi-account-group</v-icon>
                    Inclusión
                  </v-card-title>
                  <v-card-text>
                    Promovemos la diversidad y la igualdad de oportunidades para todos.
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4 mb-4">
                  <v-card-title class="text-h6">
                    <v-icon color="info" class="mr-2">mdi-trophy</v-icon>
                    Excelencia
                  </v-card-title>
                  <v-card-text>
                    Nos esforzamos por brindar el mejor servicio y resultados de calidad.
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            
            <div class="text-h5 mb-4 mt-6">Nuestro Equipo</div>
            <p class="text-body-1 mb-4">
              Contamos con un equipo multidisciplinario de profesionales apasionados 
              por conectar talento con oportunidades. Desde desarrolladores y diseñadores 
              hasta especialistas en recursos humanos y atención al cliente.
            </p>
            
            <v-divider class="my-6"></v-divider>
            
            <div class="text-center">
              <v-btn 
                color="primary" 
                size="large"
                @click="$router.push('/contact')"
                class="mr-4"
              >
                <v-icon left>mdi-email</v-icon>
                Contáctanos
              </v-btn>
              
              <v-btn 
                color="secondary" 
                variant="outlined"
                size="large"
                @click="$router.push('/')"
              >
                <v-icon left>mdi-home</v-icon>
                Volver al Inicio
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// No se necesita lógica adicional para esta vista
</script>

<style scoped>
.v-card-title {
  word-break: normal;
}
</style>