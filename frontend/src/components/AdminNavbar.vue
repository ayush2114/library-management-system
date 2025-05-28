<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
      <span class="navbar-brand bookapp">BookApp</span>
      <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link" aria-current="page">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ 'name': 'AdminEbooks' }" class="nav-link">Books</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ 'name': 'AllUsers' }" class="nav-link">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ 'name': 'AdminStats' }" class="nav-link">Stats</router-link>
          </li>
        </ul>
      </div>
      <span class="navbar-brand">{{ user.email }}</span>
      <router-link to="/" @click="logout" class="btn btn-sm btn-signout">Sign Out</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNavbar',
  data() {
    return {
      user: this.$store.getters.user
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      // this.$router.push('/')
    }
  }
}
</script>