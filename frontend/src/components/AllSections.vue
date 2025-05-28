<template>
    <div class="card">
        <div class="card-body">
            <h4 class="card-title">{{ section.name }}</h4>
            <h6 class="card-subtitle mb-2 text-muted">Date Created: {{ formatDate(section.date_created) }}</h6>
            <h6 class="card-subtitle mb-2 text-muted">Total Books: {{ section.total_ebooks }}</h6>
            <p class="card-text">{{ section.description }}</p>
        </div>
        <div class="card-body d-flex justify-content-between">
            <router-link :to="{ name: 'AddEbook', params: { section_id: section.id } }" class="btn btn-link">Add Book</router-link>
            <router-link :to="{ name: 'UpdateSection', params: { section_id: section.id } }" class="btn btn-link">Update</router-link>
            <button @click="deleteSection" class="btn btn-link">Delete</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AllSections',
    props: {
        section: Object,
    },
    methods: {
        formatDate(date) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(date).toLocaleDateString('en', options);
        },

        deleteSection() {
            this.$store.dispatch('deleteSection', this.section.id)
        },
    }
}
</script>

<style scoped>

.card-title {
    font-weight: bold;
}
</style>