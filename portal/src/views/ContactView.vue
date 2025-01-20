<template>
  <DefaultLayout>
    <ContactContent />
  </DefaultLayout>
</template>

<script>
import DefaultLayout from '@/views/Layout.vue'
import ContactContent from '@/components/ContactContent.vue'

export default {
  name: 'ArticlesView',
  components: {
    DefaultLayout,
    ContactContent
  }
}
</script>
