<template>
	<q-page class="row items-center justify-evenly">
		<q-form
			class="items-center justify-evenly"
			style="width: 500px"
			@submit.prevent="submit"
		>
			<q-banner
				dir="rtl"
				v-if="!!msg"
				inline-actions
				class="text-white q-mb-md"
				:class="color"
			>
				{{ msg }}
			</q-banner>

			<q-input
				filled
				color="blue-5"
				label="username"
				class="q-mb-md"
				v-model="params.username"
				:rules="[(val) => !!val || 'Field is required']"
			/>

			<q-input
				filled
				color="blue-5"
				label="password"
				class="q-mb-md"
				type="password"
				:rules="[(val) => !!val || 'Field is required']"
				v-model="params.password"
			/>

			<q-btn color="blue-5" type="submit">ارسال</q-btn>
		</q-form>
	</q-page>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useToken } from 'stores/token';
import { useRouter } from 'vue-router';
import { useData } from 'stores/data';
import { LoginParameters } from 'src/functions/MrBilitApiWrapper.d';
import { useLogin } from 'src/functions/MrBilitApiWrapper';

const router = useRouter();

const params = reactive<LoginParameters>({
	username: '',
	password: '',
	Source: 2,
});

const msg = ref();
const color = ref();

const Data = useData();

function submit() {
	msg.value = '';
	color.value = '';

	useLogin(params)
		.then((response) => {
			useToken().setToken(response.data.token);
			if (response.data.token) {
				msg.value = 'ورود با موفقیت انجام شد!';
				color.value = 'bg-green';
				Data.setEmail(response.data.userEmail);
				Data.setMobile(response.data.userMobile);

				router.push({ name: 'get-user' });
			} else {
				msg.value = response.data.error;
				color.value = 'bg-red';
			}
		})
		.catch((error) => {
			console.error(error);
			msg.value = 'خطایی رخ داد!!!';
			color.value = 'bg-red';
		});
}
</script>
