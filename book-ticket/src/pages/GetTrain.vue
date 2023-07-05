<template>
	<q-page class="row items-center justify-evenly">
		<q-card flat class="bg-transparent">
			<q-card-section class="items-center justify-center flex">
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

					<q-btn color="blue-5" type="submit">ارسال</q-btn>
				</q-form>
			</q-card-section>

			<q-separator />

			<q-card-section v-if="hasPropertyInObject(trains)">
				<q-card-actions>
					<q-btn class="full-width" color="blue-8" @click="send"> send</q-btn>
				</q-card-actions>

				<q-card-section>
					<q-card-actions class="justify-between row-reverse">
						<q-btn
							color="blue-4"
							class="col-3 q-mb-md"
							:outline="!all[2].hasAll"
							@click="togel_reserve_trains(all[2])"
						>
							عادی
						</q-btn>
						<q-btn
							color="blue-4"
							class="col-3 q-mb-md"
							:outline="!all[1].hasAll"
							@click="togel_reserve_trains(all[1])"
						>
							خواهران
						</q-btn>
						<q-btn
							color="blue-4"
							class="col-3 q-mb-md"
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
							<q-item class="row-reverse">
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

							<q-item class="items-center justify-center">
								<q-item-label>{{ price.WagonName }}</q-item-label>
							</q-item>

							<q-separator />

							<q-card-actions class="justify-between">
								<q-btn
									v-for="(val, index) in price.ID"
									:key="index"
									color="blue-4"
									class="col-3 q-mb-md"
									:outline="!val.has"
									@click="togel_reserve_train(val)"
								>
									<span v-if="index == 0"> برادران </span>
									<span v-else-if="index == 1"> خواهران </span>
									<span v-else>عادی</span>
								</q-btn>
							</q-card-actions>
						</q-card>
					</template>
				</template>

				<q-card-actions>
					<q-btn class="full-width" color="blue-8" @click="send"> send</q-btn>
				</q-card-actions>
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

const all = ref({
	0: { set: new Set(), hasAll: false },
	1: { set: new Set(), hasAll: false },
	2: { set: new Set(), hasAll: false },
});

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
				ID: { val: number[]; has: boolean }[];
				WagonName: string;
			};
		};
	};
}>({});

function hasPropertyInObject(ob: { [key: string]: any }) {
	for (const objectKey in ob) {
		return true;
	}
	return false;
}

const reserve = ref<Set<number>>(new Set());

function togel_reserve_train(trains: { val: number[]; has: boolean }) {
	for (const train of trains.val) {
		if (trains.has) reserve.value.delete(train);
		else reserve.value.add(train);
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
					ids.has = reserve.value.has(id);
				}
			}
		}
	}
}

async function submit() {
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
						].val.push(class1.ID);

						// @ts-ignore
						all.value[price.SellType - 1].set.add(class1.ID);
					}
				}
			}
		})
		.catch((err) => {
			console.error(err);
		});
}

function send() {
	console.log(reserve.value);
}
</script>
