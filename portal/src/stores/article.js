import { ref } from 'vue'

const article = ref(null)
const loading = ref(false)
const error = ref(null)

const fetchArticle = async (id) => {
  loading.value = true
  error.value = null

  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL
    const response = await fetch(`${baseUrl}/articles/${id}`)
    if (!response.ok) {
      throw new Error('Error al cargar el artículo')
    }

    const data = await response.json()
    article.value = data.data
  } catch (err) {
    error.value = err.message || 'Error al cargar el artículo'
  } finally {
    loading.value = false
  }
}

export { article, loading, error, fetchArticle }
