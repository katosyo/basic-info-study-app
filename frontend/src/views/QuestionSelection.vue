<template>
  <div class="question-selection">
    <h1>問題を選定</h1>
    
    <div class="selection-form">
      <!-- ジャンル選択 -->
      <div class="form-section">
        <h2>ジャンルを選択</h2>
        <div class="category-checkboxes">
          <label v-for="category in categories" :key="category" class="checkbox-label">
            <input 
              type="checkbox" 
              :value="category" 
              v-model="selectedCategories"
              class="checkbox-input"
            >
            <span>{{ category }}</span>
          </label>
        </div>
        <p v-if="categories.length === 0" class="loading">ジャンルを読み込み中...</p>
      </div>

      <!-- 問題数選択 -->
      <div class="form-section">
        <h2>問題数</h2>
        <select v-model="questionCount" class="select-input">
          <option v-for="n in [5, 10, 15, 20, 30, 50]" :key="n" :value="n">{{ n }}問</option>
        </select>
      </div>

      <!-- 出題順選択 -->
      <div class="form-section">
        <h2>出題順</h2>
        <div class="radio-group">
          <label class="radio-label">
            <input type="radio" value="random" v-model="order" class="radio-input">
            <span>ランダム</span>
          </label>
          <label class="radio-label">
            <input type="radio" value="unseen" v-model="order" class="radio-input">
            <span>見たことない問題優先</span>
          </label>
          <label class="radio-label">
            <input type="radio" value="incorrect" v-model="order" class="radio-input">
            <span>間違えた問題優先</span>
          </label>
        </div>
      </div>

      <!-- 開始ボタン -->
      <div class="form-actions">
        <button @click="startQuiz" :disabled="selectedCategories.length === 0" class="start-button">
          問題を開始
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import QuestionService from '@/services/question.service';

export default {
  name: 'QuestionSelection',
  data() {
    return {
      categories: [],
      selectedCategories: [],
      questionCount: 10,
      order: 'random'
    };
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await QuestionService.getCategories();
        this.categories = response.categories || [];
        // デフォルトですべて選択
        this.selectedCategories = [...this.categories];
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.categories = [];
      }
    },
    async startQuiz() {
      if (this.selectedCategories.length === 0) {
        alert('少なくとも1つのジャンルを選択してください。');
        return;
      }

      try {
        console.log('問題取得リクエスト:', {
          categories: this.selectedCategories,
          count: this.questionCount,
          order: this.order
        });

        const response = await QuestionService.getQuestionsByCriteria({
          categories: this.selectedCategories,
          count: this.questionCount,
          order: this.order
        });

        console.log('問題取得レスポンス:', response);

        // レスポンスが配列の場合とオブジェクトの場合の両方に対応
        const questions = Array.isArray(response) ? response : (response.questions || []);
        
        console.log('抽出した問題:', questions);
        
        if (questions && questions.length > 0) {
          // 問題データをセッションストレージに保存して、Quiz画面に渡す
          sessionStorage.setItem('quizQuestions', JSON.stringify(questions));
          sessionStorage.setItem('quizSettings', JSON.stringify({
            categories: this.selectedCategories,
            count: this.questionCount,
            order: this.order
          }));
          this.$router.push('/quiz');
        } else {
          alert('選択した条件に該当する問題が見つかりませんでした。');
        }
      } catch (error) {
        console.error('Error starting quiz:', error);
        console.error('Error response:', error.response);
        if (error.response && error.response.status === 404) {
          alert('選択した条件に該当する問題が見つかりませんでした。');
        } else {
          alert('問題の取得に失敗しました: ' + (error.message || '不明なエラー'));
        }
      }
    }
  }
};
</script>

<style scoped>
.question-selection {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.selection-form {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h2 {
  color: #555;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.category-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.checkbox-label:hover {
  background-color: #f0f0f0;
}

.checkbox-input {
  margin-right: 0.5rem;
  transform: scale(1.2);
  cursor: pointer;
}

.select-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background-color: #fff;
  cursor: pointer;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.radio-label:hover {
  background-color: #f0f0f0;
}

.radio-input {
  margin-right: 0.5rem;
  transform: scale(1.2);
  cursor: pointer;
}

.form-actions {
  margin-top: 2rem;
  text-align: center;
}

.start-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 1rem 3rem;
  border-radius: 5px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.start-button:hover:not(:disabled) {
  background-color: #218838;
}

.start-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.loading {
  color: #666;
  font-style: italic;
}
</style>

