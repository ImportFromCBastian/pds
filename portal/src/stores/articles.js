import { ref } from 'vue'

const articles = ref([])
const totalArticles = ref(0)
const currentPage = ref(1)
const totalPages = ref(0)
const loading = ref(false)
const error = ref(null)
const filters = ref({
  author: '',
  published_from: '',
  published_to: '',
  per_page: 5
})

const fetchArticles = async (params = {}) => {
  loading.value = true
  error.value = null

  try {
    const queryParams = { ...filters.value, ...params, page: currentPage.value }
    const queryString = new URLSearchParams(queryParams).toString()
    const baseUrl = import.meta.env.VITE_API_BASE_URL

    const response = await fetch(`${baseUrl}/articles/?${queryString}`)

    if (!response.ok) {
      throw new Error('Error al cargar los artículos')
    }

    const data = await response.json()

    articles.value = data.data
    totalArticles.value = data.total
    currentPage.value = data.page
    totalPages.value = Math.ceil(data.total / filters.value.per_page)
  } catch (err) {
    error.value = err.message || 'Error al cargar los artículos'
  } finally {
    loading.value = false
  }
}

export { articles, totalArticles, currentPage, totalPages, loading, error, fetchArticles, filters }
