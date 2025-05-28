<template>
    <div class="signup-container">
        <form @submit.prevent="signup" class="signup-form">
            <h2>Create Account</h2>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input v-model="email" type="email" id="email" placeholder="Enter your email" class="form-control"
                    required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input v-model="password" type="password" id="password" placeholder="Enter your password"
                    class="form-control" required>
            </div>
            <button type="submit" class="btn">Signup</button>
        </form>
        <div class="signin-container">
            <p>Already have an account?</p>
            <router-link class="signin-link" to="/login">Sign in</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SignupView',
    data() {
        return {
            email: "",
            password: ""
        }
    },

    methods: {
        async signup() {
            try {
                const url = "http://127.0.0.1:5000" + '/api/signup'

                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    }),
                    credentials: 'same-origin',
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    this.$router.push('/login');
                } else {
                    const error_data = await response.json();
                    alert(error_data.message);
                }

            } catch (error) {
                console.log(error);
            }
        }
    }
}
</script>

<style scoped>
.signup-container {
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.signup-form {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 400px;
}

.signup-form h2 {
  text-align: center;
  color: #333;
}


.btn {
  width: 100%;
  background-color: #6a11cb;
  color: white;
  border-radius: 4px;
  font-size: 16px;
}

.btn:hover {
  background-color: #2575fc;
}

.btn:active {
  transform: scale(0.98);
}

.signin-container {
  margin-top: 20px;
  text-align: center;
}

.signin-link {
  color: #6a11cb;
  text-decoration: none;
}

.signin-link:hover {
  color: #2575fc;
}
</style>
