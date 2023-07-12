<template>
	<q-page class="row items-center justify-evenly">
		<q-card
			flat
			class="bg-transparent items-center justify-evenly q-pa-md"
			style="width: 500px"
		>
			<q-card-section class="items-center justify-center flex text-h6">
				مشخصات خود را برای ثبت در بلیط وارد نمایید.
			</q-card-section>

			<q-card-section>
				<q-select
					class="full-width"
					filled
					use-input
					hide-selected
					fill-input
					input-debounce="0"
					label="select user"
					:options="users"
					v-model="userSelected"
				/>
			</q-card-section>

			<q-card-section>
				<q-form @submit.prevent="submit">
					<q-input
						filled
						label="نام"
						class="q-mb-md"
						dir="rtl"
						v-model="user.persianFirstName"
						:rules="[(val) => !!val || 'این فیلد الزامی است.', justPersian]"
					/>

					<q-input
						filled
						label="نام خانوادگی"
						class="q-mb-md"
						dir="rtl"
						v-model="user.persianLastName"
						:rules="[(val) => !!val || 'این فیلد الزامی است.', justPersian]"
					/>

					<!--					<persian-date
											v-model="user.birthDay"
											class="q-mb-md"
											:rules="[(val) => !!val || 'این فیلد الزامی است.']"
											label="تاریخ تولد"
										/>-->

					<q-input
						filled
						label="تاریخ تولد"
						class="q-mb-md"
						v-model="user.birthDay"
						mask="date"
						:rules="['date', (val) => !!val || 'این فیلد الزامی است.']"
					>
						<template v-slot:append>
							<q-icon name="event" class="cursor-pointer">
								<q-popup-proxy
									cover
									transition-show="scale"
									transition-hide="scale"
								>
									<q-date
										dir="rtl"
										v-model="user.birthDay"
										calendar="persian"
										today-btn
										:options="options"
									/>
								</q-popup-proxy>
							</q-icon>
						</template>
					</q-input>

					<q-input
						filled
						label="کد ملی"
						class="q-mb-md"
						v-model="user.nationalCode"
						:rules="[(val) => !!val || 'این فیلد الزامی است.', justNumber]"
						maxlength="10"
					/>

					<div dir="rtl" class="q-gutter-sm q-mb-md">
						<q-radio v-model="user.male" :val="true" label="آفا" />
						<q-radio v-model="user.male" :val="false" label="خانم" />
					</div>

					<q-btn type="submit" color="blue-5" class="full-width" outline>
						ثبت اطلاعات
					</q-btn>

					<q-banner
						dir="rtl"
						inline-actions
						class="text-white q-mb-md"
						:class="{ 'bg-red': !!err, 'bg-transparent': !err }"
					>
						{{ err }}
					</q-banner>
				</q-form>
			</q-card-section>
		</q-card>
	</q-page>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
// import PersianDate from 'components/PersianDate.vue';
import type { User } from 'src/stores/user.d';
import { useUser } from 'src/stores/user';
import { useRouter } from 'vue-router';
import { useRead, useWrite } from 'src/functions/IO';
import { onMounted, watch } from 'vue';

const user = reactive<User>({
	persianFirstName: '',
	persianLastName: '',
	nationalCode: '',
	birthDay: '',
	male: true,
});

const users = ref<{ value: number; label: string }[]>([]);

const userSelected = ref();
let beforeUsers: User[] = [];

watch(userSelected, (value) => {
	for (const beforeUsersKey in beforeUsers[value.value]) {
		// @ts-ignore
		user[beforeUsersKey] = beforeUsers[value.value][beforeUsersKey];
	}
});

onMounted(() => {
	beforeUsers = useRead('usersData', []);
	for (let i = 0; i < beforeUsers.length; i++) {
		users.value.push({
			value: i,
			label:
				beforeUsers[i].persianFirstName + ' ' + beforeUsers[i].persianLastName,
		});
	}
});

function exitUser() {
	for (const beforeUser of beforeUsers) {
		if (
			beforeUser.persianFirstName + ' ' + beforeUser.persianLastName ==
			user.persianFirstName + ' ' + user.persianLastName
		)
			return true;
	}
	return false;
}

function options(date: string) {
	let a = new Date().toLocaleDateString('fa-IR-u-nu-latn');

	let as = a.split('/');
	for (let i = 0; i < as.length; i++)
		if (as[i].length == 1) as[i] = '0' + as[i];

	return date >= as[0] + '/' + as[1] + '/' + as[2];
}

function justNumber(val: string) {
	return /^[0-9]+$/.test(val) || 'فقط از اعداد استفاده نمایید.';
}

function justPersian(val: string) {
	return (
		/^[\u0600-\u06FF\s]+$/.test(val) ||
		'فقط از حروف فارسی و فاصله استفاده نمایید.'
	);
}

const err = ref('');

const router = useRouter();

function submit() {
	err.value = '';
	if (user.nationalCode.length == 10) {
		useUser().setUser(user);

		if (!exitUser()) useWrite('usersData', user, true);

		router.push({ name: 'get-train' });
	} else err.value = 'کد ملی صحیح نمی باشد.';
}
</script>
