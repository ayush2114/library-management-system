<template>
  <Navbar />

  <div class="container mt-3">
    <form @submit.prevent="search" class="d-flex">
      <input v-model="search_word" class="form-control search-input me-2" type="search" placeholder="Search" aria-label="Search" name="search_word">
      <button class="btn btn-outline-success btn-search" type="submit">Search</button>
    </form>
  </div>

  <div class="container mt-5">
    <h2 class="mb-4">Books in the Library</h2>

    <p v-if="filteredEbooks.length == 0">No books in the library.</p>

    <table v-else class="table table-hover">
      <thead>
        <tr class="table-primary">
          <th scope="col">S.No</th>
          <th scope="col">Book Title</th>
          <th scope="col">Authors</th>
          <th scope="col">Section</th>
          <th scope="col">Rating</th>
          <th scope="col">Status</th>
        </tr>
      </thead>
      <tbody>

        <tr v-for="(ebook, index) in filteredEbooks" :key="ebook.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ ebook.name }}</td>
          <td>{{ ebook.authors }}</td>
          <td>{{ ebook.section_name }}</td>
          <td v-if="ebook.average_rating">{{ ebook.average_rating }}</td>
          <td v-else>-</td>

          <td v-if="is_requested(ebook)">Requested</td>
          <td v-else-if="is_issued(ebook)">Issued</td>
          <td v-else-if="is_purchased(ebook)">Purchased</td>

          <td scope="col" v-else>
            <button @click="requestEbook(ebook.id)" class="btn btn-outline-success btn-sm">Request</button>
          </td>

        </tr>

      </tbody>
    </table>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import Navbar from '../components/UserNavbar.vue'
export default {
  name: 'UserDashboard',
  components: {
    Navbar
  },
  data() {
    return {
      // user_associations: this.$store.state.user_associations,
      search_word: ''
    }
  },

  computed: {
    ...mapState(['ebooks', 'user_associations']),

    filteredEbooks() {
      if (!this.search_word) {
        return this.ebooks;
      }
      const query = this.search_word.toLowerCase();
      return this.ebooks.filter((ebook) => {
        return (
          ebook.name.toLowerCase().includes(query) ||
          ebook.authors.toLowerCase().includes(query) ||
          ebook.section_name.toLowerCase().includes(query)
      );
      });
    },
  },
 
  mounted() {
    this.getEbooks();
    this.getUserAssociations();
  },

  methods: {
    ...mapActions(['getEbooks', 'getUserAssociations']),

    search() {
      console.log('searching for: ' + this.search_word);
    },

    async requestEbook(ebook_id) {
      try {
        const url = "http://127.0.0.1:5000/api/request-ebook/" + this.$store.state.id + "/" + ebook_id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token,
          }
        });
        if (response.ok) {
          console.log("Ebook requested successfully");
          this.getUserAssociations();
        } else {
          const errorData = await response.json();
          alert(errorData.message);
        }
      } catch (error) {
        console.error(error);
      }
    },

    is_requested(ebook) {
      for (let i = 0; i < this.user_associations.length; i++) {
        if (this.user_associations[i].ebook_id == ebook.id && this.user_associations[i].request_status == 'requested') {
          return true
        }
      }
      return false
    },

    is_issued(ebook) {
      for (let i = 0; i < this.user_associations.length; i++) {
        if (this.user_associations[i].ebook_id == ebook.id && this.user_associations[i].request_status == 'issued') {
          return true
        }
      }
      return false
    },

    is_purchased(ebook) {
      for (let i = 0; i < this.user_associations.length; i++) {
        if (this.user_associations[i].ebook_id == ebook.id && this.user_associations[i].request_status == 'purchased') {
          return true
        }
      }
      return false
    },

  }
}
</script>

<style scoped>
.btn-search {
  color: rgb(95, 0, 220) !important;
  border-color: rgb(95, 0, 220) !important;
}

.btn-search:hover {
  background-color: rgb(95, 0, 220) !important;
  border-color: rgb(95, 0, 220) !important;
  color: white !important;
}

.search-input {
  border-color: rgb(95, 0, 220) !important;
  background-color: white !important;
  color: rgb(95, 0, 220) !important;
}

/* .btn-request {
  background-color: rgb(128, 65, 210) !important;
  border-color: rgb(95, 0, 220) !important;
  color: white !important;
} */
</style>