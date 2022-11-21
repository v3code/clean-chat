import type { AxiosError } from 'axios';
import { userStore } from '../user/store';

export function handleError(error: any) {
	if (error?.isAxiosError) {
		return handleAxiosErrors(error as AxiosError);
	}
	return {
		shouldFail: true,
		messages: []
	};
}

function handleAxiosErrors(error: AxiosError) {
	const responseData = error?.response?.data as any; // TODO add type
	switch (error.response.status) {
		case 401:
			userStore.logout();
			return {
				shouldFail: false,
				messages: []
			};
		case 400:
			if (responseData?.detail) {
				return {
					shouldFail: true,
					messages: [responseData?.detail]
				};
			}
			return {
				shouldFail: false,
				messages: []
			};
		default:
			return {
				shouldFail: false,
				messages: []
			};
	}
}
