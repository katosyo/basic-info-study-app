<template>
  <div class="home">
    <h1 v-if="!isLoggedIn">ようこそ、基本情報勉強アプリへ！</h1>
    <h1 v-else>学習を続けましょう！</h1>
    <p v-if="!isLoggedIn">学習を始めるには、ログインまたは新規登録してください。</p>
    
    <!-- ローディング表示 -->
    <div v-if="isLoggedIn && loading" class="loading-message">
      統計情報を読み込み中...
    </div>
    
    <!-- ログイン時の統計情報ダッシュボード -->
    <div v-if="isLoggedIn && statistics" class="dashboard">
      <div class="stats-grid">
        <!-- 連続学習日数 -->
        <div class="stat-card streak-card">
          <div class="stat-icon">🔥</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.consecutive_days }}</div>
            <div class="stat-label">連続学習日数</div>
          </div>
        </div>
        
        <!-- 今日の学習 -->
        <div class="stat-card today-card">
          <div class="stat-icon">📅</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.today_answers }}</div>
            <div class="stat-label">今日解いた問題</div>
            <div class="stat-sub" v-if="statistics.today_answers > 0">
              正答率: {{ statistics.today_accuracy }}%
            </div>
          </div>
        </div>
        
        <!-- 総解答数 -->
        <div class="stat-card total-card">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.total_answers }}</div>
            <div class="stat-label">総解答数</div>
            <div class="stat-sub">
              正答率: {{ statistics.average_accuracy }}%
            </div>
          </div>
        </div>
        
        <!-- 学習進捗 -->
        <div class="stat-card progress-card">
          <div class="stat-icon">📈</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.unique_questions }}/{{ statistics.total_questions }}</div>
            <div class="stat-label">学習した問題</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: statistics.progress_percentage + '%' }"></div>
            </div>
            <div class="stat-sub">{{ statistics.progress_percentage }}% 完了</div>
          </div>
        </div>
      </div>
      
      <!-- カテゴリ別統計 -->
      <div v-if="statistics.category_stats && Object.keys(statistics.category_stats).length > 0" class="category-stats">
        <h3>カテゴリ別正答率</h3>
        <div class="category-list">
          <div 
            v-for="(stats, category) in statistics.category_stats" 
            :key="category"
            class="category-item"
          >
            <div class="category-name">{{ category }}</div>
            <div class="category-progress">
              <div class="category-progress-bar">
                <div 
                  class="category-progress-fill" 
                  :style="{ width: stats.accuracy + '%' }"
                  :class="{ 'high': stats.accuracy >= 80, 'medium': stats.accuracy >= 60 && stats.accuracy < 80, 'low': stats.accuracy < 60 }"
                ></div>
              </div>
              <div class="category-accuracy">{{ stats.accuracy }}%</div>
            </div>
            <div class="category-count">{{ stats.correct }}/{{ stats.total }}</div>
          </div>
        </div>
      </div>
      
    </div>
    
    <!-- メインアクション -->
    <div class="main-actions">
      <router-link to="/question-selection" class="action-card">
        <div class="card-icon">📝</div>
        <h2>問題を解く</h2>
        <p>問題を選択して学習を開始します</p>
      </router-link>
      <router-link to="/answer-history" class="action-card">
        <div class="card-icon">📊</div>
        <h2>回答履歴</h2>
        <p>これまで解いた問題の履歴を確認します</p>
      </router-link>
      <router-link to="/study-materials" class="action-card">
        <div class="card-icon">📚</div>
        <h2>対策問題集</h2>
        <p>間違えた問題から対策問題集を作成します</p>
      </router-link>
    </div>
    
    <div v-if="!isLoggedIn" class="auth-actions">
      <router-link to="/login" class="btn btn-primary">ログイン</router-link>
      <router-link to="/register" class="btn btn-secondary">新規登録</router-link>
    </div>
  </div>
</template>

<script>
import QuestionService from '@/services/question.service';

export default {
  name: 'HomePage',
  data() {
    return {
      isLoggedIn: false,
      statistics: null,
      loading: false
    };
  },
  created() {
    this.checkLoginStatus();
    if (this.isLoggedIn) {
      this.loadStatistics();
    }
  },
  watch: {
    $route: 'checkLoginStatus',
    isLoggedIn(newVal) {
      if (newVal) {
        this.loadStatistics();
      } else {
        this.statistics = null;
      }
    }
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('user');
    },
    async loadStatistics() {
      if (!this.isLoggedIn) {
        console.log('Not logged in, skipping statistics load');
        return;
      }
      
      const userId = QuestionService.getUserId();
      console.log('Loading statistics for user ID:', userId);
      if (!userId) {
        console.log('No user ID found');
        return;
      }
      
      this.loading = true;
      try {
        console.log('Fetching statistics...');
        this.statistics = await QuestionService.getUserStatistics(userId);
        console.log('Statistics loaded:', this.statistics);
      } catch (error) {
        console.error('Error loading statistics:', error);
        console.error('Error details:', error.response || error.message);
        // エラー時でも空の統計情報を設定して表示を試みる
        this.statistics = {
          total_answers: 0,
          total_correct: 0,
          total_incorrect: 0,
          average_accuracy: 0,
          today_answers: 0,
          today_correct: 0,
          today_accuracy: 0,
          week_answers: 0,
          week_correct: 0,
          week_accuracy: 0,
          consecutive_days: 0,
          unique_questions: 0,
          total_questions: 500,
          progress_percentage: 0,
          category_stats: {}
        };
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px); /* ヘッダーとフッターの高さを考慮 */
  padding: 40px 20px;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #333;
  margin-bottom: 20px;
  font-size: 2.5rem;
}

p {
  color: #666;
  margin-bottom: 40px;
  font-size: 1.2rem;
}

.main-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  width: 100%;
  margin-bottom: 40px;
}

