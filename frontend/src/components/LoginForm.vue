<template>
  <form @submit.prevent="handleSubmit" class="login-form">
    <div class="form-group">
      <label for="username">ユーザー名:</label>
      <input type="text" id="username" v-model="username" required>
    </div>
    <div class="form-group">
      <label for="password">パスワード:</label>
      <input type="password" id="password" v-model="password" required>
    </div>
    <button type="submit" class="submit-button">ログイン</button>
    <p v-if="error" class="error-message">{{ error }}</p>
  </form>
</template>

<script>
import AuthService from '@/services/auth.service';

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      error: null
    };
  },
  methods: {
    async handleSubmit() {
      this.error = null;
      try {
        await AuthService.login(this.username, this.password);
        this.$router.push('/'); // ログイン成功後にホームにリダイレクト
      } catch (err) {
        this.error = err;
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  width: 100%;
  max-width: 400px; /* フォームの最大幅 */
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #007bff;
  outline: none;
}

.submit-button {
  background-color: #007bff;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 10px;
}
</style>

