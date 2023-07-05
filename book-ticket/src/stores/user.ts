import { defineStore } from 'pinia';
import { reactive } from 'vue';
import type { User } from './user.d';

export const useUser = defineStore('user', () => {
	const user = reactive<User>({
		persianFirstName: '',
		persianLastName: '',
		nationalCode: '',
		birthDay: '',
		male: true,
	});

	function getFullName() {
		return user.persianFirstName + ' ' + user.persianLastName;
	}

	function setUser(val: User) {
		for (const userKey in user) {
			// @ts-ignore
			user[userKey] = val[userKey];
		}
	}

	function getUser(): User {
		return user;
	}

	return { setUser, getUser, getFullName };
});
