import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse } from 'axios';

export function useSleep(ms: number) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

export function useApiGet(
	url: string,
	config: AxiosRequestConfig,
	accept?: (response: AxiosResponse) => void,
	error?: (err: any) => void
): Promise<AxiosResponse> {
	return new Promise(async (resolve, reject) => {
		await axios
			.get(url, config)
			.then((response) => {
				if (accept) accept(response);
				resolve(response);
			})
			.catch((err) => {
				if (error) error(err);
				reject(err);
			});
	});
}

export function useApiPost(
	url: string,
	data: any,
	config: AxiosRequestConfig,
	accept?: (response: AxiosResponse) => void,
	error?: (err: any) => void
): Promise<AxiosResponse> {
	return new Promise(async (resolve, reject) => {
		await axios
			.post(url, data, config)
			.then((response) => {
				if (accept) accept(response);
				resolve(response);
			})
			.catch((err) => {
				if (error) error(err);
				reject(err);
			});
	});
}
