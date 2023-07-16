const JalaliDate = {
	g_days_in_month: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
	j_days_in_month: [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29],
};

function JToG(
	j_y: number | string,
	j_m: number | string,
	j_d: number | string
): [number | string, number | string, number | string] {
	if (typeof j_y === 'string') {
		j_y = parseInt(j_y);
	}
	if (typeof j_m === 'string') {
		j_m = parseInt(j_m);
	}
	if (typeof j_d === 'string') {
		j_d = parseInt(j_d);
	}
	const jy = j_y - 979;
	const jm = j_m - 1;
	const jd = j_d - 1;

	let j_day_no =
		365 * jy +
		parseInt(String(jy / 33)) * 8 +
		parseInt(String(((jy % 33) + 3) / 4));
	for (let i = 0; i < jm; ++i) j_day_no += JalaliDate.j_days_in_month[i];

	j_day_no += jd;

	let g_day_no = j_day_no + 79;

	let gy = 1600 + 400 * parseInt(String(g_day_no / 146097));
	g_day_no = g_day_no % 146097;

	let leap = true;
	if (g_day_no >= 36525) {
		/* 36525 = 365*100 + 100/4 */
		g_day_no--;
		gy += 100 * parseInt(String(g_day_no / 36524));
		g_day_no = g_day_no % 36524;

		if (g_day_no >= 365) g_day_no++;
		else leap = false;
	}

	gy += 4 * parseInt(String(g_day_no / 1461));
	g_day_no %= 1461;

	if (g_day_no >= 366) {
		leap = false;
		g_day_no--;
		gy += parseInt(String(g_day_no / 365));
		g_day_no = g_day_no % 365;
	}
	let i = 0;
	// @ts-ignore
	for (; g_day_no >= JalaliDate.g_days_in_month[i] + (i == 1 && leap); i++) {
		// @ts-ignore
		g_day_no -= JalaliDate.g_days_in_month[i] + (i == 1 && leap);
	}
	let gm: string | number = i + 1;
	let gd: string | number = g_day_no + 1;

	gm = gm < 10 ? '0' + gm : gm;
	gd = gd < 10 ? '0' + gd : gd;

	return [gy, gm, gd];
}

export function useJalaliToGregorian(date: string, splitterOfOutput='-',splitterOfInput = '/') {
	const dateSplit = date.split(splitterOfInput);
	const jD = JToG(dateSplit[0], dateSplit[1], dateSplit[2]);
	return jD[0] + splitterOfOutput + jD[1] + splitterOfOutput + jD[2];
}
