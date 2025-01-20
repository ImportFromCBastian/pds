<template>
  <main class="flex-1">
    <div class="flex w-full flex-col items-center pt-0 text-center">
      <div class="relative w-full bg-[url('../assets/grupo.jpg')] bg-cover bg-center bg-no-repeat">
        <div class="absolute inset-0 z-0 bg-opacity-30 backdrop-blur-sm"></div>

        <div class="relative z-10 space-y-4">
          <h1
            class="mx-auto mt-10 max-w-4xl rounded-lg bg-opacity-50 p-4 text-3xl font-bold tracking-tighter text-white sm:text-4xl md:text-5xl lg:text-6xl"
          >
            Transformando Vidas con Amor Equino
          </h1>
          <p
            class="mx-auto max-w-[700px] rounded-lg bg-cyan-600 bg-opacity-60 p-4 text-xl text-white"
          >
            Descubre el poder sanador de nuestros amigos de cuatro patas en un ambiente cálido y
            acogedor.
          </p>
        </div>
        <div class="relative z-10 mb-16 mt-5 space-x-4">
          <router-link to="/contact">
            <button class="rounded-lg bg-white px-6 py-2 text-cyan-800 hover:bg-cyan-100">
              Contáctanos
            </button>
          </router-link>
        </div>
      </div>
    </div>

    <section class="w-full py-12 md:py-24 lg:py-32">
      <div class="container mx-auto px-4 md:px-6">
        <h2
          class="mb-8 text-center text-3xl font-bold tracking-tighter text-cyan-600 sm:text-4xl md:text-5xl"
        >
          La Magia de la Equinoterapia
        </h2>
        <div class="grid gap-6 lg:grid-cols-3 lg:gap-12">
          <div
            class="rounded-lg bg-white p-4 shadow-lg transition-shadow duration-300 hover:shadow-xl"
          >
            <img
              src="../assets/caballo.jpg"
              alt="Niño montando un caballo"
              class="mb-4 h-96 w-full rounded-md object-cover"
            />
            <h3 class="mb-2 text-xl font-bold text-cyan-600">Conexión Emocional</h3>
            <p>
              Fortalece lazos emocionales y fomenta la confianza a través del vínculo especial entre
              humanos y caballos.
            </p>
          </div>

          <div
            class="rounded-lg bg-white p-4 shadow-lg transition-shadow duration-300 hover:shadow-xl"
          >
            <img
              src="../assets/caballo2.jpg"
              alt="Niña parada sobre un caballo caballo durante terapia"
              class="mb-4 h-96 w-full rounded-md object-cover"
            />
            <h3 class="mb-2 text-xl font-bold text-cyan-700">Desarrollo Físico</h3>
            <p>
              Mejora el equilibrio, la coordinación y la fuerza muscular a través del movimiento
              rítmico del caballo.
            </p>
          </div>

          <div
            class="rounded-lg bg-white p-4 shadow-lg transition-shadow duration-300 hover:shadow-xl"
          >
            <img
              src="../assets/caballo1.jpg"
              alt="Persona montando un caballo"
              class="mb-4 h-96 w-full rounded-md object-cover"
            />
            <h3 class="mb-2 text-xl font-bold text-cyan-700">Crecimiento Cognitivo</h3>
            <p>
              Estimula la concentración, la memoria y las habilidades de resolución de problemas en
              un entorno natural.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="w-full bg-cyan-100 py-12 md:py-24 lg:py-32">
      <div class="container mx-auto px-4 text-center md:px-6">
        <h2 class="mb-4 text-3xl font-bold tracking-tighter text-cyan-800 sm:text-4xl md:text-5xl">
          No te pierdas de las últimas noticias
        </h2>
        <p class="mx-auto mb-8 max-w-[700px] text-gray-700 md:text-xl">
          Descubre todo lo que está pasando en CEDICA
        </p>
        <router-link to="/articles">
          <button class="rounded-lg bg-cyan-600 px-6 py-2 text-white hover:bg-cyan-600">
            Ver noticias
          </button>
        </router-link>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>
