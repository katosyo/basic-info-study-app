<template>
  <div class="quiz-page">
    <h1>問題解答</h1>
    <div v-if="questions.length > 0" class="quiz-container">
      <div class="progress-info">
        <p>問題 {{ currentQuestionIndex + 1 }} / {{ questions.length }}</p>
      </div>
      
      <div v-if="currentQuestion" class="question-card">
        <p class="question-text">{{ currentQuestion.question_text }}</p>
        <div class="options">
          <div 
            v-for="option in currentQuestion.options" 
            :key="option.id" 
            class="option-item"
            :class="{
              'selected': selectedOptionId === option.id && !feedback,
              'excluded': excludedOptions.includes(option.id) && !feedback,
              'user-answer': feedback && !feedback.is_correct && selectedOptionId === option.id,
              'correct-answer': feedback && option.is_correct,
              'disabled': feedback
            }"
            @click="!feedback && selectOption(option.id)"
            @contextmenu.prevent="!feedback && excludeOption(option.id)"
          >
            <input 
              type="radio" 
              :id="`option-${option.id}`" 
              :value="option.id" 
              v-model="selectedOptionId"
              @click.stop
              :disabled="!!feedback"
            >
            <label :for="`option-${option.id}`" class="option-label">
              <span :class="{ 'excluded-text': excludedOptions.includes(option.id) && !feedback }">
                {{ option.option_text }}
              </span>
              <span v-if="feedback && !feedback.is_correct && selectedOptionId === option.id" class="answer-label user-answer-label">
                あなたの回答
              </span>
              <span v-if="feedback && option.is_correct" class="answer-label correct-answer-label">
                ✓ 正解
              </span>
            </label>
          </div>
        </div>
        <div class="actions">
          <button @click="submitAnswer" :disabled="!selectedOptionId" class="submit-button">
            解答する
          </button>
          <button @click="clearExclusions" class="clear-button" v-if="excludedOptions.length > 0">
            除外を解除
          </button>
        </div>
        <p v-if="feedback" :class="{'feedback': true, 'correct': feedback.is_correct, 'incorrect': !feedback.is_correct}">
          {{ feedback.message }}
        </p>
        <div v-if="feedback && currentQuestion.explanation" class="explanation">
          <h3>解説</h3>
          <p>{{ currentQuestion.explanation }}</p>
        </div>
        <button v-if="feedback" @click="nextQuestion" class="next-button">
          {{ isLastQuestion ? '結果を見る' : '次の問題へ' }}
        </button>
      </div>
    </div>
    <p v-else-if="!loading" class="no-questions">問題がありません。問題選定画面から問題を選択してください。</p>
    <p v-else class="loading">問題を読み込み中...</p>
  </div>
</template>

<script>
import QuestionService from '@/services/question.service';

