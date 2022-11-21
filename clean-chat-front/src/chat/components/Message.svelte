<script lang="ts">
	import type { Message } from '../types';
	import { MessageCheckStatus } from '../types';
	import { userStore } from '../../user/store';
	import { onDestroy } from 'svelte';
	import MdDelete from 'svelte-icons/md/MdDelete.svelte';
	import MdEdit from 'svelte-icons/md/MdEdit.svelte';
	import { Button } from 'flowbite-svelte';
	import { globalStore } from '../../core/global-store.js';
	import { chatStore } from '../stores/store.js';

	export let message: Message;
	const baseClasses = 'flex w-[40%] ml-0 flex-col rounded border-1 p-3 bg-gray-200 text-black';
	let toxicClasses = 'bg-red-200 border-red-600 text-red-600';
	let safeClasses = 'bg-green-200 border-green-600 text-green-600';
	let userClasses = 'bg-blue-200 border-blue-600 text-blue-600 self-end';
	let messageClass = baseClasses;

	let userState;
	let chatState;

	onDestroy(userStore.subscribe((v) => (userState = v)));
	onDestroy(chatStore.subscribe((v) => (chatState = v)));

	$: {
		const classes = [baseClasses];
		if (message.author.id === userState?.userData?.id) {
			classes.push(userClasses);
		} else if (message.type === MessageCheckStatus.TOXIC) {
			classes.push(toxicClasses);
		} else if (message.type === MessageCheckStatus.SAFE) {
			classes.push(safeClasses);
		}

		messageClass = classes.join(' ');
	}
</script>

<div class={messageClass}>
	<span class="text-md">{message.author.username}</span>
	<span class="text-sm">{message.created}</span>
	<p class="text-lg p-4">{message.content}</p>
	{#if message.author.id === $userStore?.userData?.id}
		<div class="p-1 ml-auto flex flex-row gap-1">
<!--			<Button size="sm" disabled={$globalStore.isLoading} outline pill color="dark">-->
<!--				<div class="w-[18px] h-[18px]">-->
<!--					<MdEdit />-->
<!--				</div>-->
<!--			</Button>-->
			<Button
				size="sm"
				disabled={$globalStore.isLoading}
				on:click={() => chatStore.deleteMessage(chatState?.currentChannel?.id, message.id)}
				outline
				pill
				color="dark"
			>
				<div class="w-[18px] h-[18px]">
					<MdDelete />
				</div>
			</Button>
		</div>
	{/if}
</div>
