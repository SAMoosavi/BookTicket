<template>
	<q-page class="row items-center justify-evenly">
		<q-card flat class="bg-transparent">
			<q-card-section class="items-center justify-center flex">
				<q-spinner-ball color="blue" size="2em" />
				please wait
				<span v-if="user.getUser().male">Mr.</span>
				<span v-else>Miss.</span>
				<span>{{ user.getFullName() }}</span>
				<q-spinner-ball color="blue" size="2em" />
			</q-card-section>
		</q-card>
	</q-page>
</template>

<script setup lang="ts">
import { useData } from 'stores/data';
import { useToken } from 'stores/token';
import { useUser } from 'stores/user';

const data = useData();
const token = useToken();
const user = useUser();

console.log(
	data.getReserve(),
	data.getData(),
	token.getToken(),
	user.getUser()
);
</script>
