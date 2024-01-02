<template>
  <Navbar/>
  <router-view></router-view>
  
  <footer class="bg-gray-800">
      <div class="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-center">
        <span class="text-sm text-gray-400 sm:text-center dark:text-gray-400">
          © 2024 <a href="https://ahloytan.netlify.app/" class="hover:underline" aria-label="Aloysius Tan">Aloysius Tan</a>. Coded in Singapore. All Rights Reserved.
        </span>
      </div>
  </footer>

</template>
<script>
import Navbar from './components/Navbar.vue'

export default {
  name: "App",
  components: {
    Navbar,
  },
}

</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

</style>
