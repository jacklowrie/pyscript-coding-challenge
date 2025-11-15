import {EditorState} from "@codemirror/state";
import {EditorView, basicSetup} from "@codemirror/view";
import {python} from "@codemirror/lang-python";

// Expose a function for PyScript or other code
export function createCodeMirror(textareaId) {
    const element = document.getElementById(textareaId);
    const state = EditorState.create({
        doc: element.value,
        extensions: [basicSetup, python()]
    });
    const view = new EditorView({
        state,
        parent: element.parentNode
    });
    element.style.display = "none"; // hide original textarea
    return view;
}
