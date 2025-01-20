<template>
  <main class="flex flex-1 flex-col bg-gray-100 p-6">
    <div class="contact-form">
      <form @submit.prevent="sendForm" class="mb-6 space-y-4 rounded-md bg-cyan-100 p-5">
        <div class="grid grid-cols-2 gap-2 sm:grid-cols-2 lg:grid-cols-6">
          <div class="sm:col-span-2 lg:col-span-2">
            <label for="titulo" class="block text-sm font-medium text-gray-700">Titulo de la Consulta:</label>
            <input
              v-model="form.titulo"
              type="text"
              placeholder="Titulo"
              class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
              required
            />
            <span v-if="errors.titulo" class="error">{{ errors.titulo }}</span>
          </div>
          <div class="sm:col-span-2 lg:col-span-2">
            <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico:</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="Tu correo electrónico"
              class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
              required
            />
            <span v-if="errors.email" class="error">{{ errors.email }}</span>
          </div>
        </div>
        <div class="sm:col-span-2 lg:col-span-2">
          <label for="descripcion" class="block text-sm font-medium text-gray-700">Mensaje:</label>
          <textarea
            v-model="form.descripcion"
            placeholder="Escribe tu consulta"
            class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
            required
          ></textarea>
          <span v-if="errors.descripcion" class="error">{{ errors.descripcion }}</span>
        </div>
        <div class="sm:col-span-2 lg:col-span-2">
          <label for="g-recaptcha" class="block text-sm font-medium text-gray-700">Verificación reCAPTCHA</label>
          <div>
            <div v-if="loadingCaptcha" class="text-sm text-gray-500">
              Cargando validación reCAPTCHA, espere un momento... <!-- Espero que sea un pequeño momento siempre -->
            </div>
            <div class="g-recaptcha" :data-sitekey="captchaKey" id="recaptcha-container"></div>
          </div>
        </div>
        <div>
          <button
            type="submit"
            :disabled="loadingCaptcha"
            class="mx-2 mt-6 h-12 w-full rounded-md bg-cyan-800 px-4 text-sm font-medium text-white shadow hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            Enviar Mensaje
          </button>
        </div>
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { sendMessage } from '@/stores/contact'

const form = ref({
  titulo: '',
  email: '',
  descripcion: '',
})

const errors = ref({})
const loadingCaptcha = ref(true)
const captchaKey = import.meta.env.VITE_API_CAPTCHA_SITE_WEB

const sendForm = async () => {
  errors.value = {}

  if (!form.value.titulo.trim()) {
    errors.value.titulo = 'El título no debe estar vacío o ser solo espacios.'
  }
  if (!form.value.email.trim() || !form.value.email.includes('@')) {
    errors.value.email = 'El email debe contener un @ y no puede estar vacío.'
  }
  if (!form.value.descripcion.trim()) {
    errors.value.descripcion = 'La descripción no debe estar vacía o ser solo espacios.'
  }

  if (Object.keys(errors.value).length > 0) {
    alert('Por favor, corrija los errores antes de enviar.')
    return
  }

  try {
    const recaptchaResponse = grecaptcha.getResponse()
    if (!recaptchaResponse) {
      alert("Resuelva la verificación reCAPTCHA para enviar su consulta")
      return
    }

    const formDataWithRecaptcha = {
      ...form.value,
      recaptcha: recaptchaResponse,
    }

    const jsonFormData = JSON.stringify(formDataWithRecaptcha)
    const response = await sendMessage(jsonFormData)

    if (response.status === 201) {
      alert('Su consulta ha sido enviada')
      resetForm()
      location.reload()
    } 
    else {
      alert('Ha ocurrido un error al enviar su consulta')
    }
  } 
  catch (error) {
    if (error.data) {
      errors.value = error.data
    } else {
      alert('Ha ocurrido un error inesperado')
    }
  }
}

const resetForm = () => {
  form.value.titulo = ''
  form.value.email = ''
  form.value.descripcion = ''
}

onMounted(() => {
  setTimeout(() => {
    if (window.grecaptcha) {
      grecaptcha.ready(() => {
        grecaptcha.render('recaptcha-container', {})
        loadingCaptcha.value = false
      })
    } else {
      alert('No se ha podido cargar la validacion reCAPTCHA, reingrese a la sección Contacto para reintentar el envio de la Consulta')
    }
  }, 1000)
})

</script>

<style scoped>
.error {
  color: red;
  font-size: 12px;
}
</style>
