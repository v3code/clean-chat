<script lang="ts">
	import { globalStore } from '../core/global-store';
	import { handleError } from './error-handlers';
	import { Toast } from 'flowbite-svelte';
	import { slide } from 'svelte/transition';
	import FaExclamationTriangle from 'svelte-icons/fa/FaExclamationTriangle.svelte'
	import { onDestroy } from 'svelte';

	let globalError;
	onDestroy(globalStore.subscribe(({ error }) => (globalError = error)));

	$: errorState = globalError
		? handleError(globalError)
		: {
				shouldFail: true,
				messages: []
		  };
</script>

{#each errorState.messages as toast}
	<Toast color="red" class='absolute' transition={slide}>
		<FaExclamationTriangle slot='icon'></FaExclamationTriangle>
		{toast}
	</Toast>
{/each}


<slot />
