<template>
  <nav class="relative bg-cyan-800 p-4 text-white">
    <div class="flex space-x-2">
      <router-link to="/" class="flex">
        <img src="../assets/logo.png" alt="logo cedica" class="h-10" />

        <img src="../assets/logo_texto.png" alt="texto cedica" class="hidden h-10 sm:block" />
      </router-link>
    </div>

    <div
      class="absolute left-0 right-0 top-1/2 flex -translate-y-1/2 transform justify-center space-x-4"
    >
      <router-link to="/" class="hover:underline">Inicio</router-link>
      <router-link to="/articles" class="hover:underline">Noticias</router-link>
      <router-link to="/contact" class="hover:underline">Contacto</router-link>
    </div>
  </nav>
</template>
