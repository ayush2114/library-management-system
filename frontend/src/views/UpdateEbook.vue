<template>
    <Navbar />
    <div class="container mt-5">
        <form @submit.prevent="updateEbook">

            <div class="form-group mb-3">
                <label for="title">Title</label>
                <input v-model="ebook.name" type="text" class="form-control" id="title" required>
            </div>
            <div class="form-group mb-3">
                <label for="authors">Authors</label>
                <input v-model="ebook.authors" type="text" class="form-control" id="authors" required>
            </div>
            <div class="form-group mb-3">
                <label for="content">Content</label>
                <textarea v-model="ebook.content" class="form-control" id="content"></textarea>
            </div>
            <div class="form-group mb-3">
                <label for="price">Price</label>
                <input v-model="ebook.price" type="number" class="form-control" id="price" required>
            </div>
            <div class="form-group mb-3">
                <label for="acess_duration">Access Duration (days)</label>
                <input v-model="ebook.acces_duration" type="number" class="form-control" id="acess_duration">
            </div>
            <div class="form-group mb-3">
                <label for="section_id">Section</label>
                <select v-model="ebook.section_id" class="form-control" id="section_id" required>
                    <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}
                    </option>
                </select>
            </div>
            <div class="btn-container">
                <button type="submit" class="btn btn-add">Update Book</button>
                <button @click="cancelForm" class="btn btn-cancel">Cancel</button>
            </div>
        </form>
    </div>
</template>

<script>
import Navbar from '../components/AdminNavbar.vue'
export default {
    name: "UpdateEbook",
    components: {
        Navbar
    },

    data() {
        return {
            ebook: '',
        }
    },
    computed: {
        sections() {
            return this.$store.state.sections
        }
    },

    async mounted() {
        this.getEbook(this.$route.params.ebook_id);
        this.$store.dispatch('getSections');
    },

    methods: {

        async updateEbook() {
            try {
                const url = "http://127.0.0.1:5000/api/ebooks/" + this.$route.params.ebook_id;
                const response = await fetch(url, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-token": this.$store.state.token
                    },
                    body: JSON.stringify(this.ebook)
                });
                if (response.ok) {
                    console.log("Ebook updated successfully");
                    this.$router.push('/admin/ebooks');
                } else {
                    const errorData = await response.json();
                    alert(errorData.message);
                }
            } catch (error) {
                console.error('error updating ebook', error);
            }
        },

        async getEbook(ebook_id) {
            try {
                const url = "http://127.0.0.1:5000/api/ebooks/" + ebook_id;
                const response = await fetch(url, {
                    headers: {
                        "Authentication-token": this.$store.state.token
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    this.ebook = data;
                } else {
                    const errorData = await response.json();
                    console.log(errorData.message);
                }
            } catch (error) {
                console.error('error getting ebook', error);
            }
        },

        cancelForm() {
            this.$router.push('/admin/ebooks');
        }
    }
}
</script>

<style scoped>
</style>