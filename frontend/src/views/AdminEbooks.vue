<template>
  <Navbar />
  <div class="container mt-5">
    <h2 class="mb-5">All Sections in Library</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="section in sections" :key="section.id">
        <Sections :section="section"></Sections>
      </div>
      <div class="col">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">Add new section</h5>
            <p class="card-text">Click the button below to add a new section to the library.</p>
            <router-link to="/admin/add-section" class="btn btn-primary">Add Section</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container mt-5">
    <h2 class="mb-3">All Books in Library</h2>
    <p v-if="ebooks.length == 0"> No books in the library.</p>
    <table v-else class="table table-hover">
      <thead>
        <tr class="table-primary">
          <th scope="col">S.No</th>
          <th scope="col">Title</th>
          <th scope="col">Author</th>
          <th scope="col">Section</th>
          <th scope="col"></th>
          <!-- <th scope="col"></th> -->
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ebook, index) in ebooks" :key="ebook.id">
          <Ebooks :ebook="ebook" :index="index + 1"></Ebooks>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import Navbar from '../components/AdminNavbar.vue';
import Sections from '@/components/AllSections.vue';
import Ebooks from '@/components/AllEbooks.vue';
export default {
  name: 'AdminEbooks',
  components: {
    Navbar,
    Sections,
    Ebooks
  },

  computed: {
    ...mapState(['ebooks', 'sections'])
  },

  created() {
    this.getEbooks();
    this.getSections();
  },

  methods: {
    ...mapActions(['getSections', 'getEbooks']),
  },
}
</script>
