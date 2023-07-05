<template>
	<q-page class="row items-center justify-evenly">
		<q-form
			class="items-center justify-evenly q-pa-md"
			@submit.prevent="submit"
			style="width: 500px"
		>
			<q-banner
				dir="rtl"
				v-if="!!err"
				inline-actions
				class="text-white q-mb-md bg-red"
			>
				{{ err }}
			</q-banner>

			<q-input
				filled
				label="Persian First Name"
				class="q-mb-md"
				dir="rtl"
				v-model="user.persianFirstName"
				:rules="[justPersian]"
			/>

			<q-input
				filled
				label="Persian Last Name"
				class="q-mb-md"
				dir="rtl"
				v-model="user.persianLastName"
				:rules="[justPersian]"
			/>

			<persian-date
				@value="
					(val) => {
						user.birthDay = val;
					}
				"
				label="Birth Day"
			/>

			<q-input
				filled
				label="National Code"
				class="q-mb-md"
				v-model="user.nationalCode"
				:rules="[justNumber]"
				maxlength="10"
			/>

			<div class="q-gutter-sm q-mb-md">
				<q-radio v-model="user.male" :val="true" label="male" />
				<q-radio v-model="user.male" :val="false" label="female" />
			</div>

			<q-btn type="submit" color="blue-4" class="full-width" outline
				>send
			</q-btn>
		</q-form>
	</q-page>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import PersianDate from 'components/PersianDate.vue';
import type { User } from 'src/stores/user.d';
import { useUser } from 'src/stores/user';
import { useRouter } from 'vue-router';

const user = reactive<User>({
	persianFirstName: '',
	persianLastName: '',
	nationalCode: '',
	birthDay: '',
	male: true,
});

function justNumber(val: string) {
	return /^[0-9]+$/.test(val) || 'just numbers';
}

function justPersian(val: string) {
	return /^[\u0600-\u06FF\s]+$/.test(val) || 'just persian';
}

const err = ref('');

const router = useRouter();

function submit() {
	err.value = '';
	if (user.nationalCode.length == 10) {
		useUser().setUser(user);

		router.push({ name: 'get-train' });
	} else err.value = 'national CODE is not correct';
}
</script>
