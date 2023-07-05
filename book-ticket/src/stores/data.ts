import { defineStore } from 'pinia';
import { reactive, ref } from 'vue';

export const useData = defineStore('data', () => {
	const data = reactive<{ mobile: string; email: string }>({
		mobile: '',
		email: '',
	});

	const reserve = ref<number[]>([]);

	function setMobile(value: string) {
		data.mobile = value;
	}

	function setEmail(value: string) {
		data.email = value;
	}

	function getData() {
		return data;
	}

	function setReserve(value: number[]) {
		reserve.value = value;
	}

	function getReserve() {
		return reserve.value;
	}

	return { setMobile, setEmail, setReserve, getReserve, getData };
});
