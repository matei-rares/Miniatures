import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/Home.vue'
import BlogView from '../components/Blog.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/blog',
        name: 'blog',
        component: BlogView
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
