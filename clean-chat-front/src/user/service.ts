import { globalStore } from '../core/global-store';
import { userApi, withAuthHeader } from './api';
import { setToken } from '../core/services/token-service';

export const handleLogin = async (email: string, password: string) => {
	const response = await userApi.post('/login', {
		email,
		password
	});
	const userData = response.data.user;
	const token = response.data.token;
	setToken(token);
	return userData;
};

export const handleGetUser = async () => {
	const response = await userApi.get('/', {
		headers: {
			...withAuthHeader()
		}
	});
	return response.data;
};

export const handleUpdateConfig = async (hideToxic: boolean, hideUnchecked: boolean) => {
	const response = await userApi.patch(
		'/config',
		{
			hide_toxic: hideToxic,
			hide_unchecked: hideUnchecked
		},
		{
			headers: {
				...withAuthHeader()
			}
		}
	);
	return response.data;
};

export const handleRegistration = async (email: string, username: string, password: string) => {
	await userApi.post('/register', {
		email,
		username,
		password
	});
};
