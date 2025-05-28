<template>
    <nav class="navbar navbar-expand-lg navbar-dark">
      
    <div class="container-fluid">
      <span class="navbar-brand bookapp">BookApp</span>
   
      <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/user/dashboard" class="nav-link" aria-current="page">Books</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/ebooks" class="nav-link">My Books</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/stats" class="nav-link">Stats</router-link>
          </li>
        </ul>
      </div>
      <span class="navbar-brand">{{ user.email }}</span>
      
      <button class="btn btn-sm btn-signout" @click="logout">Sign Out</button>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'UserNavbar',
  data() {
    return {
      user: this.$store.getters.user
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('logout')
      this.$router.push('/')
    }
  }
}
</script>