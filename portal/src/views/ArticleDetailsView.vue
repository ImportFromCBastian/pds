<template>
  <DefaultLayout>
    <ArticleDetails />
  </DefaultLayout>
</template>

<script>
import DefaultLayout from '@/views/Layout.vue'
import ArticleDetails from '@/components/ArticleDetails.vue'

export default {
  name: 'ArticlesDetailsView',
  components: {
    DefaultLayout,
    ArticleDetails
  }
}
</script>
