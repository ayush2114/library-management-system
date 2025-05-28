<template>
    <Navbar />
    <div class="container mt-5">
        <form @submit.prevent="updateSection">
            <div class="form-group mb-3">
                <label for="name">Name</label>
                <input v-model="section.name" type="text" class="form-control" id="name" placeholder="Enter the name"
                    required>
            </div>
            <div class="form-group mb-3">
                <label for="description">Description</label>
                <textarea v-model="section.description" class="form-control" id="description"
                    placeholder="Enter the description"></textarea>
            </div>
            <div class="btn-container">
            <button type="submit" class="btn btn-add">Update Section</button>
            <button @click="cancelForm" class="btn btn-cancel">Cancel</button>
        </div>
        </form>
    </div>
</template>

<script>
import Navbar from '../components/AdminNavbar.vue'
export default {
    name: "UpdateSection",
    data() {
        return {
            section: {
                name: "",
                description: ""
            }
        }
    },
    components: {
        Navbar
    },
    methods: {
        async updateSection() {
            try {
                const url = "http://127.0.0.1:5000/api/sections/" + this.$route.params.section_id;
                const response = await fetch(url, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-token": this.$store.state.token
                    },
                    body: JSON.stringify(this.section)
                });
                if (response.ok) {
                    console.log("Section updated successfully");
                    this.$router.push('/admin/ebooks');
                } else {
                    const errorData = await response.json();
                    alert(errorData.message);
                }
            } catch (error) {
                console.error('error updating section', error);
            }
        },
        cancelForm() {
            this.$router.push('/admin/ebooks');
        },
    },
    async mounted() {
        try {
            const url = "http://127.0.0.1:5000/api/sections/" + this.$route.params.section_id;
            const response = await fetch(url, {
                headers: {
                    "Authentication-token": this.$store.state.token
                }
            });
            const data = await response.json();
            this.section = data;
        } catch (error) {
            console.log(error);
        }
    }
}
</script>