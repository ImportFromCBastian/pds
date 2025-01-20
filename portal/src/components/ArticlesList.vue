<template>
  <main class="flex flex-1 flex-col bg-gray-100 p-6">
    <h1 class="mb-6 text-2xl font-bold text-gray-800">Noticias</h1>

    <form @submit.prevent="applyFilters" class="mb-6 space-y-4 rounded-md bg-cyan-100 p-5">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6">
        <div class="sm:col-span-2 lg:col-span-2">
          <label for="author" class="block text-sm font-medium text-gray-700">Autor</label>
          <input
            id="author"
            v-model="filters.author"
            type="text"
            placeholder="Ejemplo: María García"
            class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
          />
        </div>
        <div class="sm:col-span-1 lg:col-span-1">
          <label for="published_from" class="block text-sm font-medium text-gray-700">Desde</label>
          <input
            id="published_from"
            v-model="filters.published_from"
            type="date"
            :max="filters.published_to || today"
            class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
          />
        </div>
        <div class="sm:col-span-1 lg:col-span-1">
          <label for="published_from" class="block text-sm font-medium text-gray-700">Hasta</label>
          <input
            id="published_to"
            v-model="filters.published_to"
            type="date"
            :min="filters.published_from"
            :max="today"
            class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
          />
        </div>

        <div class="sm:col-span-1 lg:col-span-1">
          <label for="per_page" class="block text-sm font-medium text-gray-700"
            >Resultados por página</label
          >
          <select
            id="per_page"
            v-model="filters.per_page"
            @change="applyFilters"
            class="mt-1 h-12 w-full rounded-md border-gray-300 p-2 shadow-sm focus:border-cyan-500 focus:ring-cyan-500 sm:text-sm"
          >
            <option selected value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
        </div>

        <div class="flex sm:col-span-1">
          <button
            type="button mx-2"
            @click="resetFilters"
            class="mt-6 h-12 w-full rounded-md bg-gray-400 px-4 text-sm font-medium text-white shadow hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-offset-2"
          >
            Limpiar filtros
          </button>

          <button
            type="submit"
            class="mx-2 mt-6 h-12 w-full rounded-md bg-cyan-800 px-4 text-sm font-medium text-white shadow hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2"
          >
            Aplicar filtros
          </button>
        </div>
      </div>
    </form>

    <div
      v-if="articles.length > 0 && !loading && !error"
      class="grid flex-grow gap-6 sm:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3"
    >
      <div
        v-for="article in articles"
        :key="article.id"
        class="relative flex h-auto w-full max-w-full flex-col overflow-hidden rounded-lg bg-white p-4 shadow-md"
      >
        <h2 class="overflow-hidden text-ellipsis break-words text-lg font-semibold text-gray-800">
          {{ article.titulo }}
        </h2>
        <p class="mb-2 overflow-hidden text-ellipsis break-words text-sm text-gray-600">
          Autor: {{ article.autor }}
        </p>
        <p class="mb-2 overflow-hidden text-ellipsis break-words text-sm text-gray-500">
          Fecha de publicación: {{ formatDate(article.fecha_publicacion) }}
        </p>
        <p class="mb-4 overflow-hidden text-ellipsis break-words text-gray-700">
          {{ article.copete }}
        </p>
        <router-link
          v-if="article.id"
          :to="{ name: 'article-details', params: { id: article.id } }"
          class="absolute bottom-2 left-4 text-blue-500 hover:underline"
        >
          Leer más
        </router-link>
      </div>
    </div>

    <div
      v-if="articles.length > 0 && !loading && !error"
      class="mt-10 items-center justify-between"
    >
      <div class="text-sm text-gray-700">
        Mostrando {{ articles.length }} de {{ totalArticles }} resultados
      </div>

      <div class="mt-2 flex items-center space-x-2">
        <button
          v-if="currentPage > 1"
          @click="changePage(currentPage - 1)"
          class="rounded bg-cyan-800 px-4 py-2 text-white hover:bg-cyan-600"
        >
          Anterior
        </button>
        <button
          v-for="page in totalPages"
          :key="page"
          @click="changePage(page)"
          :class="{
            'bg-gray-300': page === currentPage,
            'bg-cyan-800 text-white hover:bg-cyan-600': page !== currentPage
          }"
          class="rounded px-4 py-2"
        >
          {{ page }}
        </button>
        <button
          v-if="currentPage < totalPages"
          @click="changePage(currentPage + 1)"
          class="rounded bg-cyan-800 px-4 py-2 text-white hover:bg-cyan-600"
        >
          Siguiente
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center text-gray-500">Cargando artículos...</div>
    <div v-if="error" class="text-center text-red-500">
      Hubo un error al cargar los artículos. Por favor, intenta nuevamente.
    </div>
    <div v-if="articles.length === 0 && !loading && !error" class="text-center text-gray-500">
      No se encontraron artículos.
    </div>
  </main>
</template>

<script setup>
import { onMounted, watch } from 'vue'

import {
  articles,
  loading,
  error,
  fetchArticles,
  filters,
  totalArticles,
  currentPage,
  totalPages
} from '@/stores/articles'

const today = new Date().toISOString().split('T')[0]

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}
const changePage = (page) => {
  currentPage.value = page
  fetchArticles()
}

const applyFilters = () => {
  const params = {}
  currentPage.value = 1

  if (filters.value.author) {
    params.author = filters.value.author
  }

  if (filters.value.published_from) {
    params.published_from = filters.value.published_from
  }

  if (filters.value.published_to) {
    params.published_to = filters.value.published_to
  }
  params.per_page = filters.value.per_page
  fetchArticles(params)
}
const resetFilters = () => {
  filters.value.author = ''
  filters.value.published_from = ''
  filters.value.published_to = ''
  filters.value.per_page = '10'
  applyFilters()
}
onMounted(() => {
  fetchArticles()
})
watch(
  () => filters.value.published_from,
  (newFrom) => {
    if (newFrom && filters.value.published_to && newFrom > filters.value.published_to) {
      filters.value.published_to = ''
    }
  }
)

watch(
  () => filters.value.published_to,
  (newTo) => {
    if (newTo && filters.value.published_from && newTo < filters.value.published_from) {
      filters.value.published_from = ''
    }
  }
)
</script>
