import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useToken = defineStore('token', () => {
	const token = ref('');
	const header = ref<{ Authorization: string }>({ Authorization: '' });

	function setToken(tok: string) {
		token.value = tok;
		header.value.Authorization = 'Bearer ' + token.value;
	}

	function getToken() {
		return token.value;
	}

	function getHeader() {
		return header.value;
	}

	function isLoggedIn() {
		return token.value !== '';
	}

	return { setToken, getToken, getHeader, isLoggedIn };
});
