<template>
	<q-input filled :label="label" v-model="date" mask="date" :rules="['date']">
		<template v-slot:append>
			<q-icon name="event" class="cursor-pointer">
				<q-popup-proxy cover transition-show="scale" transition-hide="scale">
					<q-date
						v-model="date"
						calendar="persian"
						today-btn
						:options="options"
					>
						<div class="row items-center justify-end">
							<q-btn v-close-popup label="Close" color="primary" flat />
						</div>
					</q-date>
				</q-popup-proxy>
			</q-icon>
		</template>
	</q-input>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{ label: string; today?: boolean }>();
const emit = defineEmits(['value']);
const date = ref();

function options(date: string) {
	if (!props.today) return true;

	let a = new Date().toLocaleDateString('fa-IR-u-nu-latn');

	let as = a.split('/');
	for (let i = 0; i < as.length; i++)
		if (as[i].length == 1) as[i] = '0' + as[i];

	return date >= as[0] + '/' + as[1] + '/' + as[2];
}

watch(date, (val) => emit('value', val));
</script>