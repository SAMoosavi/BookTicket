import { defineStore } from 'pinia';
import { reactive, ref } from 'vue';
import type { GetAvailableParameters } from '../functions/MrBilitApiWrapper.d';

export const useData = defineStore('data', () => {
	const data = reactive<{ mobile: string; email: string }>({
		mobile: '',
		email: '',
	});

	const train = reactive<GetAvailableParameters>({
		from: 0,
		to: 0,
		date: '',
		adultCount: 1,
		childCount: 0,
		infantCount: 0,
		exclusive: false,
		availableStatus: 'Both',
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

	function setTrain(Train: GetAvailableParameters) {
		train.from = Train.from;
		train.to = Train.to;
		train.date = Train.date;
	}

	function getTrain(): GetAvailableParameters {
		return train;
	}

	return {
		setMobile,
		setEmail,
		setReserve,
		getReserve,
		getData,
		setTrain,
		getTrain,
	};
});
