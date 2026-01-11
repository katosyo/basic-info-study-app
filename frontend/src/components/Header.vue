<template>
  <header class="app-header">
    <div class="header-content">
      <!-- 左端: ロゴ -->
      <div class="logo-section">
        <router-link to="/" class="logo-link">
          <span class="logo-text">基本情報勉強アプリ</span>
        </router-link>
      </div>

      <!-- 右端: ユーザーアイコンとログイン/ログアウト -->
      <div class="user-section">
        <router-link 
          v-if="isLoggedIn" 
          to="/user-dashboard" 
          class="user-icon-link"
          title="ユーザー管理画面"
        >
          <svg class="user-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </router-link>
        <button 
          v-if="isLoggedIn" 
          @click="logout" 
          class="logout-button"
        >
          ログアウト
        </button>
        <template v-else>
          <router-link to="/register" class="signup-button">
            サインアップ
          </router-link>
          <router-link to="/login" class="login-button">
            ログイン
          </router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      isLoggedIn: false,
    };
  },
  created() {
    this.checkLoginStatus();
  },
  watch: {
    $route: 'checkLoginStatus'
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('user');
    },
    logout() {
      localStorage.removeItem('user');
      this.isLoggedIn = false;
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.app-header {
  background-color: #007bff;
  color: white;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}

.logo-section {
  flex: 0 0 auto;
}

.logo-link {
  text-decoration: none;
  color: white;
  display: flex;
  align-items: center;
  transition: opacity 0.2s;
}

.logo-link:hover {
  opacity: 0.8;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-icon-link {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.user-icon-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-icon {
  width: 24px;
  height: 24px;
}

.signup-button,
.login-button,
.logout-button {
  padding: 0.5rem 1rem;
  border-radius: 5px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.signup-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.signup-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.login-button {
  background-color: white;
  color: #007bff;
}

.login-button:hover {
  background-color: #f0f0f0;
}

.logout-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>

