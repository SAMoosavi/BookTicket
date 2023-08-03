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
				<q-item-section class="text-grey"> چیزی یافت نشد</q-item-section>
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
		value: 670,
		label: 'آب نیل',
	},
	{
		value: 90016,
		label: 'آب نیل',
	},
	{
		value: 337,
		label: 'آباده',
	},
	{
		value: 7,
		label: 'آبیک',
	},
	{
		value: 4,
		label: 'آبگرم',
	},
	{
		value: 9,
		label: 'آتش بغ',
	},
	{
		value: 224,
		label: 'آزادور',
	},
	{
		value: 290,
		label: 'آنکارا',
	},
	{
		value: 14,
		label: 'اراک',
	},
	{
		value: 261,
		label: 'اردکان',
	},
	{
		value: 510,
		label: 'ارسنجان',
	},
	{
		value: 448,
		label: 'ارومیه',
	},
	{
		value: 18,
		label: 'ازنا',
	},
	{
		value: 20,
		label: 'اسفراین',
	},
	{
		value: 301,
		label: 'اسلامشهر',
	},
	{
		value: 237,
		label: 'اشکذر',
	},
	{
		value: 201,
		label: 'اشکذر',
	},
	{
		value: 21,
		label: 'اصفهان',
	},
	{
		value: 387,
		label: 'اقلید',
	},
	{
		value: 51,
		label: 'الوند',
	},
	{
		value: 22,
		label: 'امروان',
	},
	{
		value: 24,
		label: 'اندیمشک',
	},
	{
		value: 25,
		label: 'اهواز',
	},
	{
		value: 450,
		label: 'اینچه برون',
	},
	{
		value: 28,
		label: 'بادرود',
	},
	{
		value: 30,
		label: 'بافق',
	},
	{
		value: 383,
		label: 'بجستان',
	},
	{
		value: 76,
		label: 'بستان آباد',
	},
	{
		value: 34,
		label: 'بکران',
	},
	{
		value: 299,
		label: 'بم',
	},
	{
		value: 36,
		label: 'بندرترکمن',
	},
	{
		value: 37,
		label: 'بندرعباس',
	},
	{
		value: 226,
		label: 'بهاباد',
	},
	{
		value: 43,
		label: 'بیابانک',
	},
	{
		value: 44,
		label: 'بیشه',
	},
	{
		value: 54,
		label: 'تاکستان',
	},
	{
		value: 55,
		label: 'تبریز',
	},
	{
		value: 449,
		label: 'تجرک',
	},
	{
		value: 251,
		label: 'تربت حیدریه',
	},
	{
		value: 912,
		label: 'تربیت معلم',
	},
	{
		value: 59,
		label: 'تنگ هفت',
	},
	{
		value: 1,
		label: 'تهران',
	},
	{
		value: 56,
		label: 'تپه سفید',
	},
	{
		value: 287,
		label: 'جاجرم ',
	},
	{
		value: 61,
		label: 'جاجرم',
	},
	{
		value: 221,
		label: 'جلفا',
	},
	{
		value: 351,
		label: 'جمکران',
	},
	{
		value: 62,
		label: 'جوین',
	},
	{
		value: 513,
		label: 'خاش',
	},
	{
		value: 143,
		label: 'خاوران(تبریز)',
	},
	{
		value: 69,
		label: 'خراسانک',
	},
	{
		value: 71,
		label: 'خرم دره',
	},
	{
		value: 70,
		label: 'خرم پی',
	},
	{
		value: 72,
		label: 'خرمشهر',
	},
	{
		value: 369,
		label: 'خواف',
	},
	{
		value: 75,
		label: 'دامغان',
	},
	{
		value: 78,
		label: 'دورود',
	},
	{
		value: 285,
		label: 'رازی',
	},
	{
		value: 344,
		label: 'رباط کریم',
	},
	{
		value: 451,
		label: 'رشت',
	},
	{
		value: 373,
		label: 'زادمحمود',
	},
	{
		value: 259,
		label: 'زاهدان',
	},
	{
		value: 92,
		label: 'زرند',
	},
	{
		value: 96,
		label: 'زرین دشت',
	},
	{
		value: 97,
		label: 'زنجان',
	},
	{
		value: 239,
		label: 'زواره',
	},
	{
		value: 100,
		label: 'ساری',
	},
	{
		value: 65,
		label: 'ساوه',
	},
	{
		value: 105,
		label: 'سبزوار',
	},
	{
		value: 48,
		label: 'سراوان',
	},
	{
		value: 83,
		label: 'سربندر',
	},
	{
		value: 234,
		label: 'سرخس',
	},
	{
		value: 257,
		label: 'سعادت شهر',
	},
	{
		value: 115,
		label: 'سلماس',
	},
	{
		value: 116,
		label: 'سمنان',
	},
	{
		value: 120,
		label: 'سنخواست',
	},
	{
		value: 123,
		label: 'سهند',
	},
	{
		value: 121,
		label: 'سوادکوه',
	},
	{
		value: 125,
		label: 'سیرجان',
	},
	{
		value: 128,
		label: 'سیمین دشت',
	},
	{
		value: 106,
		label: 'سپیددشت',
	},
	{
		value: 129,
		label: 'شازند',
	},
	{
		value: 130,
		label: 'شاهرود',
	},
	{
		value: 133,
		label: 'شرفخانه',
	},
	{
		value: 511,
		label: 'شلمچه',
	},
	{
		value: 264,
		label: 'شهرضا',
	},
	{
		value: 600,
		label: 'شهرکرد',
	},
	{
		value: 135,
		label: 'شوش',
	},
	{
		value: 134,
		label: 'شوشتر',
	},
	{
		value: 255,
		label: 'شیراز',
	},
	{
		value: 144,
		label: 'شیرگاه',
	},
	{
		value: 90031,
		label: 'صفا شهر',
	},
	{
		value: 258,
		label: 'صفاشهر',
	},
	{
		value: 311,
		label: 'طبس',
	},
	{
		value: 148,
		label: 'عجب شیر',
	},
	{
		value: 509,
		label: 'فهرج',
	},
	{
		value: 40,
		label: 'فیروزان',
	},
	{
		value: 154,
		label: 'فیروزکوه',
	},
	{
		value: 156,
		label: 'قائمشهر',
	},
	{
		value: 160,
		label: 'قزوین',
	},
	{
		value: 161,
		label: 'قم',
	},
	{
		value: 403,
		label: 'کارون',
	},
	{
		value: 162,
		label: 'کاشان',
	},
	{
		value: 508,
		label: 'کربلا',
	},
	{
		value: 165,
		label: 'کرج',
	},
	{
		value: 167,
		label: 'کرمان',
	},
	{
		value: 195,
		label: 'کرمانشاه',
	},
	{
		value: 302,
		label: 'ماهشهر',
	},
	{
		value: 249,
		label: 'محمدیه',
	},
	{
		value: 189,
		label: 'مراغه',
	},
	{
		value: 256,
		label: 'مرودشت',
	},
	{
		value: 191,
		label: 'مشهد',
	},
	{
		value: 15,
		label: 'ملایر',
	},
	{
		value: 194,
		label: 'مهاباد',
	},
	{
		value: 86,
		label: 'مهران',
	},
	{
		value: 250,
		label: 'میاندوآب',
	},
	{
		value: 197,
		label: 'میانه',
	},
	{
		value: 198,
		label: 'میبد',
	},
	{
		value: 202,
		label: 'نقاب',
	},
	{
		value: 262,
		label: 'نقده',
	},
	{
		value: 203,
		label: 'نکا',
	},
	{
		value: 206,
		label: 'نیشابور',
	},
	{
		value: 213,
		label: 'هرند',
	},
	{
		value: 215,
		label: 'هشتگرد',
	},
	{
		value: 216,
		label: 'هفت تپه',
	},
	{
		value: 117,
		label: 'همدان',
	},
	{
		value: 295,
		label: 'وان',
	},
	{
		value: 209,
		label: 'ورامین',
	},
	{
		value: 211,
		label: 'ورزنه',
	},
	{
		value: 212,
		label: 'ورسک',
	},
	{
		value: 219,
		label: 'یزد',
	},
	{
		value: 401,
		label: 'پرند',
	},
	{
		value: 50,
		label: 'پل سفید',
	},
	{
		value: 53,
		label: 'پیشوا',
	},
	{
		value: 66,
		label: 'چمسنگر',
	},
	{
		value: 512,
		label: 'کربلا',
	},
	{
		value: 176,
		label: 'گرمسار',
	},
	{
		value: 175,
		label: 'گرگان',
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
