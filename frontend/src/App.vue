<template>
  <router-view/>
</template>

<style>
 #app {
  font-family: poppins, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.navbar {
    background-color: #7b00ff !important;
    padding: 15px;
}

.bookapp {
  font-weight: bold !important;
}
.btn-signout {
  background-color: #7b00ff;
  border: 2px solid white;
  color: white;
}

.btn-signout:hover {
  background-color: white;
  color: #7b00ff;
}

.nav-link {
  color: white !important;
}

.btn-container {
    display: flex;
    gap: 20px;
}

.btn-add {
    background-color: #4CAF50;
    color: white;
}
.btn-add:hover {
    background-color: #45a049;
}
.btn-cancel {
    background-color: #f44336;
    color: white;
}
.btn-cancel:hover {
    background-color: #d32f2f;
}
</style> 