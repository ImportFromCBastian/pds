<template>
  <main class="flex w-full flex-1 flex-col items-center bg-gray-100">
    <div
      v-if="!loading && !error && article"
      class="relative m-10 flex w-full max-w-6xl flex-col space-y-4 rounded-lg bg-white p-6 shadow-md sm:min-w-[20px] md:min-w-[600px] lg:min-w-[1000px] xl:min-w-[1500px]"
    >
      <router-link
        to="/articles"
        class="flex w-fit items-center space-x-2 rounded-md pb-2"
        alt="Volver al listado de noticias"
      >
        <span class="material-icons text-md">arrow_back</span>

        <span class="material-icons text-md">list_alt</span>
      </router-link>

      <p class="flex items-center justify-end space-x-2 align-middle text-sm text-gray-500">
        <span class="material-icons text-sm">calendar_today</span>
        <span>
          {{ formatDate(article.fecha_publicacion) }}
        </span>
      </p>

      <h1 class="break-words text-3xl font-bold text-gray-800">
        {{ article.titulo }}
      </h1>
      <h2 class="break-words text-lg font-thin text-gray-800">
        {{ article.copete }}
      </h2>
      <div class="mt-4 break-words rounded-md bg-cyan-100 p-2 text-gray-700">
        {{ article.contenido }}
      </div>

      <div class="border-t border-gray-300 pt-4">
        <div class="flex items-center justify-between text-sm text-gray-500">
          <span class="flex items-center">
            <span class="material-icons mr-2 text-sm"> person </span>
            Autor: {{ article.autor }}
          </span>
        </div>
      </div>
    </div>
    <div v-if="loading">
      <p class="text-center text-gray-500">Cargando artículo...</p>
    </div>
    <div v-if="error">
      <p class="text-center text-red-500">Error al cargar el arículo.</p>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchArticle, article, error, loading } from '@/stores/article'

const route = useRoute()
const articleId = route.params.id

onMounted(() => {
  fetchArticle(articleId)
})

const formatDate = (date, withTime = true) => {
  const optionsDate = { year: 'numeric', month: 'long', day: 'numeric' }
  const optionsTime = { hour: '2-digit', minute: '2-digit' }

  const formattedDate = new Date(date).toLocaleDateString('es-ES', optionsDate)

  if (withTime) {
    const formattedTime = new Date(date).toLocaleTimeString('es-ES', optionsTime)
    return `${formattedDate} a las ${formattedTime}`
  }

  return formattedDate
}
</script>
