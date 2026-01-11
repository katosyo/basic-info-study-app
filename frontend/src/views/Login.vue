<template>
  <div class="login-page">
    <h1>ログイン</h1>
    <LoginForm />
    <p>アカウントをお持ちでない方は<router-link to="/register">こちら</router-link>から登録してください。</p>
    <p class="quiz-link">または、<router-link to="/question-selection">問題を解く</router-link>ページに直接アクセスすることもできます。</p>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue';

export default {
  name: 'LoginPage',
  components: {
    LoginForm
  }
}
</script>

<style scoped>
.login-page {
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

p {
  margin-top: 20px;
}

.quiz-link {
  margin-top: 30px;
  font-size: 1.1rem;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>

