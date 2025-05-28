<template>
    <Navbar />
    <div class="container mt-3">
        <h2 class="mb-4">Payment</h2>
        <form @submit.prevent="buyEbook">
            <div class="mb-3">
                <label for="card_number" class="form-label">Card Number</label>
                <input type="text" class="form-control" id="card_number" name="card_number" required>
            </div>
            <div class="mb-3">
                <label for="expiry_date" class="form-label">Expiry Date</label>
                <input type="text" class="form-control" id="expiry_date" name="expiry_date" placeholder="MM/YY"
                    required>
            </div>
            <div class="mb-3">
                <label for="cvv" class="form-label">CVV</label>
                <input type="text" class="form-control" id="cvv" name="cvv" required>
            </div>
            <div class="mb-3">
                <label for="name_on_card" class="form-label">Name on Card</label>
                <input type="text" class="form-control" id="name_on_card" name="name_on_card" required>
            </div>
            <div class="mb-3">
                <label for="price" class="form-label">Price</label>
                <input type="text" class="form-control" id="price" name="price" :value="price" readonly="true">
            </div>
            <button type="submit" class="btn btn-success">Submit Payment</button>
        </form>
    </div>

</template>

<script>
import Navbar from '../components/UserNavbar.vue'
export default {
    name: 'BuyEbook',

    data() {
        return {
            price: 0
        }
    },
    components: {
        Navbar
    },

    methods: {
        async buyEbook() {
            try {
                const url = "http://127.0.0.1:5000/api/buy-ebook/" + this.$store.state.id + "/" + this.$route.params.ebook_id;
                const response = await fetch(url, {
                    headers: {
                        "Authentication-token": this.$store.state.token
                    },
                });
                const data = await response.json();
                console.log(data);
                this.$router.push('/user/ebooks');
            } catch (error) {
                console.log(error);
            }
        },

        async getPrice() {
            try {
                const url = "http://127.0.0.1:5000/api/ebooks/" + this.$route.params.ebook_id;
                const response = await fetch(url, {
                    headers: {
                        "Authentication-token": this.$store.state.token
                    }
                });
                const data = await response.json();
                this.price = data.price;
            } catch (error) {
                console.log(error);
            }
        }
    },
    mounted() {
        this.getPrice();
    }
}
</script>