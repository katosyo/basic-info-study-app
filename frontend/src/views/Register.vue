<template>
  <div class="register-page">
    <h1>ユーザー登録</h1>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label for="username">ユーザー名:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="email">メールアドレス:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">パスワード:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="submit-button">登録</button>
      <p v-if="error" class="error-message">{{ error }}</p>
      <p v-if="message" class="success-message">{{ message }}</p>
    </form>
    <p>すでにアカウントをお持ちの方は<router-link to="/login">こちら</router-link>からログインしてください。</p>
  </div>
</template>

<script>
import AuthService from '@/services/auth.service';

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: null,
      message: null
    };
  },
  methods: {
    async handleRegister() {
      this.error = null;
      this.message = null;
      try {
        const response = await AuthService.register(this.username, this.email, this.password);
        this.message = response.message || '登録が完了しました！';
        // 登録成功後、ログインページにリダイレクトすることも検討
        this.$router.push('/login');
      } catch (err) {
        this.error = err;
      }
    }
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px); /* ヘッダーの高さなどを考慮 */
  padding: 20px;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.register-form {
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
input[type="email"],
input[type="password"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus {
  border-color: #007bff;
  outline: none;
}

.submit-button {
  background-color: #28a745; /* 緑系の色 */
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #218838;
}

p {
  margin-top: 20px;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 10px;
}

.success-message {
  color: #28a745;
  text-align: center;
  margin-top: 10px;
}
</style>

