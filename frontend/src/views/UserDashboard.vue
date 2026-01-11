<template>
  <div class="user-dashboard">
    <h1>ユーザー管理画面</h1>
    
    <div class="dashboard-content">
      <div class="user-info">
        <h2>ユーザー情報</h2>
        <p v-if="userInfo">ユーザー名: {{ userInfo.username }}</p>
        <p v-else>ユーザー情報を読み込み中...</p>
      </div>

      <div class="dashboard-actions">
        <router-link to="/answer-history" class="action-button">
          解答履歴を見る
        </router-link>
        <router-link to="/study-materials" class="action-button">
          対策問題集・ノートを作成
        </router-link>
        <router-link to="/question-selection" class="action-button">
          問題を解く
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserDashboard',
  data() {
    return {
      userInfo: null
    };
  },
  created() {
    this.loadUserInfo();
  },
  methods: {
    loadUserInfo() {
      const user = localStorage.getItem('user');
      if (user) {
        try {
          this.userInfo = JSON.parse(user);
        } catch (e) {
          console.error('Error parsing user info:', e);
        }
      }
    }
  }
};
</script>

<style scoped>
.user-dashboard {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}

h1 {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.dashboard-content {
  background-color: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: white;
  border-radius: 5px;
}

.user-info h2 {
  color: #007bff;
  margin-bottom: 1rem;
}

.dashboard-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-button {
  display: block;
  padding: 1rem;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  text-align: center;
  font-weight: 500;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #0056b3;
}
</style>

