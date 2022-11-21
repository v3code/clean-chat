import { writable } from 'svelte/store';
import { deleteToken } from '../core/services/token-service';
import { handleGetUser, handleLogin, handleRegistration, handleUpdateConfig } from './service';
import { globalStore } from '../core/global-store';
import { transformResponseToUserConfig } from './utils';

const initialState = {
	userData: null,
	isAuthorized: false
};

function createUserStore() {
	const { subscribe, set, update } = writable(initialState);

	const login = async (email: string, password: string) => {
		try {
			globalStore.resetError();
			const userData = await handleLogin(email, password);
			set({ userData: transformResponseToUserConfig(userData), isAuthorized: true });
		} catch (e) {
			globalStore.setError(e);
		}
	};

	const updateConfig = async (hideToxic: boolean, hideUnchecked: boolean) => {
		try {
			globalStore.resetError();
			const userData = await handleUpdateConfig(hideToxic, hideUnchecked);
			set({ userData: transformResponseToUserConfig(userData), isAuthorized: true });
		} catch (e) {
			globalStore.setError(e);
		}
	};

	const register = async (email: string, username: string, password: string) => {
		try {
			globalStore.resetError();
			await handleRegistration(email, username, password);
		} catch (e) {
			globalStore.setError(e);
		}
	};

	const logout = () => {
		set({ ...initialState, isAuthorized: false });
		deleteToken();
	};

	const initialize = async () => {
		try {
			globalStore.resetError();
			const userData = await handleGetUser();
			if (userData) {
				set({ userData: transformResponseToUserConfig(userData), isAuthorized: true });
			}
		} catch (e) {
			globalStore.setError(e);
		}
	};

	return {
		subscribe,
		update,
		set,
		login,
		logout,
		initialize,
		register,
		updateConfig
	};
}

export const userStore = createUserStore();
