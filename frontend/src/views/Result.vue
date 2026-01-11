<template>
  <div class="result-page">
    <h1>解答結果</h1>
    
    <div v-if="results.length > 0" class="result-container">
      <!-- 統計情報 -->
      <div class="statistics">
        <div class="stat-card total">
          <h2>総問題数</h2>
          <p class="stat-number">{{ results.length }}</p>
        </div>
        <div class="stat-card correct">
          <h2>正解数</h2>
          <p class="stat-number">{{ correctCount }}</p>
        </div>
        <div class="stat-card incorrect">
          <h2>不正解数</h2>
          <p class="stat-number">{{ incorrectCount }}</p>
        </div>
        <div class="stat-card accuracy">
          <h2>正答率</h2>
          <p class="stat-number">{{ accuracy }}%</p>
        </div>
      </div>

      <!-- 問題別の結果 -->
      <div class="results-list">
        <h2>問題別の結果</h2>
        <div 
          v-for="(result, index) in results" 
          :key="index" 
          class="result-item"
          :class="{'correct': result.is_correct, 'incorrect': !result.is_correct}"
        >
          <div class="result-header">
            <span class="question-number">問題 {{ index + 1 }}</span>
            <span class="result-badge" :class="{'correct-badge': result.is_correct, 'incorrect-badge': !result.is_correct}">
              {{ result.is_correct ? '正解' : '不正解' }}
            </span>
          </div>
          <div class="question-content">
            <p class="question-text">{{ result.question.question_text }}</p>
            <div class="selected-answer">
              <strong>あなたの回答:</strong>
              <span>{{ getSelectedOptionText(result) }}</span>
            </div>
            <div v-if="!result.is_correct" class="correct-answer">
              <strong>正解:</strong>
              <span>{{ getCorrectOptionText(result) }}</span>
            </div>
            <div v-if="result.question.explanation" class="explanation">
              <strong>解説:</strong>
              <p>{{ result.question.explanation }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- アクションボタン -->
      <div class="actions">
        <router-link to="/question-selection" class="btn btn-primary">
          もう一度問題を解く
        </router-link>
        <router-link to="/" class="btn btn-secondary">
          ホームに戻る
        </router-link>
      </div>
    </div>
    
    <div v-else class="no-results">
      <p>結果データが見つかりませんでした。</p>
      <router-link to="/question-selection" class="btn btn-primary">
        問題を選定する
      </router-link>
    </div>
  </div>
</template>

<script>
import QuestionService from '@/services/question.service';

export default {
  name: 'ResultPage',
  data() {
    return {
      results: [],
      submitting: false
    };
  },
  computed: {
    correctCount() {
      return this.results.filter(r => r.is_correct).length;
    },
    incorrectCount() {
      return this.results.filter(r => !r.is_correct).length;
    },
    accuracy() {
      if (this.results.length === 0) return 0;
      return Math.round((this.correctCount / this.results.length) * 100);
    }
  },
  created() {
    this.loadResults();
    this.submitAnswersToBackend();
  },
  methods: {
    loadResults() {
      const quizResults = sessionStorage.getItem('quizResults');
      if (quizResults) {
        try {
          this.results = JSON.parse(quizResults);
        } catch (error) {
          console.error('Error parsing quiz results:', error);
          this.results = [];
        }
      }
    },
    async submitAnswersToBackend() {
      // ログインしている場合のみバックエンドに送信
      const userId = QuestionService.getUserId();
      if (!userId || this.results.length === 0) {
        return;
      }

      if (this.submitting) {
        return;
      }

      this.submitting = true;
      try {
        // 解答をバックエンドに送信
        const answers = this.results.map(result => ({
          question_id: result.question_id,
          selected_option_id: result.selected_option_id
        }));
        
        await QuestionService.submitAnswers(answers);
        console.log('解答をバックエンドに送信しました');
      } catch (error) {
        console.error('Error submitting answers to backend:', error);
        // エラーが発生しても結果表示は続行
      } finally {
        this.submitting = false;
      }
    },
    getSelectedOptionText(result) {
      const selectedOption = result.question.options.find(
        opt => opt.id === result.selected_option_id
      );
      return selectedOption ? selectedOption.option_text : '選択なし';
    },
    getCorrectOptionText(result) {
      const correctOption = result.question.options.find(
        opt => opt.is_correct
      );
      return correctOption ? correctOption.option_text : '不明';
    }
  }
};
</script>

<style scoped>
.result-page {
  max-width: 1000px;
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

.result-container {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.statistics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-card.correct {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.stat-card.incorrect {
  background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
  color: white;
}

.stat-card.accuracy {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
}

.stat-card h2 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  opacity: 0.9;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0;
}

.results-list {
  margin-top: 2rem;
}

.results-list h2 {
  color: #333;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.result-item {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #ddd;
  background-color: #f8f9fa;
  transition: all 0.2s;
}

.result-item.correct {
  border-left-color: #28a745;
  background-color: #d4edda;
}

.result-item.incorrect {
  border-left-color: #dc3545;
  background-color: #f8d7da;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}

.result-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.correct-badge {
  background-color: #28a745;
  color: white;
}

.incorrect-badge {
  background-color: #dc3545;
  color: white;
}

.question-content {
  text-align: left;
}

.question-text {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.selected-answer {
  margin-bottom: 0.5rem;
  padding: 0.8rem;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 5px;
}

.selected-answer strong {
  color: #333;
  margin-right: 0.5rem;
}

.correct-answer {
  padding: 0.8rem;
  background-color: rgba(40, 167, 69, 0.2);
  border-radius: 5px;
  border-left: 3px solid #28a745;
}

.correct-answer strong {
  color: #28a745;
  margin-right: 0.5rem;
}

.explanation {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #e7f3ff;
  border-left: 3px solid #007bff;
  border-radius: 5px;
}

.explanation strong {
  color: #007bff;
  margin-right: 0.5rem;
}

.explanation p {
  color: #555;
  line-height: 1.8;
  margin: 0.5rem 0 0 0;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 2rem;
  border-radius: 5px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.2s;
  display: inline-block;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.no-results {
  text-align: center;
  padding: 3rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.no-results p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}
</style>

