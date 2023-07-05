import { defineStore } from 'pinia';
import { reactive } from 'vue';

export const useData = defineStore('data', () => {
	const data = reactive<{ mobile: string; email: string }>({
		mobile: '',
		email: '',
	});

	function setMobile(value: string) {
		data.mobile = value;
	}

	function setEmail(value: string) {
		data.email = value;
	}

	return { setMobile, setEmail };
});
