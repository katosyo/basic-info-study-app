<template>
  <div class="answer-history">
    <h1>解答履歴</h1>
    
    <div class="history-controls">
      <div class="sort-controls">
        <label>並び替え:</label>
        <select v-model="sortBy" @change="sortHistory" class="sort-select">
          <option value="timestamp">解答日時</option>
          <option value="question_id">問題番号</option>
          <option value="category">ジャンル</option>
          <option value="accuracy">正答率</option>
        </select>
        <button 
          @click="toggleSortOrder" 
          class="sort-order-button"
          :title="sortOrder === 'desc' ? '降順（新しい順）' : '昇順（古い順）'"
        >
          {{ sortOrder === 'desc' ? '↓' : '↑' }}
        </button>
        <span class="sort-info">{{ getSortLabel() }}</span>
      </div>
    </div>

    <div v-if="loading" class="loading">読み込み中...</div>
    <div v-else-if="history.length === 0" class="no-data">
      解答履歴がありません。
    </div>
    <div v-else class="history-list">
      <div 
        v-for="(item, index) in sortedHistory" 
        :key="index" 
        class="history-item"
        :class="{ 'correct': item.is_correct, 'incorrect': !item.is_correct }"
        @click="showQuestionDetail(item.question_id)"
      >
        <div class="item-header">
          <span 
            class="question-id clickable" 
            @click.stop="setSort('question_id')"
            :title="sortBy === 'question_id' ? 'クリックでソート' : 'クリックで問題番号でソート'"
          >
            問題ID: {{ item.question_id }}
            <span v-if="sortBy === 'question_id'" class="sort-indicator">
              {{ sortOrder === 'desc' ? '↓' : '↑' }}
            </span>
          </span>
          <span 
            class="category-badge clickable" 
            @click.stop="setSort('category')"
            :title="sortBy === 'category' ? 'クリックでソート' : 'クリックでジャンルでソート'"
          >
            {{ item.category }}
            <span v-if="sortBy === 'category'" class="sort-indicator">
              {{ sortOrder === 'desc' ? '↓' : '↑' }}
            </span>
          </span>
          <span 
            class="accuracy-badge clickable" 
            @click.stop="setSort('accuracy')"
            :title="sortBy === 'accuracy' ? 'クリックでソート' : 'クリックで正答率でソート'"
          >
            正答率: {{ item.accuracy }}%
            <span v-if="sortBy === 'accuracy'" class="sort-indicator">
              {{ sortOrder === 'desc' ? '↓' : '↑' }}
            </span>
          </span>
        </div>
        <div class="item-content">
          <p class="question-text clickable-question">{{ item.question_text }}</p>
          <div class="item-meta">
            <span class="result" :class="{ 'correct': item.is_correct, 'incorrect': !item.is_correct }">
              {{ item.is_correct ? '正解' : '不正解' }}
            </span>
            <span 
              class="timestamp clickable" 
              @click.stop="setSort('timestamp')"
              :title="sortBy === 'timestamp' ? 'クリックでソート' : 'クリックで解答日時でソート'"
            >
              {{ formatDate(item.timestamp) }}
              <span v-if="sortBy === 'timestamp'" class="sort-indicator">
                {{ sortOrder === 'desc' ? '↓' : '↑' }}
              </span>
            </span>
            <span class="attempts">試行回数: {{ item.total_attempts }}回（正解: {{ item.correct_attempts }}回）</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 問題詳細モーダル -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>問題詳細</h2>
          <button @click="closeModal" class="close-button">×</button>
        </div>
        <div v-if="questionDetail" class="modal-body">
          <div class="detail-section">
            <div class="detail-header">
              <span class="detail-category">{{ questionDetail.category }}</span>
              <span class="detail-difficulty">難易度: {{ getDifficultyLabel(questionDetail.difficulty) }}</span>
            </div>
            <p class="detail-question-text">{{ questionDetail.question_text }}</p>
            <div class="detail-options">
              <div 
                v-for="option in questionDetail.options" 
                :key="option.id"
                class="detail-option"
                :class="{ 'correct-option': option.is_correct }"
              >
                <span class="option-mark">{{ option.is_correct ? '✓' : '○' }}</span>
                <span class="option-text">{{ option.option_text }}</span>
                <span v-if="option.is_correct" class="correct-label">正解</span>
              </div>
            </div>
            <div v-if="questionDetail.explanation" class="detail-explanation">
              <h3>解説</h3>
              <p>{{ questionDetail.explanation }}</p>
            </div>
          </div>
        </div>
        <div v-else class="modal-loading">
          読み込み中...
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QuestionService from '@/services/question.service';

