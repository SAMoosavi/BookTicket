import { RouteRecordRaw } from 'vue-router';
import { useToken } from 'stores/token';

const routes: RouteRecordRaw[] = [
	{
		path: '/',
		component: () => import('layouts/MainLayout.vue'),
		children: [
			{
				path: '',
				name: 'home',
				component: () => import('pages/IndexPage.vue'),
				beforeEnter: (to, from, next) => {
					if (useToken().isLoggedIn()) next();
					else next({ name: 'login' });
				},
			},
			{
				path: '/get-train',
				name: 'get-train',
				component: () => import('pages/GetTrain.vue'),
				beforeEnter: (to, from, next) => {
					if (useToken().isLoggedIn()) next();
					else next({ name: 'login' });
				},
			},
			{
				path: '/login',
				name: 'login',
				component: () => import('pages/LoginUser.vue'),
				beforeEnter: (to, from, next) => {
					if (!useToken().isLoggedIn()) next();
					else next({ name: 'home' });
				},
			},
		],
	},

	// Always leave this as last one,
	// but you can also remove it
	{
		path: '/:catchAll(.*)*',
		component: () => import('pages/ErrorNotFound.vue'),
	},
];

export default routes;
