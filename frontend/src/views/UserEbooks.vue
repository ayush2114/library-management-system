<template>
  <Navbar />

  <div class="container mt-5">
    <h2 class="mb-4"> My current issued books</h2>

    <p v-if="issued_associations.length == 0">No books currently issued.</p>

    <table v-else class="table table-hover">
      <thead>
        <tr class="table-primary">
          <th scope="col">S.No</th>
          <th scope="col">Book Title</th>
          <th scope="col">Authors</th>
          <th scope="col">Section</th>
          <th scope="col">Issue Date</th>
          <th scope="col">Return Date</th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col"></th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(association, index) in issued_associations" :key="association.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ association.ebook_name }}</td>
          <td>{{ association.ebook_authors }}</td>
          <td>{{ association.section_name }}</td>
          <td>{{ formateDate(association.date_issued) }}</td>
          <td>{{ formateDate(association.date_return) }}</td>
          <td scope="col">
            <router-link :to="{ name: 'ReadEbook', params: { ebook_id: association.ebook_id } }"
              class="btn btn-secondary btn-sm">Read</router-link>
          </td>
          <td scope="col">
            <button @click="returnEbook(association.user_id, association.ebook_id)"
              class="btn btn-warning btn-sm">Return</button>
          </td>
          <td scope="col">
            <router-link :to="{ name: 'BuyEbook', params: { ebook_id: association.ebook_id } }"
              class="btn btn-success btn-sm">Buy</router-link>
          </td>
          <td scope="col">
            <button @click="toggleForm(index, 'issued')" class="btn btn-info btn-sm">Rate</button>
            <RateForm v-if="rateFormVisibleIssued[index]" @close="toggleForm(index, 'issued')"
              @submit-rating="submitRating" :user_id="association.user_id" :ebook_id="association.ebook_id" />
          </td>
        </tr>
      </tbody>

    </table>
  </div>

  <div class="container mt-5">
    <h2 class="mb-4"> Purchased books</h2>

    <p v-if="purchased_associations.length == 0">You have not purchased any ebooks.</p>

    <table v-else class="table table-hover">

      <thead>
        <tr class="table-primary">
          <th scope="col">S.No</th>
          <th scope="col">Book Title</th>
          <th scope="col">Authors</th>
          <th scope="col">Section</th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col"></th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(association, index) in purchased_associations" :key="association.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ association.ebook_name }}</td>
          <td>{{ association.ebook_authors }}</td>
          <td>{{ association.section_name }}</td>
          <td scope="col">
            <router-link :to="{ name: 'ReadEbook', params: { ebook_id: association.ebook_id } }"
              class="btn btn-secondary btn-sm">Read</router-link>
          </td>
          <td scope="col">
            <button @click="toggleForm(index, 'purchased')" class="btn btn-info btn-sm">Rate</button>
            <RateForm v-if="rateFormVisiblePurchased[index]" @close="toggleForm(index, 'purchased')"
              @submit-rating="submitRating" :user_id="association.user_id" :ebook_id="association.ebook_id" />
          </td>
          <td scope="col">
            <button @click="downloadEbook(association.ebook_id, association.ebook_name)" class="btn btn-dark btn-sm">Download</button>
          </td>
        </tr>
      </tbody>

    </table>
  </div>


</template>

<script>
import Navbar from '../components/UserNavbar.vue'
import RateForm from '../components/RateForm.vue'
export default {
  name: 'UserEbooks',
  components: {
    Navbar,
    RateForm
  },
  data() {
    return {
      rateFormVisibleIssued: [],
      rateFormVisiblePurchased: [],
      task_id: '',
    }
  },

  computed: {
    associations() {
      return this.$store.state.user_associations;
    },
    issued_associations() {
      return this.associations.filter(association => association.request_status === 'issued');
    },
    purchased_associations() {
      return this.associations.filter(association => association.request_status === 'purchased');
    }
  },

  methods: {

    formateDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('en', options);
    },

    toggleForm(index, type) {
      if (type === 'issued') {
        this.rateFormVisibleIssued[index] = !this.rateFormVisibleIssued[index];
      } else if (type === 'purchased') {
        this.rateFormVisiblePurchased[index] = !this.rateFormVisiblePurchased[index];
      }

    },

    async returnEbook(user_id, ebook_id) {
      try {
        const url = "http://127.0.0.1:5000/api/return-ebook/" + user_id + "/" + ebook_id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token
          }
        });
        if (response.ok) {
          console.log("Ebook returned successfully");
          this.$store.dispatch("getUserAssociations")
        } else {
          const errorData = await response.json();
          console.log(errorData.message);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async submitRating(user_id, ebook_id, rating) {
      // send the rating to the backend
      try {
        const url = "http://127.0.0.1:5000/api/rate-ebook/" + user_id + "/" + ebook_id;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-token": this.$store.state.token
          },
          body: JSON.stringify({ rating: rating })
        });
        // console.log(rating);
        if (response.ok) {
          console.log("Rating submitted successfully");
          this.$store.dispatch("getUserAssociations");
          // reset the form visibility
          this.rateFormVisibleIssued = new Array(this.issued_associations.length).fill(false);
          this.rateFormVisiblePurchased = new Array(this.purchased_associations.length).fill(false);
        } else {
          const errorData = await response.json();
          console.log(errorData.message);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async downloadEbook(ebook_id, ebook_name) {
      try {
        const url = "http://127.0.0.1:5000/create-pdf/" + ebook_id;
        const response = await fetch(url, {
          headers: {
            "Authentication-token": this.$store.state.token
          }
        });
        const data = await response.json();
        this.task_id = data.task_id;
        // Fixed interval polling
        const interval = setInterval(async () => {
          try {
            const url = "http://127.0.0.1:5000/download-pdf/" + this.task_id;
            const response = await fetch(url, {
              headers: {
                "Authentication-token": this.$store.state.token
              }
            });
            if (!response.ok) {
              const errorData = await response.json();
              console.log(errorData.message);
            } else {
              const pdf = await response.blob();
              const pdfUrl = URL.createObjectURL(pdf);
              const link = document.createElement("a");
              link.href = pdfUrl;
              link.download = ebook_name + ".pdf";
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              clearInterval(interval);
              alert("File Downloaded");
            }
          } catch (error) {
            console.error(error);
          }
        }, 1000);
      } catch (error) {
        console.error(error);
      }
    },
  },
  async mounted() {
    // get the associations
    this.$store.dispatch("getUserAssociations");
    // initialize the rate-form visibility
    this.rateFormVisibleIssued = new Array(this.issued_associations.length).fill(false);
    this.rateFormVisiblePurchased = new Array(this.purchased_associations.length).fill(false);
  }
}
</script>