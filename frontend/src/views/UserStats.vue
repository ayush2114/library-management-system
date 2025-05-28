<template>
  <Navbar />
  <div class="container mt-5">
    <h2 class="mb-4">Statistics</h2>
    <p>Here are some statistics for your account</p>
    <ul class="list-group">
      <li class="list-group-item">Number of books available: {{ total_ebooks }}</li>
      <li class="list-group-item">Number of books issued: {{ total_issued }}</li>
      <li class="list-group-item">Number of books purchased: {{ total_purchased }}</li>
      <li class="list-group-item">Number of books requested: {{ total_requested }}</li>
    </ul>
  </div>
</template>

<script>
import Navbar from '../components/UserNavbar.vue'
export default {
  name: 'UserStats',
  components: {
    Navbar
  },
  data() {
    return {
      total_ebooks: 0,
      total_issued: 0,
      total_purchased: 0,
      total_requested: 0
    }
  },
  methods: {
    async getStats() {
      const url = "http://127.0.0.1:5000/api/user-stats/" + this.$store.state.id;
      const res = await fetch(url, {
        headers: {
          "Authentication-token": this.$store.state.token
        }
      });
      const data = await res.json();
      console.log(data);
      this.total_ebooks = data.total_ebooks;
      this.total_issued = data.total_issued;
      this.total_purchased = data.total_purchased;
      this.total_requested = data.total_requested;
    }
  },
  mounted() {
    this.getStats();
  }
}
</script>