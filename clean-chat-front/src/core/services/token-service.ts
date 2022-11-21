import { ENV } from '../../env';

const TOKEN_KEY = ENV.TOKEN_KEY;

export function setToken(token: string) {
	localStorage.setItem(TOKEN_KEY, token);
}

export function deleteToken() {
	localStorage.removeItem(TOKEN_KEY);
}

export function getToken() {
	return localStorage.getItem(TOKEN_KEY);
}
