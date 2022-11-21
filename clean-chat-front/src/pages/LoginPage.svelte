<script lang="ts">
	import { Input, Button, Label, Spinner } from 'flowbite-svelte';
	import { userStore } from '../user/store';
	import { navigate } from 'svelte-navigator';

	let email = '';
	let password = '';

	let isLoading = false;

	const onLogin = async () => {
		isLoading = true;
		await userStore.login(email, password);
		isLoading = false;
		navigate('/chat') // TODO replace this clutch with better solution
	};

	$: submitDisabled = !(email && password);
</script>

<div class="flex gap-5 mt-8 flex-col w-full md:p-0 p-3 md:w-[620px] mx-auto">
	<Label>
		<span>Email *</span>
		<Input
			disabled={isLoading}
			type="email"
			placeholder="Enter your email here"
			size="md"
			bind:value={email}
		/>
	</Label>
	<Label>
		<span>Password *</span>
		<Input
			disabled={isLoading}
			type="password"
			placeholder="Enter your password here"
			size="md"
			bind:value={password}
		/>
	</Label>
	<Button disabled={submitDisabled || isLoading} on:click={onLogin} color="blue">
		<div class="flex flex-row items-center gap-2">
			{#if isLoading}
				<Spinner size="4" />
			{/if}
			Login
		</div>
	</Button>
	<Button
		disabled={isLoading}
		on:click={() => navigate('/signup')}
		color="alternative"
		variant="outlined"
	>
		Signup
	</Button>
</div>
