import axios from 'axios';
import { getToken } from '../core/services/token-service';
import { ENV } from '../env';

export function withAuthHeader() {
	const token = getToken();
	if (!token) {
		return {};
	}
	return {
		Authorization: `Bearer ${token}`
	};
}

export const userApi = axios.create({
	baseURL: ENV.BASE_API_ENDPOINT + '/user',
	withCredentials: true
});
