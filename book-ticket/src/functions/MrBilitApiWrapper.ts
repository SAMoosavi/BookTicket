import { useApiGet, useApiPost } from './promis';
import { useJalaliToGregorian } from './date';
import type {
	GetAvailableParameters,
	LoginParameters,
	ReserveSeatParameters,
} from './MrBilitApiWrapper.d';
import { useToken } from 'stores/token';
import { useUser } from 'stores/user';
import { useData } from 'stores/data';

const token = useToken();

export async function useLogin(params: LoginParameters) {
	return await useApiGet('https://auth.mrbilit.com/api/login', { params });
}

export async function useGetAvailable(params: GetAvailableParameters) {
	return await useApiGet(
		'https://train.atighgasht.com/TrainService/api/GetAvailable/v2',
		{
			params: { ...params, date: useJalaliToGregorian(params.date) },
		}
	);
}

export async function useReserveSeat(params: ReserveSeatParameters) {
	return await useApiGet(
		'https://train.atighgasht.com/TrainService/api/ReserveSeat',
		{
			params: {
				trainID: params.trainID,
				adultCount: '1',
				childCount: '0',
				infantCount: '0',
				includeOptionalServices: true,
				exclusive: false,
				genderCode: params.genderCode,
				seatCount: '1',
			},
			headers: token.getHeader(),
		}
	);
}

export async function useRegisterInfo(bill_ID: number) {
	const User = useUser();
	const user = User.getUser();

	const Data = useData();
	const data = Data.getData();

	return await useApiPost(
		'https://train.atighgasht.com/TrainService/api/RegisterInfo',
		{
			Email: data.email,
			Mobile: data.mobile,
			People: [
				{
					PersianFirstName: user.persianFirstName,
					PersianLastName: user.persianLastName,
					Male: user.male,
					BirthDay: useJalaliToGregorian(user.birthDay),
					NationalCode: user.nationalCode,
					TrainCars: [],
					TrainCapacityOptionalService: {},
				},
			],
			Phone: '',
			BillID: bill_ID,
		},
		{
			headers: token.getHeader(),
		}
	);
}

export async function usePay(bill_code: string) {
	return await useApiGet(
		`https://payment.mrbilit.com/api/billpayment/${bill_code}`,
		{
			params: {
				payFromCredit: true,
				access_token: token.getToken(),
			},
			headers: token.getHeader(),
		}
	);
}

export async function useGetStatus(bill_code: number, mac: string) {
	return await useApiGet(
		`https://finalize.mrbilit.com/api/workflow/bill/${bill_code}/status`,
		{
			params: { mac: mac },
		}
	);
}
