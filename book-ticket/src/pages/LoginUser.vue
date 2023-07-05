<template>
	<q-page class="row items-center justify-evenly">
		<q-card flat class="bg-transparent">
			<q-card-section class="items-center justify-center flex text-h6">
				مشخصات ورود خود را برای مستر بلیط وارد نمایید.
			</q-card-section>
			<q-card-section>
				<q-form
					class="items-center justify-evenly"
					style="width: 500px"
					@submit.prevent="submit"
				>
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

const err = ref();

const Data = useData();
const isPwd = ref(true);

function submit() {
	err.value = '';

	useLogin(params)
		.then((response) => {
			useToken().setToken(response.data.token);
			if (response.data.token) {
				Data.setEmail(response.data.userEmail);
				Data.setMobile(response.data.userMobile);

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
