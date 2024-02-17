import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CommunityView from '../views/CommunityView.vue'
import SignupView from '../views/SignupView.vue'


import { useCounterStore } from '../stores/counter'

import DetailView from '../views/community/DetailView.vue'
import CreateView from '../views/community/CreateView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
    
    
    {
      path: '/reviews/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/review/:id',
      name: 'UpdateView',
      component: CreateView
    },
    
  ]
})

router.beforeEach((to,from)=>{
  const store = useCounterStore()
  if (to.name === 'CommunityView' && !store.isLogin){
    window.alert('로그인이 필요합니다.')
    return { name: 'LoginView'}
  }
  if ((to.name === 'SignUpView' || to.name === 'LoginView') && (store.isLogin)) {
    window.alert('이미 로그인이 되어 있습니다.')
    return { name: 'CommunityView'}
  }
})


export default router
