<template>
	<q-page class="row items-center justify-evenly">
		<q-card
			style="width:100vw"
			flat
			class="bg-transparent items-center justify-evenly q-pa-md"
		>
			<q-card-section class="items-center justify-center flex text-h6">
				<h1 class="text-h4">انتخاب قطار</h1>
			</q-card-section>

			<q-card-section class="items-center justify-center flex text-h6">
				مشخصات قطار را وارد نمایید.
			</q-card-section>

			<q-card-section style="padding: 0" class="items-center justify-center flex">
				<q-form
					class="items-center justify-evenly q-pa-md"
					style="width: 500px"
					@submit.prevent="submit"
				>
					<select-location
						label="مبدا"
						class="q-mb-md"
						@value="
							(val) => {
								params.from = val;
							}
						"
					/>
					<select-location
						label="مقصد"
						class="q-mb-md"
						@value="
							(val) => {
								params.to = val;
							}
						"
					/>

					<persian-date
						today
						label="تاریخ حرکت"
						@value="
							(val) => {
								params.date = val;
							}
						"
					/>

					<q-btn color="blue-5" class="full-width" outline type="submit">
						جست و جوی قطار
					</q-btn>
				</q-form>
			</q-card-section>

			<q-separator />

			<q-card-section v-if="finding">
				<q-spinner-clock />
			</q-card-section>
			<q-card-section style="padding: 0;" v-else-if="hasPropertyInObject(trains)">
				<q-card-section class="items-center justify-center flex text-h6">
					قطار و بلیط مورد نظر خود را انتخاب نمایید
				</q-card-section>

				<q-card-section style="padding: 0;">
					<q-card-actions class="justify-between row-reverse">
						<q-btn
							color="blue-5"
							class="col-3"
							:outline="!all[2].hasAll"
							@click="togel_reserve_trains(all[2])"
						>
							عادی
						</q-btn>
						<q-btn
							color="blue-5"
							class="col-3"
							:outline="!all[1].hasAll"
							@click="togel_reserve_trains(all[1])"
						>
							خواهران
						</q-btn>
						<q-btn
							color="blue-5"
							class="col-3"
							:outline="!all[0].hasAll"
							@click="togel_reserve_trains(all[0])"
						>
							برادران
						</q-btn>
					</q-card-actions>
				</q-card-section>

				<template v-for="(train, index) in trains" :key="index">
					<template v-for="(price, index) in train.ID" :key="index">
						<q-card class="q-mt-md my-card text-center" bordered flat>
							<q-item class="items-center justify-center">
								<q-item-label>{{ price.WagonName }}</q-item-label>
							</q-item>

							<q-separator />

							<q-item class="row">
								<q-item-section>
									<q-item-label caption> حرکت</q-item-label>
									<q-item-label>
										{{ train.DepartureTime }}
									</q-item-label>
								</q-item-section>

								<q-item-section>
									<q-item-label caption> رسیدن</q-item-label>

									<q-item-label>
										{{ train.ArrivalTime }}
									</q-item-label>
								</q-item-section>
							</q-item>

							<q-separator />

							<q-card-actions class="justify-between">
								<template v-for="(val, index) in price.ID" :key="index">
									<q-separator vertical v-if="index != 0" />

									<q-item class="q-pa-none col-3 column">
										<q-btn
											color="blue-5"
											:outline="!val.has"
											@click="togel_reserve_train(val)"
										>
												<span v-if="index == 0"> برادران </span>
												<span v-else-if="index == 1"> خواهران </span>
												<span v-else>عادی</span>
										</q-btn>

										<q-item-label class="q-mt-sm text-caption text-grey">
											<span class="q-ml-md">
												{{ val.val.reduce((a, b) => a + b.capacity, 0) }}
											</span>
											<span>ظرفیت</span>
										</q-item-label>
									</q-item>
								</template>
							</q-card-actions>
						</q-card>
					</template>
				</template>

				<q-card-actions>
					<q-btn class="full-width q-my-md" color="blue-8" @click="send">
						رزرو
					</q-btn>
				</q-card-actions>

				<q-banner
					dir="rtl"
					inline-actions
					class="text-white q-mb-md"
					:class="{ 'bg-red': !!err, 'bg-transparent': !err }"
				>
					{{ err }}
				</q-banner>
			</q-card-section>
			<q-card-section v-else-if="server_error">
				{{ server_error }}
				<q-spinner-clock />
			</q-card-section>
		</q-card>
	</q-page>
</template>

