<template>
    <Navbar />
    <div class="container mt-5">
        <form @submit.prevent="addEbook">
            <div class="form-group mb-3">
                <label for="name">Ebook Name</label>
                <input v-model="ebook.name" type="text" class="form-control" id="name" placeholder="Enter the name"
                    required>
            </div>
            <div class="form-group mb-3">
                <label for="authors">Authors</label>
                <input v-model="ebook.authors" type="text" class="form-control" id="authors"
                    placeholder="Enter the authors" required>
            </div>
            <div class="form-group mb-3">
                <label for="content">Content</label>
                <textarea v-model="ebook.content" class="form-control" id="content"
                    placeholder="Enter the content"></textarea>
            </div>
            <div class="form-group mb-3">
                <label for="price">Price</label>
                <input v-model="ebook.price" type="number" class="form-control" id="price" required>
            </div>
            <div class="form-group mb-3">
                <label for="acess_duration">Access Duration (days)</label>
                <input v-model="ebook.acces_duration" type="number" class="form-control" id="acess_duration">
            </div>
            <div class="btn-container">
            <button type="submit" class="btn btn-add">Add Book</button>
            <button @click="cancelForm" class="btn btn-cancel">Cancel</button>
        </div>
        </form>
    </div>
</template>

<script>
import Navbar from '../components/AdminNavbar.vue'
export default {
    name: "AddEbook",
    components: {
        Navbar
    },
    data() {
        return {
            ebook: {
                name: "",
                authors: "",
                content: "",
                price: 400,
                section_id: this.$route.params.section_id,
                acces_duration: 7
            },
        }
    },
    methods: {
        async addEbook() {
            try {
                const url = "http://127.0.0.1:5000/api/ebooks";
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        "Authentication-Token": this.$store.state.token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.ebook),
                    credentials: 'same-origin',
                });
                if (response.ok) {
                    console.log('Ebook added successfully');
                    this.$router.push('/admin/ebooks');
                } else {
                    const errorData = await response.json();
                    alert(errorData.message);
                }
            } catch (error) {
                console.error('error while adding ebook', error);
            }
        },
        cancelForm() {
            this.$router.push('/admin/ebooks');
        },
    },
}
</script>
