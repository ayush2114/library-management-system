<template>
  <Navbar />

  <div class="container mt-3">
    <h2 class="mb-4">Statistics</h2>
    <p>Here are some statistics for the system:</p>
    <ul>
      <li>Total number of users: {{ total_users }}</li>
      <li>Total number of sections in the library: {{ total_sections }}</li>
      <li>Total number of ebooks in the library: {{ total_ebooks }}</li>
      <li v-if="sections.length > 0">Section-wise distribution of ebooks:</li>
        <ul>
          <li v-for="section in sections" :key="section.id">{{ section.name }}: {{ section.total_ebooks }}</li>
        </ul>
    </ul>
  </div>


</template>

<script>
import Navbar from '../components/AdminNavbar.vue'
export default {
  name: 'AdminStats',
  components: {
    Navbar
  },
  data() {
    return {
      total_users: 0,
      total_ebooks: 0,
    }
  },
  computed: {
    total_sections() {
      return this.sections.length;
    },
    sections() {
      return this.$store.state.sections;
    }
  },
  methods: {
    async getStats() {
      try {
        const url = 'http://localhost:5000/api/admin-stats';
        const response = await fetch(url, {
          headers: {
            'Authentication-token': this.$store.state.token
          }
        });
        const data = await response.json();
        this.total_users = data.total_users;
        this.total_ebooks = data.total_ebooks;

      } catch (error) {
        console.error(error);
      }
    },

  },
  async mounted() {
    await this.getStats();
    this.$store.dispatch('getSections');
  }
}
</script>