<script setup lang="ts">
import PersianDate from 'components/PersianDate.vue';
import SelectLocation from 'components/SelectLocation.vue';
import { reactive, ref } from 'vue';
import { useGetAvailable } from 'src/functions/MrBilitApiWrapper';
import type { GetAvailableParameters } from 'src/functions/MrBilitApiWrapper.d';
import { useData } from 'stores/data';
import { useRouter } from 'vue-router';

const params = reactive<GetAvailableParameters>({
	from: 0,
	to: 0,
	date: '',
	adultCount: 1,
	childCount: 0,
	infantCount: 0,
	exclusive: false,
	availableStatus: 'Both',
});
let copy_params = { ...params };

const server_error = ref(false);

const all = ref({
	0: { set: new Set(), hasAll: false },
	1: { set: new Set(), hasAll: false },
	2: { set: new Set(), hasAll: false },
});

const finding = ref(false);

function hasAllInSet(parent: Set<number>, child: Set<number>) {
	let findAll = true;
	child.forEach((num) => {
		if (!parent.has(num)) findAll = false;
	});
	return findAll;
}

const trains = ref<{
	[TrainNumber: number]: {
		DepartureTime: string;
		ArrivalTime: string;
		ID: {
			[WagonID: number]: {
				ID: { val: { ID: number; capacity: number }[]; has: boolean }[];
				WagonName: string;
			};
		};
	};
}>({});

function hasPropertyInObject(ob: { [key: string]: any }) {
	return Object.keys(ob).length != 0;
}

const reserve = ref<Set<number>>(new Set());

function togel_reserve_train(trains: {
	val: { ID: number; capacities: number }[];
	has: boolean;
}) {
	for (const train of trains.val) {
		if (trains.has) reserve.value.delete(train.ID);
		else reserve.value.add(train.ID);
	}
	trains.has = !trains.has;
	for (const allKey in all.value) {
		all.value[allKey].hasAll = hasAllInSet(
			reserve.value,
			all.value[allKey].set
		);
	}
}

function togel_reserve_trains(myTrains: { set: Set<number>; hasAll: boolean }) {
	myTrains.set.forEach((train) => {
		if (myTrains.hasAll) reserve.value.delete(train);
		else reserve.value.add(train);
	});
	myTrains.hasAll = !myTrains.hasAll;
	for (const trainKey in trains.value) {
		for (const trainIdKes in trains.value[trainKey].ID) {
			for (const ids of trains.value[trainKey].ID[trainIdKes].ID) {
				for (const id of ids.val) {
					ids.has = reserve.value.has(id.ID);
				}
			}
		}
	}
}

async function submit() {
	trains.value = {};
	all.value = {
		0: { set: new Set(), hasAll: false },
		1: { set: new Set(), hasAll: false },
		2: { set: new Set(), hasAll: false },
	};
	reserve.value.clear();
	finding.value = true;
	await useGetAvailable(params)
		.then((response) => {
			for (const train of response.data.Trains) {
				for (const price of train.Prices) {
					for (const class1 of price.Classes) {
						if (!trains.value[train.TrainNumber])
							trains.value[train.TrainNumber] = {
								DepartureTime: train.DepartureTime.substring(11),
								ArrivalTime: train.ArrivalTime.substring(11),
								ID: {
									[class1.WagonID]: {
										WagonName: class1.WagonName,
										ID: [
											{ val: [], has: false },
											{ val: [], has: false },
											{ val: [], has: false },
										],
									},
								},
							};
						if (!trains.value[train.TrainNumber].ID[class1.WagonID])
							trains.value[train.TrainNumber].ID[class1.WagonID] = {
								WagonName: class1.WagonName,
								ID: [
									{ val: [], has: false },
									{ val: [], has: false },
									{ val: [], has: false },
								],
							};

						trains.value[train.TrainNumber].ID[class1.WagonID].ID[
							price.SellType - 1
						].val.push({ ID: class1.ID, capacity: class1.Capacity });

						// @ts-ignore
						all.value[price.SellType - 1].set.add(class1.ID);
					}
				}
			}
		})
		.catch((err) => {
			console.error(err);
			if (typeof err.response == 'string')
				err.response = JSON.parse(err.response);
			server_error.value = err.response.data.Error;
		})
		.finally(() => {
			finding.value = false;
			copy_params = { ...params };
		});
}

const err = ref('');
const data = useData();

const router = useRouter();

function send() {
	if (reserve.value.size == 0) err.value = 'حداقل یک قطار را باید انتخاب کنید';
	else {
		data.setReserve([...reserve.value]);
		data.setTrain(copy_params);
		router.push({ name: 'find-train' });
	}
}
</script>
