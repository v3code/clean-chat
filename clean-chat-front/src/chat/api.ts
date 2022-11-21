import axios from 'axios';
import { ENV } from '../env';

export const chatApi = axios.create({
	baseURL: ENV.BASE_API_ENDPOINT + '/chat',
	withCredentials: true
});
