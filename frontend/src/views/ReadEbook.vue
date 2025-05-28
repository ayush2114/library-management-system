<template>
<div class="container mt-5">
    <div class="card">
        <div class="card-header">
            <h1 class="card-title text-center">{{ ebook.name }}</h1>
            <h4 class="card-subtitle mb-2 text-muted text-center">Authors: {{ ebook.authors }}</h4>
        </div>
        <div class="card-body">
            {{ ebook.content }}
        </div>
        <div class="card-footer">
            <router-link to="/user/ebooks" class="btn btn-secondary btn-sm">Back</router-link>
        </div>
    </div>
</div>

</template>

<script>
export default {
    name: 'ReadEbook',
    data() {
        return {
            ebook: ''
        }
    },
    methods: {
        async getEbook(ebook_id) {
            try {
                const url = "http://127.0.0.1:5000/api/ebooks/" + ebook_id;
                const response = await fetch(url, {
                    headers: {
                        "Authentication-token": this.$store.state.token
                    }
                });
                const data = await response.json();
                this.ebook = data;
            } catch (error) {
                console.error('error while getting ebook', error);
            }
        }
    },
    mounted() {
        this.getEbook(this.$route.params.ebook_id)
    }
}
</script>