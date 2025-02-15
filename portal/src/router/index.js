import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticlesView from '../views/ArticlesView.vue'
import ContactView from '@/views/ContactView.vue'
import ArticleDetailsView from '@/views/ArticleDetailsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticlesView
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView
    },
    {
      path: '/article/:id',
      name: 'article-details',
      component: ArticleDetailsView
    }
  ]
})

export default router