.action-card {
  background-color: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 30px 20px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.action-card h2 {
  color: #333;
  margin: 15px 0 10px 0;
  font-size: 1.5rem;
}

.action-card p {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 10px;
}

.auth-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.btn {
  padding: 12px 25px;
  border-radius: 5px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: 1px solid #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-secondary {
  background-color: #f8f9fa;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-secondary:hover {
  background-color: #e2e6ea;
  border-color: #0056b3;
}

/* ダッシュボード */
.dashboard {
  width: 100%;
  margin-bottom: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.stat-content {
  flex-grow: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-sub {
  font-size: 0.85rem;
  color: #888;
}

.streak-card {
  border-left: 4px solid #ff6b35;
  background: linear-gradient(135deg, #fff5f0 0%, #ffffff 100%);
}

.today-card {
  border-left: 4px solid #4ecdc4;
  background: linear-gradient(135deg, #f0fffe 0%, #ffffff 100%);
}

.total-card {
  border-left: 4px solid #007bff;
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
}

.progress-card {
  border-left: 4px solid #28a745;
  background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin: 8px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
  transition: width 0.3s ease;
}

/* カテゴリ別統計 */
.category-stats {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.category-stats h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3rem;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.category-name {
  font-weight: bold;
  color: #333;
  min-width: 120px;
  font-size: 0.95rem;
}

.category-progress {
  flex-grow: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-progress-bar {
  flex-grow: 1;
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
}

.category-progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 5px;
}

.category-progress-fill.high {
  background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
}

.category-progress-fill.medium {
  background: linear-gradient(90deg, #ffc107 0%, #ff9800 100%);
}

.category-progress-fill.low {
  background: linear-gradient(90deg, #dc3545 0%, #e91e63 100%);
}

.category-accuracy {
  font-weight: bold;
  color: #333;
  min-width: 50px;
  text-align: right;
  font-size: 0.9rem;
}

.category-count {
  font-size: 0.85rem;
  color: #666;
  min-width: 60px;
  text-align: right;
}


.loading-message {
  padding: 20px;
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* レスポンシブデザイン */
/* タブレット用 (768px - 1024px) */
@media (max-width: 1024px) and (min-width: 769px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .main-actions {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .stat-card {
    padding: 18px;
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
  
  .category-stats {
    padding: 20px;
  }
}

/* スマホ・タブレット用 (768px以下) */
@media (max-width: 768px) {
  .home {
    padding: 20px 15px;
    min-height: calc(100vh - 100px);
  }
  
  h1 {
    font-size: 1.8rem;
    margin-bottom: 15px;
  }
  
  p {
    font-size: 1rem;
    margin-bottom: 25px;
  }
  
  .dashboard {
    margin-bottom: 25px;
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .stat-card {
    padding: 15px;
    gap: 12px;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .stat-value {
    font-size: 1.6rem;
    margin-bottom: 3px;
  }
  
  .stat-label {
    font-size: 0.85rem;
    margin-bottom: 3px;
  }
  
  .stat-sub {
    font-size: 0.8rem;
  }
  
  .category-stats {
    padding: 15px;
    margin-bottom: 20px;
  }
  
  .category-stats h3 {
    font-size: 1.1rem;
    margin-bottom: 15px;
  }
  
  .category-list {
    gap: 12px;
  }
  
  .category-item {
    padding: 10px;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  .category-name {
    min-width: 100px;
    font-size: 0.9rem;
    width: 100%;
  }
  
  .category-progress {
    width: 100%;
    gap: 8px;
  }
  
  .category-progress-bar {
    height: 8px;
  }
  
  .category-accuracy {
    min-width: 45px;
    font-size: 0.85rem;
  }
  
  .category-count {
    min-width: 55px;
    font-size: 0.8rem;
    width: 100%;
    text-align: left;
    margin-top: 5px;
  }
  
  .main-actions {
    grid-template-columns: 1fr;
    gap: 15px;
    margin-bottom: 25px;
  }
  
  .action-card {
    padding: 20px 15px;
  }
  
  .action-card h2 {
    font-size: 1.3rem;
    margin: 12px 0 8px 0;
  }
  
  .action-card p {
    font-size: 0.9rem;
    margin: 0;
  }
  
  .card-icon {
    font-size: 2.5rem;
    margin-bottom: 8px;
  }
  
  .auth-actions {
    flex-direction: column;
    width: 100%;
    max-width: 300px;
    gap: 10px;
  }
  
  .btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1rem;
  }
  
  .progress-bar {
    height: 6px;
    margin: 6px 0;
  }
}

/* 小さなスマホ用 (480px以下) */
@media (max-width: 480px) {
  .home {
    padding: 15px 10px;
  }
  
  h1 {
    font-size: 1.5rem;
    margin-bottom: 12px;
  }
  
  p {
    font-size: 0.95rem;
    margin-bottom: 20px;
  }
  
  .stat-card {
    padding: 12px;
    gap: 10px;
  }
  
  .stat-icon {
    font-size: 1.8rem;
  }
  
  .stat-value {
    font-size: 1.4rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .stat-sub {
    font-size: 0.75rem;
  }
  
  .category-stats {
    padding: 12px;
  }
  
  .category-stats h3 {
    font-size: 1rem;
  }
  
  .category-name {
    font-size: 0.85rem;
  }
  
  .action-card {
    padding: 18px 12px;
  }
  
  .action-card h2 {
    font-size: 1.2rem;
  }
  
  .card-icon {
    font-size: 2.2rem;
  }
}
</style>

