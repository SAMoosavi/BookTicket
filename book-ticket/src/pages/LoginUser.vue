<template>
	<q-page class="row items-center justify-evenly">
		<q-card
			flat
			class="bg-transparent items-center justify-evenly q-pa-md"
			style="width: 500px"
		>
			<q-card-section class="items-center justify-center flex text-h6">
				مشخصات ورود خود را برای مستر بلیط وارد نمایید.
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
				<q-form dir="ltr" @submit.prevent="submit">
					<q-input
						filled
						color="blue-5"
						label="نام کاربری"
						class="q-mb-md"
						v-model="params.username"
						:rules="[(val) => !!val || 'این فیلد الزامی است.']"
					/>

					<q-input
						filled
						color="blue-5"
						label="رمز ورود"
						class="q-mb-md"
						:rules="[(val) => !!val || 'این فیلد الزامی است.']"
						v-model="params.password"
						:type="isPwd ? 'password' : 'text'"
					>
						<template v-slot:append>
							<q-icon
								:name="isPwd ? 'visibility_off' : 'visibility'"
								class="cursor-pointer"
								@click="isPwd = !isPwd"
							/>
						</template>
					</q-input>

					<q-btn color="blue-5" outline type="submit" class="full-width">
						ورود
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
import { onMounted, reactive, ref, watch } from 'vue';
import { useToken } from 'stores/token';
import { useRouter } from 'vue-router';
import { useData } from 'stores/data';
import { LoginParameters } from 'src/functions/MrBilitApiWrapper.d';
import { useLogin } from 'src/functions/MrBilitApiWrapper';
import { useRead, useWrite } from 'src/functions/IO';

const router = useRouter();

const params = reactive<LoginParameters>({
	username: '',
	password: '',
	Source: 2,
});

const err = ref();

const Data = useData();
const isPwd = ref(true);
const users = ref<{ value: number; label: string }[]>([]);

const userSelected = ref();
let beforeUsers: LoginParameters[] = [];

watch(userSelected, (value) => {
	for (const beforeUsersKey in beforeUsers[value.value]) {
		// @ts-ignore
		params[beforeUsersKey] = beforeUsers[value.value][beforeUsersKey];
	}
});

onMounted(() => {
	beforeUsers = useRead('user', []);
	for (let i = 0; i < beforeUsers.length; i++) {
		users.value.push({
			value: i,
			label: beforeUsers[i].username,
		});
	}
});

function exitUser() {
	for (const beforeUser of beforeUsers) {
		if (beforeUser.username == params.username) return true;
	}
	return false;
}

function submit() {
	err.value = '';

	useLogin(params)
		.then((response) => {
			useToken().setToken(response.data.token);
			if (response.data.token) {
				Data.setEmail(response.data.userEmail);
				Data.setMobile(response.data.userMobile);

				if (!exitUser()) useWrite('user', params, true);

				useWrite('data', Data.getData());
				useWrite('token', response.data.token);

				router.push({ name: 'get-user' });
			} else {
				err.value = response.data.error;
			}
		})
		.catch((error) => {
			console.error(error);
			err.value = 'خطایی رخ داد!!!';
		});
}
</script>
