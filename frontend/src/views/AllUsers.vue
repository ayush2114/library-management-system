<template>
    <Navbar />
    <div class="container mt-4">
      <table class="table table-hover table-striped">
        <thead class="thead-dark">
          <tr>
            <th scope="col">User ID</th>
            <th scope="col">Email</th>
            <th scope="col">Books Requested</th>
            <th scope="col">Books Issued</th>
            <th scope="col">Books Purchased</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.ebooks_requested }}</td>
            <td>{{ user.ebooks_issued }}</td>
            <td>{{ user.ebooks_purchased }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

<script>
import Navbar from '../components/AdminNavbar.vue'
export default {
    name: 'AllUsers',
    components: {
        Navbar
    },
    computed: {
        users() {
            return this.$store.state.users
        },
    },
    created() {
        this.$store.dispatch('getUsers')
    }
}
</script>


<style scoped>
.all-users {
    padding: 20px;
}

</style>