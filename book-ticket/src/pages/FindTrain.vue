<template>
	<q-page class="row items-center justify-evenly">
		<q-card dir="rtl" flat class="bg-transparent">
			<q-card-section class="items-center justify-center flex">
				<q-spinner-ball color="blue" size="2em" />
				در حال رزرو بلیط برای
				<span v-if="user.getUser().male" class="q-mx-sm"> آقای </span>
				<span v-else class="q-mx-sm"> خانم </span>
				<span>{{ user.getFullName() }}</span>
				<q-spinner-ball color="blue" size="2em" />
			</q-card-section>

			<q-card-section> تعداد تلاش ها: {{ numberOfTry }}</q-card-section>

			<q-card-section>
				<span v-if="train === 0"> یافت نشد لظفا صبر کنید...</span>
				<span v-else>بلیط پیدا شد!!</span>
			</q-card-section>

			<q-card-section>
				<q-banner
					class="text-white full-width bg-transparent"
					:class="{ 'bg-red': !!err, 'bg-blue': !!message }"
				>
					{{ err }}
				</q-banner>
			</q-card-section>
		</q-card>
	</q-page>
</template>

<script setup lang="ts">
import { useData } from 'stores/data';
import { useUser } from 'stores/user';
import {
	useGetAvailable,
	useGetStatus,
	usePay,
	useRegisterInfo,
	useReserveSeat,
} from 'src/functions/MrBilitApiWrapper';
import { onMounted, ref } from 'vue';
import { useSleep } from 'src/functions/promis';

const data = useData();
const user = useUser();

const err = ref('');
const message = ref('');

const availableTrains = ref<{ trainId: number; genderCode: number }[]>([]);
const numberOfTry = ref<number>(0);

const train = ref<{ trainId: number; genderCode: number } | undefined>();

const listOfTickets = ref<string[]>([]);

async function checkTrain() {
	return await new Promise<void>(async (resolve) => {
		while (true) {
			availableTrains.value = [];
			let hasError = false;

			await useGetAvailable(data.getTrain())
				.then((response) => {
					for (const train of response.data.Trains)
						for (const price of train.Prices)
							for (const class1 of price.Classes)
								if (class1.Capacity != 0)
									availableTrains.value.push({
										trainId: class1.ID,
										genderCode: price.SellType,
									});

					for (const availableTrain of availableTrains.value) {
						if (data.getReserve().indexOf(availableTrain.trainId) != -1) {
							train.value = availableTrain;
							break;
						}
					}
				})
				.catch((err) => {
					console.error(err);
					hasError = true;
				})
				.finally(() => {
					numberOfTry.value++;
				});

			if (train.value) {
				resolve();
				break;
			}

			if (hasError) await useSleep(120000);
			else await useSleep(4000);
		}
	});
}

let mac = '';

async function reserveTrain() {
	await useReserveSeat({
		trainID: <number>train.value?.trainId,
		adultCount: '1',
		childCount: '0',
		infantCount: '0',
		includeOptionalServices: true,
		exclusive: false,
		genderCode: <number>train.value?.genderCode,
		seatCount: '1',
	}).then(async (response) => {
		await useRegisterInfo(response.data.BillID);

		await usePay(response.data.BillCode)
			.then((response) => {
				const params = new URL(response.request.responseURL).searchParams;
				if (params.has('mac')) mac = <string>params.get('mac');
				else err.value = 'موجودی کافی نیست';
			})
			.catch((error) => {
				console.error(error);
			});

		let isSuccessful: null | true = null;
		if (mac)
			while (true) {
				await useGetStatus(response.data.BillCode, mac)
					.then((response) => {
						isSuccessful = response.data.isSuccessful;
						message.value = response.data.title;
					})
					.catch((error) => {
						console.error(error);
					});

				if (listOfTickets.value.length == 0) await useSleep(3000);
				else break;
			}
	});
}

onMounted(async () => {
	await checkTrain();
	await reserveTrain();
});
</script>