export default {
  name: 'QuizPage',
  data() {
    return {
      questions: [],
      currentQuestionIndex: 0,
      currentQuestion: null,
      selectedOptionId: null,
      excludedOptions: [],
      feedback: null,
      loading: true,
      answers: [] // 解答を保存
    };
  },
  computed: {
    isLastQuestion() {
      return this.currentQuestionIndex === this.questions.length - 1;
    }
  },
  created() {
    this.loadQuestions();
  },
  methods: {
    loadQuestions() {
      // セッションストレージから問題データを読み込む
      const quizQuestions = sessionStorage.getItem('quizQuestions');
      if (quizQuestions) {
        try {
          this.questions = JSON.parse(quizQuestions);
          if (this.questions.length > 0) {
            this.currentQuestion = this.questions[0];
          }
        } catch (error) {
          console.error('Error parsing quiz questions:', error);
          this.questions = [];
        }
      } else {
        // セッションストレージに問題がない場合は、ランダムに1問取得
        this.fetchRandomQuestion();
      }
      this.loading = false;
    },
    async fetchRandomQuestion() {
      try {
        const response = await QuestionService.getRandomQuestion();
        this.questions = [response];
        this.currentQuestion = response;
      } catch (error) {
        console.error('Error fetching random question:', error);
        this.questions = [];
      }
    },
    selectOption(optionId) {
      // 除外されている選択肢は選択できない
      if (this.excludedOptions.includes(optionId)) {
        return;
      }
      this.selectedOptionId = optionId;
    },
    excludeOption(optionId) {
      // 右クリックで選択肢を除外/解除
      const index = this.excludedOptions.indexOf(optionId);
      if (index > -1) {
        this.excludedOptions.splice(index, 1);
      } else {
        this.excludedOptions.push(optionId);
        // 除外された選択肢が選択されていた場合は選択を解除
        if (this.selectedOptionId === optionId) {
          this.selectedOptionId = null;
        }
      }
    },
    clearExclusions() {
      this.excludedOptions = [];
    },
    async submitAnswer() {
      if (!this.selectedOptionId) {
        return;
      }
      try {
        console.log('解答を送信します:', {
          question_id: this.currentQuestion.id,
          selected_option_id: this.selectedOptionId,
          user_id: QuestionService.getUserId()
        });
        
        const response = await QuestionService.submitAnswer(this.currentQuestion.id, this.selectedOptionId);
        const isCorrect = response.is_correct;
        
        console.log('解答送信成功:', response);
        
        // 解答を保存
        this.answers.push({
          question_id: this.currentQuestion.id,
          selected_option_id: this.selectedOptionId,
          is_correct: isCorrect,
          question: this.currentQuestion
        });
        
        // 正解の選択肢IDを取得
        const correctOption = this.currentQuestion.options.find(opt => opt.is_correct);
        const correctOptionId = correctOption ? correctOption.id : null;
        
        if (isCorrect) {
          this.feedback = { 
            is_correct: true, 
            message: '正解です！',
            selectedOptionId: this.selectedOptionId,
            correctOptionId: correctOptionId
          };
        } else {
          this.feedback = { 
            is_correct: false, 
            message: '不正解です。',
            selectedOptionId: this.selectedOptionId,
            correctOptionId: correctOptionId
          };
        }
      } catch (error) {
        console.error('Error submitting answer:', error);
        const errorMessage = error.response?.data?.message || error.message || '解答の送信に失敗しました。';
        this.feedback = { is_correct: false, message: errorMessage };
        alert('解答の送信に失敗しました: ' + errorMessage);
      }
    },
    nextQuestion() {
      if (this.isLastQuestion) {
        // 最後の問題の場合は結果画面に遷移
        sessionStorage.setItem('quizResults', JSON.stringify(this.answers));
        this.$router.push('/result');
      } else {
        // 次の問題へ
        this.currentQuestionIndex++;
        this.currentQuestion = this.questions[this.currentQuestionIndex];
        this.selectedOptionId = null;
        this.excludedOptions = [];
        this.feedback = null;
      }
    }
  }
};
</script>

<style scoped>
.quiz-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 1.5rem;
}

.progress-info {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #666;
  font-weight: bold;
}

.quiz-container {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.question-card {
  text-align: left;
}

.question-text {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #555;
  line-height: 1.6;
}

.options {
  margin-bottom: 1.5rem;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
  padding: 0.8rem;
  border: 2px solid #eee;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  position: relative;
}

.option-item:hover:not(.excluded) {
  background-color: #eef;
  border-color: #007bff;
}

.option-item.selected {
  background-color: #d4edda;
  border-color: #28a745;
}

.option-item.user-answer {
  background-color: #f8d7da;
  border-color: #dc3545;
  border-width: 3px;
}

.option-item.correct-answer {
  background-color: #d4edda;
  border-color: #28a745;
  border-width: 3px;
}

.option-item.disabled {
  cursor: default;
  pointer-events: none;
}

.option-item.disabled:hover {
  background-color: inherit;
  border-color: inherit;
}

.option-item.excluded {
  background-color: #f8f9fa;
  border-color: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.option-item.excluded .excluded-text {
  text-decoration: line-through;
  color: #999;
}

.option-item input[type="radio"] {
  margin-right: 1rem;
  transform: scale(1.2);
  cursor: pointer;
}

.option-label {
  flex-grow: 1;
  cursor: pointer;
  font-size: 1rem;
  color: #444;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.answer-label {
  font-size: 0.9rem;
  font-weight: bold;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  margin-left: 1rem;
}

.user-answer-label {
  background-color: #dc3545;
  color: white;
}

.correct-answer-label {
  background-color: #28a745;
  color: white;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

button {
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease-in-out;
}

.submit-button {
  background-color: #007bff;
  color: white;
}

.submit-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.submit-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.clear-button {
  background-color: #6c757d;
  color: white;
}

.clear-button:hover {
  background-color: #5a6268;
}

.next-button {
  background-color: #28a745;
  color: white;
  margin-top: 1rem;
}

.next-button:hover {
  background-color: #218838;
}

.feedback {
  margin-top: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  padding: 0.5rem;
  border-radius: 5px;
}

.feedback.correct {
  color: #28a745;
  background-color: #d4edda;
}

.feedback.incorrect {
  color: #dc3545;
  background-color: #f8d7da;
}

.explanation {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background-color: #e7f3ff;
  border-left: 4px solid #007bff;
  border-radius: 5px;
  text-align: left;
}

.explanation h3 {
  color: #007bff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.explanation p {
  color: #555;
  line-height: 1.8;
  margin: 0;
}

.no-questions, .loading {
  color: #666;
  font-size: 1.1rem;
  margin-top: 2rem;
}
</style>
