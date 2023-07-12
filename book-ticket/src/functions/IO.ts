export function useWrite(key: string, data: any, concat = false) {
	if (concat) {
		let lastData = JSON.parse(<string>localStorage.getItem(key));
		if (!lastData) lastData = [];
		if (Array.isArray(data)) data = [...lastData, ...data];
		else data = [...lastData, data];
	}
	localStorage.setItem(key, JSON.stringify(data));
}

export function useRead(key: string, defaultValue: any) {
	let data = JSON.parse(<string>localStorage.getItem(key));
	if (!data) data = defaultValue;
	return data;
}
