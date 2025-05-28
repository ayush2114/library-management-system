<template>
  <Navbar />

  <div class="container mt-3">
    <h2 class="mb-4">Requested books</h2>
    <p v-if="requested_associations.length == 0">No books currently requested.</p>
    <table v-else class="table table-hover">
      <thead>
        <tr class="table-primary">
          <th scope="col">S.No</th>
          <th scope="col">Book Title</th>
          <th scope="col">Authors</th>
          <th scope="col">Section</th>
          <th scope="col">Requested By</th>
          <th scope="col"></th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>

        <tr v-for="(association, index) in requested_associations" :key="association.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ association.ebook_name }}</td>
          <td>{{ association.ebook_authors }}</td>
          <td>{{ association.section_name }}</td>
          <td>{{ association.user_email }}</td>

          <td scope="col">
            <button @click="grantRequest(association.user_id, association.ebook_id)"
              class="btn btn-success btn-sm">Grant</button>
          </td>
          <td scope="col">
            <button @click="rejectRequest(association.user_id, association.ebook_id)"
              class="btn btn-danger btn-sm">Reject</button>
          </td>

        </tr>

      </tbody>
    </table>
  </div>

  <div class="container mt-3">
    <h2 class="mb-4">Issued books</h2>
    <p v-if="issued_associations.length == 0">No books currently issued.</p>
    <table v-else class="table table-hover">
      <thead>
        <tr class="table-primary">
          <th scope="col">S.No</th>
          <th scope="col">Book Title</th>
          <th scope="col">Authors</th>
          <th scope="col">Section</th>
          <th scope="col">Issued To</th>
          <th scope="col">Issue Date</th>
          <th scope="col">Return Date</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>

        <tr v-for="(association, index) in issued_associations" :key="association.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ association.ebook_name }}</td>
          <td>{{ association.ebook_authors }}</td>
          <td>{{ association.section_name }}</td>
          <td>{{ association.user_email }}</td>
          <td>{{ formatDate(association.date_issued) }}</td>
          <td>{{ formatDate(association.date_return) }}</td>
          <td scope="col">
            <button @click="revokeAccess(association.user_id, association.ebook_id)"
              class="btn btn-warning btn-sm">Revoke</button>
          </td>
        </tr>

      </tbody>
    </table>

    <div v-if="issued_associations.length > 0" class="container mt-3">
      <h4 class="mb-4">Export Issued Books</h4>
      <button @click="exportEbooks" class="btn btn-dark">Export Books</button>
    </div>

  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import Navbar from '../components/AdminNavbar.vue'
export default {
  name: 'AdminDashboard',
  components: {
    Navbar
  },
  data() {
    return {
      task_id: '',
    }
  },
  mounted() {
    this.getAssociations();
  },

  methods: {
    ...mapActions(['getAssociations']),

    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('en', options);
    },

    async grantRequest(user_id, ebook_id) {
      try {
        const url = "http://127.0.0.1:5000/api/grant-request/" + user_id + "/" + ebook_id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token
          }
        });
        if (response.ok) {
          console.log('Request granted successfully');
          this.getAssociations()
        } else {
          const errorData = await response.json();
          console.log(errorData.message);
        }
      } catch (error) {
        console.error('error while granting request', error);
      }
    },

    async rejectRequest(user_id, ebook_id) {
      try {
        const url = "http://127.0.0.1:5000/api/reject-request/" + user_id + "/" + ebook_id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token
          }
        });
        if (response.ok) {
          console.log('Request rejected successfully');
          this.getAssociations()
        } else {
          const errorData = await response.json();
          console.log(errorData.message);
        }
      } catch (error) {
        console.error('error while rejecting request', error);
      }
    },

    async revokeAccess(user_id, ebook_id) {
      try {
        const url = "http://127.0.0.1:5000/api/revoke-access/" + user_id + "/" + ebook_id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token
          }
        });
        if (response.ok) {
          console.log('Access revoked successfully');
          this.getAssociations()
        } else {
          const errorData = await response.json();
          console.log(errorData.message);
        }
      } catch (error) {
        console.error('error while revoking access', error);
      }
    },

    async exportEbooks() {
      try {
        const url = "http://127.0.0.1:5000/start-export";
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token
          }
        });
        const data = await response.json();
        this.task_id = data.task_id;
        // console.log(data);

        // Fixed interval polling
        const interval = setInterval(async () => {
          try {
            const url = "http://127.0.0.1:5000/get-task/" + this.task_id;
            const response = await fetch(url, {
              headers: {
                "Authentication-token": this.$store.state.token
              }
            });
            if (!response.ok) {
              const errorData = await response.json();
              console.log(errorData.message);
            } else {
              alert("Export Completed. Please check your downloads folder.");
              clearInterval(interval);
            }
          } catch (error) {
            console.error("error during task status check", error);
          }
        }, 1000);
      } catch (error) {
        console.error("error in export", error);
      }
    },
  },

  computed: {
    ...mapState(['associations']),
    ...mapGetters(['requested_associations', 'issued_associations']),
  }
}
</script>


<style scoped>
.container {
  padding: 20px;
}
</style>