<script lang="ts">
	import { Spinner } from 'flowbite-svelte';
	import { globalStore } from './core/global-store';
	import Layout from './layout/MainLayout.svelte';
	import { navigate, Router } from 'svelte-navigator';
	import PrivateRoute from './core/components/PrivateRoute.svelte';
	import ChatPage from './pages/ChatPage.svelte';
	import LoginPage from './pages/LoginPage.svelte';
	import SignupPage from './pages/SignupPage.svelte';
	import { userStore } from './user/store';
	import { onDestroy, onMount } from 'svelte';
	import Overlay from './core/components/Overlay.svelte';
	import ErrorBoundary from './error/ErrorBoundary.svelte';


	let globalState;

	let userState;

	onDestroy(globalStore.subscribe((state) => (globalState = state)));
	onDestroy(userStore.subscribe((state) => (userState = state)));

	let isLoading = false;

	onMount(async () => {
		isLoading = true;
		await userStore.initialize();
		isLoading = false;
	});

	$: if (userState.isAuthorized) {
		navigate('/chat');
	} else {
		navigate('/login');
	}
</script>

{#if isLoading}
	<Overlay>
		<Spinner size="20" />
	</Overlay>
{/if}

<ErrorBoundary>
	<Layout>
		<Router>
			<PrivateRoute shouldRedirect={!$userStore.isAuthorized} redirectPath="/login" path="/chat">
				<ChatPage />
			</PrivateRoute>
			<PrivateRoute shouldRedirect={$userStore.isAuthorized} redirectPath="/chat" path="/login">
				<LoginPage />
			</PrivateRoute>
			<PrivateRoute shouldRedirect={$userStore.isAuthorized} redirectPath="/chat" path="/signup">
				<SignupPage />
			</PrivateRoute>
		</Router>
	</Layout>
</ErrorBoundary>
