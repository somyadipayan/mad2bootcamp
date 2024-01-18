<template>
  <div class="home">
    <NavBar />
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Bootcamp" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";
export default {
  name: "HomeView",
  components: {
    HelloWorld,
    NavBar,
  },
};
</script>
