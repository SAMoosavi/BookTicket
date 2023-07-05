import { RouteRecordRaw } from 'vue-router';
import { useToken } from 'stores/token';

const routes: RouteRecordRaw[] = [
	{
		path: '/',
		component: () => import('layouts/MainLayout.vue'),
		children: [
			{
				path: '/get-user',
				name: 'get-user',
				component: () => import('pages/UserData.vue'),
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
				path: '/find-train',
				name: 'find-train',
				component: () => import('pages/FindTrain.vue'),
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
		beforeEnter: (to, from, next) => {
			if (useToken().isLoggedIn()) next();
			else next({ name: 'login' });
		},
	},
];

export default routes;
