<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { createEventDispatcher, getContext } from "svelte";
    import { nightModeKey } from "components/context-keys";

    export let offsetX = 0;
    export let offsetY = 0;

    export let active = false;
    export let activeSize = 5;

    const dispatch = createEventDispatcher();
    const nightMode = getContext(nightModeKey);

    const onPointerdown =
        (north: boolean, west: boolean) =>
        (event: PointerEvent): void => {
            dispatch("pointerclick", { north, west, originalEvent: event });
        };
</script>

<div
    class="d-contents"
    style="--offsetX: {offsetX}px; --offsetY: {offsetY}px; --activeSize: {activeSize}px;"
>
    <div class:nightMode class="bordered" on:mousedown|preventDefault />
    <div
        class:nightMode
        class:active
        class="control nw"
        on:mousedown|preventDefault
        on:pointerdown={onPointerdown(true, true)}
        on:pointermove
    />
    <div
        class:nightMode
        class:active
        class="control ne"
        on:mousedown|preventDefault
        on:pointerdown={onPointerdown(true, false)}
        on:pointermove
    />
    <div
        class:nightMode
        class:active
        class="control sw"
        on:mousedown|preventDefault
        on:pointerdown={onPointerdown(false, true)}
        on:pointermove
    />
    <div
        class:nightMode
        class:active
        class="control se"
        on:mousedown|preventDefault
        on:pointerdown={onPointerdown(false, false)}
        on:pointermove
    />
</div>

<style lang="scss">
    .d-contents {
        display: contents;
    }

    .bordered {
        position: absolute;

        top: calc(0px - var(--activeSize) + var(--offsetY));
        bottom: calc(0px - var(--activeSize) + var(--offsetY));
        left: calc(0px - var(--activeSize) + var(--offsetX));
        right: calc(0px - var(--activeSize) + var(--offsetX));

        pointer-events: none;
        border: 2px dashed black;

        &.nightMode {
            border-color: white;
        }
    }

    .control {
        position: absolute;

        width: var(--activeSize);
        height: var(--activeSize);

        &.active {
            background-color: black;
        }

        &.nightMode {
            border-color: white;

            &.active {
                background-color: white;
            }
        }

        &.nw {
            top: calc(0px - var(--offsetY));
            left: calc(0px - var(--offsetX));

            &.active {
                cursor: nw-resize;
            }
        }

        &.ne {
            top: calc(0px - var(--offsetY));
            right: calc(0px - var(--offsetX));

            &.active {
                cursor: ne-resize;
            }
        }

        &.sw {
            bottom: calc(0px - var(--offsetY));
            left: calc(0px - var(--offsetX));

            &.active {
                cursor: sw-resize;
            }
        }

        &.se {
            bottom: calc(0px - var(--offsetY));
            right: calc(0px - var(--offsetX));

            &.active {
                cursor: se-resize;
            }
        }
    }
</style>
