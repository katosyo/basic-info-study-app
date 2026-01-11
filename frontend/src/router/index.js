import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue'; // 既存のHomeコンポーネント
import Login from '../views/Login.vue'; // 作成したLoginコンポーネント
import Quiz from '../views/Quiz.vue'; // 追加
import QuestionSelection from '../views/QuestionSelection.vue'; // 問題選定画面
import Result from '../views/Result.vue'; // 結果表示画面

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "register" */ '../views/Register.vue') // 後で作成する登録ページ
  },
  {
    path: '/question-selection', // 問題選定画面
    name: 'QuestionSelection',
    component: QuestionSelection
  },
  {
    path: '/quiz', // 問題解答画面
    name: 'Quiz',
    component: Quiz
  },
  {
    path: '/result', // 結果表示画面
    name: 'Result',
    component: Result
  },
  {
    path: '/user-dashboard', // ユーザー管理画面
    name: 'UserDashboard',
    component: () => import(/* webpackChunkName: "user-dashboard" */ '../views/UserDashboard.vue')
  },
  {
    path: '/answer-history', // 解答履歴画面
    name: 'AnswerHistory',
    component: () => import(/* webpackChunkName: "answer-history" */ '../views/AnswerHistory.vue')
  },
  {
    path: '/study-materials', // 対策問題集・ノート作成画面
    name: 'StudyMaterials',
    component: () => import(/* webpackChunkName: "study-materials" */ '../views/StudyMaterials.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/question-selection', '/quiz', '/result'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    // 認証が必要なページでログインしていない場合、ログインページにリダイレクト
    next('/login');
  } else if (loggedIn && (to.path === '/login' || to.path === '/register')) {
    // ログイン済みで、かつログイン・登録ページにアクセスしようとした場合、ホームにリダイレクト
    next('/');
  } else {
    // それ以外の場合は許可
    next();
  }
});

export default router;

