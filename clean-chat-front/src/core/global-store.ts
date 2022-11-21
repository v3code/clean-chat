import { writable } from 'svelte/store';

interface GlobalStoreState {
	isLoading: boolean;
	error: null | Error;
}

const initialState: GlobalStoreState = {
	isLoading: false,
	error: null
};

function createGlobalStore() {
	const { subscribe, update } = writable<GlobalStoreState>(initialState);

	const setError = (error: Error) => update(({ error: _, ...rest }) => ({ error, ...rest }));
	const resetError = () => update(({ error: _, ...rest }) => ({ error: null, ...rest }));
	const setLoading = (isLoading: boolean) =>
		update(({ isLoading: _, ...rest }) => ({ isLoading, ...rest }));

	return {
		subscribe,
		setLoading,
		resetError,
		setError
	};
}

export const globalStore = createGlobalStore();
