<template>
	<q-select
		filled
		v-model="model"
		use-input
		hide-selected
		fill-input
		input-debounce="0"
		:label="label"
		:options="option"
		@filter="filterFn"
		class="full-width"
	>
		<template v-slot:no-option>
			<q-item>
				<q-item-section class="text-grey"> چیزی یافت نشد </q-item-section>
			</q-item>
		</template>
	</q-select>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

defineProps<{ label: string }>();
const emit = defineEmits(['value']);

interface Option {
	label: string;
	value: number;
	disable?: boolean;
}

const options: Option[] = [
	{
		label: 'تهران',
		value: 1,
	},
	{
		label: 'یزد',
		value: 219,
	},
];

const model = ref<Option>({ label: '', value: 0 });
const option = ref(options);

watch(model, (value) => {
	emit('value', options.filter((val) => val.label === value.label)[0].value);
});

function filterFn(val: string, update: (arg0: () => void) => void) {
	// call abort() at any time if you can't retrieve data somehow
	setTimeout(
		() =>
			update(() => {
				if (val === '') {
					option.value = options;
				} else {
					const needle = val.toLowerCase();
					option.value = options.filter(
						(v) => v.label.toLowerCase().indexOf(needle) > -1
					);
				}
			}),
		300
	);
}
</script>