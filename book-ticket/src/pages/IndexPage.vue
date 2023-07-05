<template>
	<q-page class="row items-center justify-evenly">
		<q-form class="items-center justify-evenly q-pa-md" style="width: 500px">
			{{ fullName }}
			<router-link :to="{ name: 'get-train' }">get train</router-link>
			<q-input
				filled
				label="Persian First Name"
				class="q-mb-md"
				v-model="PersianFirstName"
			/>

			<q-input
				filled
				label="Persian Last Name"
				class="q-mb-md"
				v-model="PersianLastName"
			/>

			<persian-date
				@value="
					(val) => {
						BirthDay = val;
					}
				"
				label="BirthDay"
			/>

			<div class="q-gutter-sm">
				<q-radio v-model="male" :val="true" label="male" />
				<q-radio v-model="male" :val="false" label="female" />
			</div>

			<q-input
				filled
				label="NationalCode"
				class="q-mb-md"
				v-model="NationalCode"
				:rules="[isNumber, len_10]"
			/>
		</q-form>
	</q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import PersianDate from 'components/PersianDate.vue';
import { useData } from 'stores/data';

const fullName = useData().getFullName();

const BirthDay = ref();
const PersianFirstName = ref('');
const PersianLastName = ref('');
const male = ref();
const NationalCode = ref('');

function isNumber(val: string) {
	for (let i = 0; i < val.length; i++) {
		if ('0' > val[i] || val[i] > '9') return false;
	}
}

function len_10(val: string) {
	return val.length == 10;
}
</script>