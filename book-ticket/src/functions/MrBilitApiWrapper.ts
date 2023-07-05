import { useApi } from './promis';
import { useJalaliToGregorian } from './date';
import type {
	GetAvailableParameters,
	LoginParameters,
} from './MrBilitApiWrapper.d';

export async function useLogin(params: LoginParameters) {
	return await useApi('https://auth.mrbilit.com/api/login', { params });
}

export async function useGetAvailable(params: GetAvailableParameters) {
	return await useApi(
		'https://train.atighgasht.com/TrainService/api/GetAvailable/v2',
		{
			params: { ...params, date: useJalaliToGregorian(params.date) },
		}
	);
}
