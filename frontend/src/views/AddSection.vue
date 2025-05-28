<template>
    <Navbar />
    <div class="container mt-5">
        <form @submit.prevent="addSection">
            <div class="form-group mb-3">
                <label for="name">Section Name</label>
                <input v-model="section.name" type="text" class="form-control" id="name" placeholder="Enter the name"
                    required>
            </div>
            <div class="form-group mb-3">
                <label for="description">Description</label>
                <textarea v-model="section.description" class="form-control" id="description"
                    placeholder="Enter the description"></textarea>
            </div>
            <div class="btn-container">
                <button type="submit" class="btn btn-add">Add Section</button>
                <button @click="cancelForm" class="btn btn-cancel">Cancel</button>
            </div>
        </form>
    </div>
</template>

<script>
import Navbar from '../components/AdminNavbar.vue'
export default {
    name: "AddSection",
    components: {
        Navbar
    },
    data() {
        return {
            section: {
                name: '',
                description: '',
            },
        }
    },
    methods: {
        async addSection() {
            try {
                const url = "http://127.0.0.1:5000/api/sections";
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        "Authentication-token": this.$store.state.token
                    },
                    body: JSON.stringify(this.section),
                    credentials: 'same-origin',
                });
                if (response.ok) {
                    console.log('Section added successfully');
                    this.$router.push('/admin/ebooks');
                } else {
                    const errorData = await response.json();
                    alert(errorData.message);
                }
            } catch (error) {
                console.error('error while adding section', error);
            }
        },

        cancelForm() {
            this.$router.push('/admin/ebooks');
        }

    },
}
</script>