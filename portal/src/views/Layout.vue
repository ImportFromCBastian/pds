<template>
  <div class="flex min-h-screen flex-col bg-gray-100">
    <Navbar />
    <main class="flex-grow">
      <slot></slot>
    </main>
    <FooterContent />
  </div>
</template>

<script>
import Navbar from '@/components/NavbarContent.vue'
import FooterContent from '@/components/FooterContent.vue'

export default {
  name: 'DefaultLayout',
  components: {
    Navbar,
    FooterContent
  }
}
</script>
