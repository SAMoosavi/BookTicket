export interface LoginParameters {
	username: string;
	password: string;
	Source: 2;
}


export interface GetAvailableParameters {
	from: number;
	to: number;
	date: string;
	adultCount: 1;
	childCount: 0;
	infantCount: 0;
	exclusive: false;
	availableStatus: "Both";
}
