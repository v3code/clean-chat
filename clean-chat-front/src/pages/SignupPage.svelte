<script lang="ts">
	import { Input, Button, Label, Spinner } from 'flowbite-svelte';
	import { navigate } from 'svelte-navigator';
	import { handleRegistration } from '../user/service';

	let email = '';
	let password = '';
	let username = '';

	let isLoading = false;

	const onSignup = async () => {
		isLoading = true;
		await handleRegistration(email, username, password);
		isLoading = false;
		navigate('/login');
	};

	$: submitDisabled = !(email && password && password);
</script>

<div class="flex gap-5 mt-8 flex-col w-full md:p-0 p-3 md:w-[620px] mx-auto">
	<Label>
		<span>Username *</span>
		<Input
			disabled={isLoading}
			placeholder="Enter your username here"
			size="md"
			bind:value={username}
		/>
	</Label>
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
	<Button class="mt-2" disabled={submitDisabled || isLoading} on:click={onSignup} color="blue">
		<div class="flex flex-row items-center gap-2">
			{#if isLoading}
				<Spinner size="4" />
			{/if}
			Signup
		</div>
	</Button>
	<Button
		disabled={isLoading}
		on:click={() => navigate('/login')}
		color="alternative"
		variant="outlined"
	>
		Login
	</Button>
</div>
