import axios from 'axios';

// 環境変数からAPI URLを取得、なければデフォルト値を使用
const BASE_API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';
const API_URL = `${BASE_API_URL}/auth/`;

class AuthService {
  async login(username, password) {
    try {
      const response = await axios.post(API_URL + 'login', {
        username,
        password
      });
      if (response.data.message) {
        localStorage.setItem('user', JSON.stringify({ 
          loggedIn: true, 
          username: response.data.username || username,
          user_id: response.data.user_id
        }));
      }
      return response.data;
    } catch (error) {
      console.error('Login error:', error.response.data.message);
      throw error.response.data.message || 'ログインに失敗しました';
    }
  }

  async register(username, email, password) {
    try {
      const response = await axios.post(API_URL + 'register', {
        username,
        email,
        password
      });
      return response.data;
    } catch (error) {
      console.error('Register error:', error.response.data.message);
      throw error.response.data.message || '登録に失敗しました';
    }
  }

  // 他の認証関連のメソッド（ログアウト、ユーザー情報取得など）もここに追加
}

export default new AuthService();

