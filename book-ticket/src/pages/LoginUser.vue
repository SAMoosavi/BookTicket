<template>
	<q-page class="row items-center justify-evenly">
		<q-card flat class="bg-transparent items-center justify-evenly q-pa-md">
			<q-card-section class="items-center justify-center flex text-h6">
				مشخصات ورود خود را برای مستر بلیط وارد نمایید.
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

					<q-btn
						label="ورود"
						color="blue-5"
						outline
						type="submit"
						class="full-width"
					/>

					<q-banner
						dir="rtl"
						inline-actions
						class="text-white q-my-md"
						:class="{ 'bg-red': !!err, 'bg-transparent': !err }"
					>
						{{ err }}
					</q-banner>
				</q-form>
			</q-card-section>
		</q-card>

		<q-btn
			class="absolute-bottom-left q-ma-md"
			round
			color="primary"
			icon="person_search"
			@click="dialog = true"
		/>
		<q-dialog v-model="dialog">
			<q-card class="bg-amber-1 overflow-hidden" style="width: 300px">
				<q-card-section class="column">
					<h3 class="text-h6 text-center">انتخاب کاربر</h3>
					<q-input
						label="جست و جو کاربر"
						v-model="search"
						fill-input
						class="full-width"
					/>
					<transition-group mode="in-out" name="list" tag="div" class="column">
						<q-btn
							v-for="user in users_copy"
							:key="user.label"
							:label="user.label"
							v-close-popup
							class="q-mt-md"
							@click="userSelected = user.value"
							outline
							color="primary"
						/>
					</transition-group>
				</q-card-section>
			</q-card>
		</q-dialog>
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
const dialog = ref(false);
const search = ref<string>();

const Data = useData();
const isPwd = ref(true);
const users = ref<{ value: number; label: string }[]>([]);
const users_copy = ref<{ value: number; label: string }[]>([]);

const userSelected = ref();
let beforeUsers: LoginParameters[] = [];

watch(userSelected, (value) => {
	for (const beforeUsersKey in beforeUsers[value]) {
		// @ts-ignore
		params[beforeUsersKey] = beforeUsers[value][beforeUsersKey];
	}
});

watch(search, (value) => {
	if (value) {
		users_copy.value = [];
		for (const user of users.value) {
			if (user.label.indexOf(value) >= 0) users_copy.value.push(user);
		}
	} else users_copy.value = users.value;
});

onMounted(() => {
	beforeUsers = useRead('user', []);
	for (let i = 0; i < beforeUsers.length; i++) {
		users.value.push({
			value: i,
			label: beforeUsers[i].username,
		});
	}
	users_copy.value = users.value;
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
