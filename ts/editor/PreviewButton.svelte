<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="typescript">
    import { bridgeCommand } from "lib/bridgecommand";
    import * as tr from "lib/i18n";
    import { withButton } from "components/helpers";

    import WithShortcut from "components/WithShortcut.svelte";
    import LabelButton from "components/LabelButton.svelte";
</script>

<WithShortcut shortcut={"Control+Shift+P"} let:createShortcut let:shortcutLabel>
    <LabelButton
        tooltip={tr.browsingPreviewSelectedCard({ val: shortcutLabel })}
        on:click={() => bridgeCommand("preview")}
        on:mount={withButton(createShortcut)}
    >
        {tr.actionsPreview()}
    </LabelButton>
</WithShortcut>
