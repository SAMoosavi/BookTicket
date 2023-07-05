import { defineStore } from 'pinia';
import { reactive, ref } from 'vue';

export const useData = defineStore('data', () => {
	const data = reactive<{ mobile: string; email: string }>({
		mobile: '',
		email: '',
	});

	const fullName = ref('');

	function setMobile(value: string) {
		data.mobile = value;
	}

	function setEmail(value: string) {
		data.email = value;
	}

	function setFullName(value: string) {
		fullName.value = value;
	}

	function getFullName() {
		return fullName.value;
	}

	return { setMobile, setEmail, setFullName, getFullName };
});
