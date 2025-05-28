<template>
    <th>{{ index }}</th>
    <td>{{ ebook.name }}</td>
    <td>{{ ebook.authors }}</td>
    <td>{{ ebook.section_name }}</td>
    <!-- <td><button class="btn btn-outline-secondary">Details</button></td> -->
    <td><router-link :to="{ name: 'UpdateEbook', params: { ebook_id: ebook.id } }" class="btn btn-link">Update</router-link></td>
    <td><button @click="deleteEbook" class="btn btn-link">Delete</button></td>
</template>

<script>
export default {
  name: 'AllEbooks',

  props: {
    ebook: Object,
    index: Number
  },

  methods: {
    deleteEbook() {
      this.$store.dispatch('deleteEbook', this.ebook.id)
    }
  },

  emits: ['delete-ebook']
}
</script>
