<template>
  <div class="signin-container">
    <form class="form" @submit.prevent="login">
      <h2>Login</h2>
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input v-model="email" type="text" class="form-control" id="email" aria-describedby="emailHelp"
          placeholder="Enter your email" required>
        <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" id="password" placeholder="Enter your password"
          required>
      </div>
      <button type="submit" class="btn">Login</button>
    </form>
    <div class="signup-container">
      <p>Don't have an account?</p>
      <router-link class="signup-link" to="/signup">Create an account</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
    }
  },

  methods: {

    async login() {

      try {

        const url = "http://127.0.0.1:5000" + '/api/login'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        if (response.ok) {
          const data = await response.json();
          this.$store.dispatch('login', data)
          if (data.role === 'admin') {
            this.$router.push('/admin/dashboard')
          } else {
            this.$router.push('/user/dashboard')
          }
        } else {
          const error_data = await response.json()
          alert(error_data.message)
        }

      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>

<style scoped>
.signin-container {
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 400px;
}

.form h2 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
}

.form-text {
  margin-top: 10px;
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

.signup-container {
  margin-top: 20px;
  text-align: center;
}

.signup-link {
  color: #6a11cb;
  text-decoration: none;
}

.signup-link:hover {
  color: #2575fc;
}
</style>