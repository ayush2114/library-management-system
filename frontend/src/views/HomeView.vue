<template>
  <div class="home">
  <div class="container">
    <h1>Library Management System</h1>
    <p>Get started with Library</p>
    <div class="button-container">
      <router-link class="btn" to="/signup">Create a new account</router-link>
      <router-link class="btn" to="/login">Sign in with your account</router-link>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  font-family: 'Arial', sans-serif;
  background: linear-gradient(to bottom right, #6a11cb, #2575fc);
  /* background-color: #6a11cb; */
  color: #fff;
}

.container {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

h1 {
  font-size: 4em;
  margin-bottom: 0.5em;
}

p {
  font-size: 1.5em;
  margin-bottom: 2em;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  background-color: #fff;
  color: #6a11cb;
  padding: 15px 30px;
  border-radius: 5px;
  font-size: 1.2em;
}

.btn:hover {
  background-color: #2575fc;
  color: #fff;
}
</style>