<script lang="ts">
	import { Button, Checkbox, Modal, Navbar, Spinner, Toggle } from 'flowbite-svelte';
	import { userStore } from '../user/store';
	import IoIosSettings from 'svelte-icons/io/IoIosSettings.svelte';
	import FaSignOutAlt from 'svelte-icons/fa/FaSignOutAlt.svelte';
	import { globalStore } from '../core/global-store';
	import { onDestroy } from 'svelte';
	import { navigate } from 'svelte-navigator';

	let subscriptions = [];

	let userState;
	let globalState;

	let settingsOpen = false;
	let newHideToxic;
	let newHideUnchecked;

	onDestroy(
		userStore.subscribe((state) => {
			userState = state;
			if (newHideToxic !== state?.userData?.hideToxic) {
				newHideToxic = state?.userData?.hideToxic;
			}
			if (newHideUnchecked !== state?.userData?.hideUnchecked) {
				newHideUnchecked = state?.userData?.hideUnchecked;
			}
		})
	);

	onDestroy(
		globalStore.subscribe((value) => {
			globalState = value;
		})
	);

	let settingsLoading = false;

	const onSettingsApply = async () => {
		settingsLoading = true;
		await userStore.updateConfig(newHideToxic, newHideUnchecked);
		settingsLoading = false;
		settingsOpen = false;
	};

	$: disableSettingApply =
		newHideToxic === userState?.userData?.hideToxic &&
		newHideUnchecked === userState?.userData?.hideUnchecked;
</script>

<Modal bind:open={settingsOpen}>
	<h3>Configurations</h3>
	<div class="flex items-stretch flex-col p-4 gap-4">
		<Toggle size="large" bind:checked={newHideToxic}>Hide toxic messages</Toggle>
		<Toggle size="large" bind:checked={newHideUnchecked}>Hide unchecked messages</Toggle>
	</div>
	<div slot="footer">
		<Button on:click={onSettingsApply} disabled={disableSettingApply || settingsLoading}
			><div class="flex flex-row items-center gap-2">
				{#if settingsLoading}
					<Spinner size="4" />
				{/if}
				Apply
			</div></Button
		>
	</div>
</Modal>

<Navbar color="none" class="bg-primary">
	<span class="self-center my-1 md:my-3 whitespace-nowrap text-xl font-semibold text-white">
		Clean chat
	</span>
	{#if userState.isAuthorized}
		<div class="ml-auto flex flex-row gap-4 items-center">
			<Button
				disabled={globalState.isLoading}
				outline
				pill
				color="light"
				on:click={() => (settingsOpen = true)}
			>
				<div class="w-[24px] h-[24px] sm:w-[24px] sm:h-[24px]">
					<IoIosSettings />
				</div>
			</Button>
			<Button
				disabled={globalState.isLoading}
				outline
				pill
				color="light"
				on:click={() => {
					userStore.logout();
					window.location.reload(); // TODO Fix later
				}}
			>
				<div class="w-[24px] h-[24px] sm:w-[24px] sm:h-[24px]">
					<FaSignOutAlt />
				</div>
			</Button>
		</div>
	{/if}
</Navbar>
<slot />
