<template>
  <DefaultLayout>
    <ArticlesContent />
  </DefaultLayout>
</template>

<script>
import DefaultLayout from '@/views/Layout.vue'
import ArticlesContent from '@/components/ArticlesList.vue'

export default {
  name: 'ArticlesView',
  components: {
    DefaultLayout,
    ArticlesContent
  }
}
</script>