export default {
  name: 'AnswerHistory',
  data() {
    return {
      history: [],
      sortedHistory: [],
      loading: true,
      sortBy: 'timestamp',
      sortOrder: 'desc',
      showModal: false,
      questionDetail: null,
      loadingQuestion: false
    };
  },
  created() {
    this.loadHistory();
  },
  methods: {
    async loadHistory() {
      this.loading = true;
      try {
        const user = localStorage.getItem('user');
        console.log('ユーザー情報:', user);
        
        if (user) {
          const userData = JSON.parse(user);
          const userId = userData.user_id;
          console.log('ユーザーID:', userId);
          
          if (userId) {
            console.log('解答履歴を取得します...');
            this.history = await QuestionService.getAnswerHistory(userId);
            console.log('取得した解答履歴:', this.history);
            this.sortHistory();
          } else {
            console.warn('ユーザーIDが取得できませんでした');
          }
        } else {
          console.warn('ログイン情報がありません');
          alert('ログイン情報がありません。ログインしてください。');
        }
      } catch (error) {
        console.error('Error loading history:', error);
        console.error('Error details:', {
          message: error.message,
          response: error.response,
          responseData: error.response?.data,
          status: error.response?.status,
          stack: error.stack
        });
        
        let errorMessage = '不明なエラー';
        if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        } else if (error.message) {
          errorMessage = error.message;
        } else if (error.response?.status) {
          errorMessage = `HTTPエラー ${error.response.status}`;
        }
        
        alert('解答履歴の取得に失敗しました: ' + errorMessage);
        this.history = [];
      } finally {
        this.loading = false;
      }
    },
    sortHistory() {
      const sorted = [...this.history];
      sorted.sort((a, b) => {
        let aVal, bVal;
        
        if (this.sortBy === 'timestamp') {
          aVal = new Date(a.timestamp);
          bVal = new Date(b.timestamp);
        } else if (this.sortBy === 'question_id') {
          aVal = a.question_id;
          bVal = b.question_id;
        } else if (this.sortBy === 'category') {
          aVal = a.category;
          bVal = b.category;
        } else if (this.sortBy === 'accuracy') {
          aVal = a.accuracy;
          bVal = b.accuracy;
        }
        
        if (this.sortOrder === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
      
      this.sortedHistory = sorted;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString('ja-JP');
    },
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'desc' ? 'asc' : 'desc';
      this.sortHistory();
    },
    getSortLabel() {
      const sortLabels = {
        'timestamp': '解答日時',
        'question_id': '問題番号',
        'category': 'ジャンル',
        'accuracy': '正答率'
      };
      const orderLabels = {
        'desc': '降順',
        'asc': '昇順'
      };
      return `${sortLabels[this.sortBy]} - ${orderLabels[this.sortOrder]}`;
    },
    setSort(field) {
      if (this.sortBy === field) {
        // 同じフィールドの場合は順序を切り替え
        this.toggleSortOrder();
      } else {
        // 異なるフィールドの場合はそのフィールドで降順にソート
        this.sortBy = field;
        this.sortOrder = 'desc';
        this.sortHistory();
      }
    },
    async showQuestionDetail(questionId) {
      this.showModal = true;
      this.loadingQuestion = true;
      this.questionDetail = null;
      
      try {
        this.questionDetail = await QuestionService.getQuestionById(questionId);
      } catch (error) {
        console.error('Error loading question detail:', error);
        alert('問題の詳細を取得できませんでした: ' + (error.message || '不明なエラー'));
        this.closeModal();
      } finally {
        this.loadingQuestion = false;
      }
    },
    closeModal() {
      this.showModal = false;
      this.questionDetail = null;
    },
    getDifficultyLabel(difficulty) {
      const labels = {
        'easy': '易しい',
        'medium': '普通',
        'hard': '難しい'
      };
      return labels[difficulty] || difficulty;
    }
  }
};
</script>

<style scoped>
.answer-history {
  max-width: 1400px;
  margin: 1rem auto;
  padding: 1rem;
}

h1 {
  color: #333;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 1.5rem;
}

.history-controls {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sort-controls label {
  font-weight: 500;
  font-size: 0.9rem;
}

.sort-controls select {
  padding: 0.4rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
}

.sort-select {
  min-width: 120px;
}

.sort-order-button {
  padding: 0.4rem 0.8rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.2s;
  font-weight: bold;
}

.sort-order-button:hover {
  background-color: #0056b3;
}

.sort-info {
  margin-left: 0.5rem;
  color: #666;
  font-size: 0.85rem;
  font-weight: 500;
}

.loading, .no-data {
  text-align: center;
  padding: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-item {
  background-color: white;
  padding: 0.75rem;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  border-left: 3px solid #ddd;
  transition: box-shadow 0.2s;
  cursor: pointer;
}

.history-item:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  background-color: #f8f9fa;
}

.clickable-question {
  cursor: pointer;
}

.history-item.correct {
  border-left-color: #28a745;
}

.history-item.incorrect {
  border-left-color: #dc3545;
}

.item-header {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.question-id {
  font-weight: bold;
  color: #333;
  font-size: 0.85rem;
}

.clickable {
  cursor: pointer;
  transition: opacity 0.2s;
  user-select: none;
}

.clickable:hover {
  opacity: 0.8;
}

.sort-indicator {
  margin-left: 0.25rem;
  font-weight: bold;
  font-size: 0.9em;
}

.category-badge {
  background-color: #007bff;
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.accuracy-badge {
  background-color: #6c757d;
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.item-content {
  margin-top: 0.5rem;
}

.question-text {
  color: #555;
  margin-bottom: 0.4rem;
  line-height: 1.5;
  font-size: 0.9rem;
}

.item-meta {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  font-size: 0.8rem;
  color: #666;
}

.result {
  font-weight: bold;
  white-space: nowrap;
}

.result.correct {
  color: #28a745;
}

.result.incorrect {
  color: #dc3545;
}

.timestamp {
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.attempts {
  white-space: nowrap;
}

/* モーダルスタイル */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #ddd;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 10;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: #f0f0f0;
}

.modal-body {
  padding: 1.5rem;
}

.modal-loading {
  padding: 2rem;
  text-align: center;
  color: #666;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-header {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.detail-category {
  background-color: #007bff;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 500;
}

.detail-difficulty {
  background-color: #6c757d;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
}

.detail-question-text {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.6;
  margin: 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.detail-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  transition: background-color 0.2s;
}

.detail-option:hover {
  background-color: #f8f9fa;
}

.detail-option.correct-option {
  background-color: #d4edda;
  border-color: #28a745;
}

.option-mark {
  font-size: 1.2rem;
  font-weight: bold;
  width: 1.5rem;
  text-align: center;
}

.correct-option .option-mark {
  color: #28a745;
}

.option-text {
  flex: 1;
  color: #555;
  line-height: 1.5;
}

.correct-label {
  background-color: #28a745;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
  white-space: nowrap;
}

.detail-explanation {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #e7f3ff;
  border-left: 4px solid #007bff;
  border-radius: 5px;
}

.detail-explanation h3 {
  color: #007bff;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.detail-explanation p {
  color: #555;
  line-height: 1.6;
  margin: 0;
}
</style>

