import axios from 'axios';

// 環境変数からAPI URLを取得、なければデフォルト値を使用
const BASE_API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';
const API_URL = `${BASE_API_URL}/questions/`;

class QuestionService {
  async getRandomQuestion() {
    try {
      const response = await axios.get(API_URL + 'random');
      return response.data;
    } catch (error) {
      console.error('Error fetching random question:', error.response.data.message);
      throw error.response.data.message || '問題の取得に失敗しました。';
    }
  }

  getUserId() {
    const user = localStorage.getItem('user');
    if (user) {
      try {
        const userData = JSON.parse(user);
        return userData.user_id;
      } catch (e) {
        return null;
      }
    }
    return null;
  }

  async submitAnswer(questionId, selectedOptionId) {
    try {
      const userId = this.getUserId();
      const requestData = {
        question_id: questionId,
        selected_option_id: selectedOptionId
      };
      
      // user_idが存在する場合のみ追加
      if (userId) {
        requestData.user_id = userId;
      }
      
      const response = await axios.post(API_URL + 'submit_answer', requestData);
      return response.data;
    } catch (error) {
      console.error('Error submitting answer:', error);
      const errorMessage = error.response?.data?.message || error.message || '解答の送信に失敗しました。';
      throw new Error(errorMessage);
    }
  }

  async getCategories() {
    try {
      const response = await axios.get(API_URL + 'categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching categories:', error.response?.data?.message);
      throw error.response?.data?.message || 'ジャンルの取得に失敗しました。';
    }
  }

  async getQuestionsByCriteria(criteria) {
    try {
      const userId = this.getUserId();
      const response = await axios.post(API_URL + 'by_criteria', {
        ...criteria,
        user_id: userId
      });
      // バックエンドは {questions: [...]} の形式で返すので、そのまま返す
      return response.data;
    } catch (error) {
      console.error('Error fetching questions by criteria:', error.response?.data?.message);
      throw error.response?.data?.message || '問題の取得に失敗しました。';
    }
  }

  async submitAnswers(answers) {
    try {
      const userId = this.getUserId();
      const requestData = {
        answers: answers
      };
      
      // user_idが存在する場合のみ追加
      if (userId) {
        requestData.user_id = userId;
      }
      
      const response = await axios.post(API_URL + 'submit_answers', requestData);
      return response.data;
    } catch (error) {
      console.error('Error submitting answers:', error);
      const errorMessage = error.response?.data?.message || error.message || '解答の送信に失敗しました。';
      throw new Error(errorMessage);
    }
  }

  async getAnswerHistory(userId) {
    try {
      console.log('解答履歴を取得します。ユーザーID:', userId);
      const response = await axios.get(API_URL + `answer_history/${userId}`);
      console.log('解答履歴のレスポンス:', response.data);
      return response.data.history || [];
    } catch (error) {
      console.error('Error fetching answer history:', error);
      console.error('Error response:', error.response);
      const errorMessage = error.response?.data?.message || error.message || '解答履歴の取得に失敗しました。';
      throw new Error(errorMessage);
    }
  }

  async getIncorrectQuestions(period = 'all') {
    try {
      const userId = this.getUserId();
      const response = await axios.post(API_URL + 'incorrect_questions', {
        user_id: userId,
        period: period
      });
      return response.data.questions || [];
    } catch (error) {
      console.error('Error fetching incorrect questions:', error.response?.data?.message);
      throw error.response?.data?.message || '間違えた問題の取得に失敗しました。';
    }
  }

  async getQuestionById(questionId) {
    try {
      const url = API_URL + questionId;
      console.log('問題詳細取得リクエスト:', url);
      const response = await axios.get(url);
      console.log('問題詳細取得レスポンス:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error fetching question:', error);
      console.error('Error response:', error.response);
      const errorMessage = error.response?.data?.message || error.message || '問題の取得に失敗しました。';
      throw new Error(errorMessage);
    }
  }

  async getUserStatistics(userId) {
    try {
      const response = await axios.get(API_URL + `statistics/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user statistics:', error.response?.data?.message);
      throw error.response?.data?.message || '統計情報の取得に失敗しました。';
    }
  }
}

export default new QuestionService();
