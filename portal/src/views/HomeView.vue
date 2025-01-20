<template>
  <DefaultLayout>
    <HomeContent />
  </DefaultLayout>
</template>

<script>
import DefaultLayout from '@/views/Layout.vue'
import HomeContent from '@/components/HomeContent.vue'

export default {
  name: 'ArticlesView',
  components: {
    DefaultLayout,
    HomeContent
  }
}
</script>
