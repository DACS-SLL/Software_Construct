<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h3 text-center mb-6">
            Términos y Condiciones
          </v-card-title>
          
          <v-card-subtitle class="text-center mb-6">
            Última actualización: {{ fechaActualizacion }}
          </v-card-subtitle>
          
          <v-card-text>
            <div class="text-body-1">
              <section class="mb-6">
                <h2 class="text-h5 mb-3">1. Aceptación de los Términos</h2>
                <p>
                  Al acceder y utilizar la Plataforma de Empleo, usted acepta estar sujeto 
                  a estos Términos y Condiciones de Uso. Si no está de acuerdo con alguna 
                  parte de estos términos, no debe utilizar nuestro servicio.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">2. Descripción del Servicio</h2>
                <p>
                  Plataforma de Empleo es un servicio web que conecta a empleadores con 
                  candidatos en busca de empleo. Proporcionamos herramientas para:
                </p>
                <ul class="ml-6 mb-3">
                  <li>Publicar ofertas de trabajo</li>
                  <li>Buscar oportunidades laborales</li>
                  <li>Gestionar aplicaciones y candidatos</li>
                  <li>Facilitar la comunicación entre empleadores y candidatos</li>
                </ul>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">3. Registro y Cuentas de Usuario</h2>
                <p>Para utilizar ciertos servicios, debe crear una cuenta proporcionando:</p>
                <ul class="ml-6 mb-3">
                  <li>Información precisa y actualizada</li>
                  <li>Una dirección de correo electrónico válida</li>
                  <li>Una contraseña segura</li>
                </ul>
                <p>
                  Usted es responsable de mantener la confidencialidad de su cuenta 
                  y contraseña, y de todas las actividades que ocurran bajo su cuenta.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">4. Responsabilidades del Usuario</h2>
                <p>Como usuario de nuestra plataforma, usted se compromete a:</p>
                <ul class="ml-6 mb-3">
                  <li>Proporcionar información veraz y precisa</li>
                  <li>No publicar contenido falso, engañoso o fraudulento</li>
                  <li>Respetar los derechos de otros usuarios</li>
                  <li>No utilizar el servicio para actividades ilegales</li>
                  <li>Mantener actualizada su información de perfil</li>
                </ul>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">5. Contenido del Usuario</h2>
                <p>
                  Al publicar contenido en nuestra plataforma (currículums, ofertas de trabajo, 
                  mensajes, etc.), usted otorga a Plataforma de Empleo una licencia no exclusiva, 
                  transferible, libre de regalías para usar, modificar, mostrar públicamente y 
                  distribuir dicho contenido únicamente con el propósito de operar el servicio.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">6. Privacidad y Protección de Datos</h2>
                <p>
                  Su privacidad es importante para nosotros. El uso de su información personal 
                  está regido por nuestra 
                  <router-link to="/privacy" class="text-primary">Política de Privacidad</router-link>, 
                  que forma parte integral de estos términos.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">7. Conducta Prohibida</h2>
                <p>Está estrictamente prohibido:</p>
                <ul class="ml-6 mb-3">
                  <li>Acosar, intimidar o discriminar a otros usuarios</li>
                  <li>Publicar ofertas falsas o fraudulentas</li>
                  <li>Spammar o enviar comunicaciones no solicitadas</li>
                  <li>Intentar hackear o comprometer la seguridad del sistema</li>
                  <li>Usar bots o scripts automatizados sin autorización</li>
                </ul>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">8. Tarifas y Pagos</h2>
                <p>
                  Algunos servicios pueden requerir pago. Las tarifas se comunicarán 
                  claramente antes de la contratación. Los pagos no son reembolsables 
                  salvo casos específicos establecidos en nuestra política de reembolsos.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">9. Limitación de Responsabilidad</h2>
                <p>
                  Plataforma de Empleo actúa como intermediario. No garantizamos la 
                  veracidad de las ofertas publicadas ni el éxito en la búsqueda de empleo. 
                  No somos responsables de las interacciones entre empleadores y candidatos 
                  fuera de nuestra plataforma.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">10. Modificación de los Términos</h2>
                <p>
                  Nos reservamos el derecho de modificar estos términos en cualquier momento. 
                  Los cambios serán notificados a través de la plataforma y entrarán en vigor 
                  después de un período de 30 días desde su publicación.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">11. Terminación del Servicio</h2>
                <p>
                  Tanto usted como Plataforma de Empleo pueden terminar la relación en 
                  cualquier momento. En caso de violación de estos términos, nos reservamos 
                  el derecho de suspender o cancelar su cuenta inmediatamente.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">12. Ley Aplicable</h2>
                <p>
                  Estos términos se rigen por las leyes de la República del Perú. 
                  Cualquier disputa será resuelta en los tribunales competentes de Arequipa.
                </p>
              </section>
              
              <section class="mb-6">
                <h2 class="text-h5 mb-3">13. Contacto</h2>
                <p>
                  Si tiene preguntas sobre estos términos, puede contactarnos a través de:
                </p>
                <ul class="ml-6">
                  <li>Email: legal@plataformaempleo.com</li>
                  <li>Teléfono: +51 54 123-4567</li>
                  <li>Dirección: Av. Ejército 123, Cercado, Arequipa</li>
                </ul>
              </section>
            </div>
            
            <v-divider class="my-6"></v-divider>
            
            <div class="text-center">
              <v-btn 
                color="primary" 
                size="large"
                @click="$router.push('/contact')"
                class="mr-4"
              >
                <v-icon left>mdi-email</v-icon>
                ¿Preguntas? Contáctanos
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
import { computed } from 'vue'

const fechaActualizacion = computed(() => {
  return new Date('2025-01-15').toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})
</script>

<style scoped>
h2 {
  color: rgb(var(--v-theme-primary));
  font-weight: 600;
}

ul {
  list-style-type: disc;
}

li {
  margin-bottom: 4px;
}

section {
  scroll-margin-top: 100px;
}
</style>