/**
 * A2UI JavaScript Renderer
 * ========================
 * A simple client-side renderer for A2UI JSONL messages.
 * 
 * This renders A2UI components to native HTML elements with styling.
 */

class A2UIRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.components = new Map();  // id -> component definition
        this.dataModel = {};          // data model for bindings
        this.rootId = null;

        if (!this.container) {
            throw new Error(`Container element '${containerId}' not found`);
        }
    }

    /**
     * Process a single A2UI message
     */
    processMessage(message) {
        if (typeof message === 'string') {
            message = JSON.parse(message);
        }

        if (message.surfaceUpdate) {
            this.handleSurfaceUpdate(message.surfaceUpdate);
        } else if (message.dataModelUpdate) {
            this.handleDataModelUpdate(message.dataModelUpdate);
        } else if (message.beginRendering) {
            this.handleBeginRendering(message.beginRendering);
        } else if (message.deleteSurface) {
            this.handleDeleteSurface(message.deleteSurface);
        }
    }

    /**
     * Process multiple messages from JSONL string
     */
    processJSONL(jsonl) {
        const lines = jsonl.trim().split('\n');
        for (const line of lines) {
            if (line.trim()) {
                this.processMessage(line);
            }
        }
    }

    handleSurfaceUpdate(update) {
        const components = update.components || [];
        for (const comp of components) {
            this.components.set(comp.id, comp);
        }
    }

    handleDataModelUpdate(update) {
        this.dataModel = this.deepMerge(this.dataModel, update.contents || {});
        // Re-render if already rendered
        if (this.rootId) {
            this.render();
        }
    }

    handleBeginRendering(begin) {
        this.rootId = begin.root;
        this.render();
    }

    handleDeleteSurface() {
        this.container.innerHTML = '';
        this.components.clear();
        this.dataModel = {};
        this.rootId = null;
    }

    /**
     * Render the component tree
     */
    render() {
        if (!this.rootId) return;

        this.container.innerHTML = '';
        const rootElement = this.renderComponent(this.rootId);
        if (rootElement) {
            this.container.appendChild(rootElement);
        }
    }

    /**
     * Render a single component by ID
     */
    renderComponent(id) {
        const compDef = this.components.get(id);
        if (!compDef) {
            console.warn(`Component '${id}' not found`);
            return null;
        }

        const component = compDef.component;
        const type = Object.keys(component)[0];
        const props = component[type];

        switch (type) {
            case 'Column':
                return this.renderColumn(id, props);
            case 'Row':
                return this.renderRow(id, props);
            case 'Text':
                return this.renderText(id, props);
            case 'Button':
                return this.renderButton(id, props);
            case 'Card':
                return this.renderCard(id, props);
            case 'Image':
                return this.renderImage(id, props);
            case 'TextField':
                return this.renderTextField(id, props);
            case 'Checkbox':
                return this.renderCheckbox(id, props);
            case 'List':
                return this.renderList(id, props);
            default:
                console.warn(`Unknown component type: ${type}`);
                return this.renderUnknown(id, type, props);
        }
    }

    // Component Renderers

    renderColumn(id, props) {
        const div = document.createElement('div');
        div.id = id;
        div.className = 'a2ui-column';
        if (props.alignment) div.classList.add(`align-${props.alignment}`);

        const children = this.getChildren(props);
        for (const childId of children) {
            const child = this.renderComponent(childId);
            if (child) div.appendChild(child);
        }
        return div;
    }

    renderRow(id, props) {
        const div = document.createElement('div');
        div.id = id;
        div.className = 'a2ui-row';
        if (props.alignment) div.classList.add(`align-${props.alignment}`);
        if (props.spacing) div.classList.add(`spacing-${props.spacing}`);

        const children = this.getChildren(props);
        for (const childId of children) {
            const child = this.renderComponent(childId);
            if (child) div.appendChild(child);
        }
        return div;
    }

    renderText(id, props) {
        const hint = props.usageHint || 'body';
        let el;

        switch (hint) {
            case 'h1': el = document.createElement('h1'); break;
            case 'h2': el = document.createElement('h2'); break;
            case 'h3': el = document.createElement('h3'); break;
            case 'caption': el = document.createElement('span'); el.className = 'caption'; break;
            default: el = document.createElement('p');
        }

        el.id = id;
        el.className = `a2ui-text ${hint}`;
        el.textContent = this.resolveValue(props.text);
        return el;
    }

    renderButton(id, props) {
        const btn = document.createElement('button');
        btn.id = id;
        btn.className = `a2ui-button ${props.style || 'primary'}`;
        btn.textContent = this.resolveValue(props.label);

        if (props.disabled && this.resolveValue(props.disabled) === 'true') {
            btn.disabled = true;
        }

        if (props.action) {
            btn.onclick = () => this.handleAction(props.action, id);
        }

        return btn;
    }

    renderCard(id, props) {
        const div = document.createElement('div');
        div.id = id;
        div.className = `a2ui-card elevation-${props.elevation || 'medium'}`;

        if (props.child) {
            const child = this.renderComponent(props.child);
            if (child) div.appendChild(child);
        }

        return div;
    }

    renderImage(id, props) {
        const img = document.createElement('img');
        img.id = id;
        img.className = 'a2ui-image';
        img.src = this.resolveValue(props.url);
        if (props.alt) img.alt = this.resolveValue(props.alt);
        return img;
    }

    renderTextField(id, props) {
        const wrapper = document.createElement('div');
        wrapper.className = 'a2ui-textfield-wrapper';

        if (props.label) {
            const label = document.createElement('label');
            label.textContent = this.resolveValue(props.label);
            label.htmlFor = id;
            wrapper.appendChild(label);
        }

        const input = document.createElement('input');
        input.type = props.type || 'text';
        input.id = id;
        input.className = 'a2ui-textfield';
        if (props.placeholder) input.placeholder = this.resolveValue(props.placeholder);
        if (props.value) input.value = this.resolveValue(props.value);

        if (props.action) {
            input.onchange = (e) => this.handleAction(props.action, id, { value: e.target.value });
        }

        wrapper.appendChild(input);
        return wrapper;
    }

    renderCheckbox(id, props) {
        const wrapper = document.createElement('div');
        wrapper.className = 'a2ui-checkbox-wrapper';

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = id;
        input.className = 'a2ui-checkbox';
        if (props.checked) input.checked = this.resolveValue(props.checked) === 'true';

        if (props.action) {
            input.onchange = (e) => this.handleAction(props.action, id, { checked: e.target.checked });
        }

        const label = document.createElement('label');
        label.htmlFor = id;
        label.textContent = this.resolveValue(props.label);

        wrapper.appendChild(input);
        wrapper.appendChild(label);
        return wrapper;
    }

    renderList(id, props) {
        const div = document.createElement('div');
        div.id = id;
        div.className = 'a2ui-list';

        // Template-based rendering
        if (props.children?.template) {
            const template = props.children.template;
            const source = this.resolveValue(template.source);

            if (Array.isArray(source)) {
                for (let i = 0; i < source.length; i++) {
                    // For now, simple list items
                    const item = document.createElement('div');
                    item.className = 'a2ui-list-item';
                    item.textContent = JSON.stringify(source[i]);
                    div.appendChild(item);
                }
            }
        }

        return div;
    }

    renderUnknown(id, type, props) {
        const div = document.createElement('div');
        div.id = id;
        div.className = 'a2ui-unknown';
        div.innerHTML = `<em>Unknown: ${type}</em>`;
        return div;
    }

    // Helpers

    getChildren(props) {
        if (props.children?.explicitList) {
            return props.children.explicitList;
        }
        return [];
    }

    resolveValue(value) {
        if (!value) return '';
        if (value.literalString !== undefined) {
            return value.literalString;
        }
        if (value.path) {
            return this.getPath(this.dataModel, value.path);
        }
        return value;
    }

    getPath(obj, path) {
        const parts = path.split('.');
        let current = obj;
        for (const part of parts) {
            if (current === undefined || current === null) return '';
            current = current[part];
        }
        return current !== undefined ? String(current) : '';
    }

    deepMerge(target, source) {
        const result = { ...target };
        for (const key in source) {
            if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
                result[key] = this.deepMerge(result[key] || {}, source[key]);
            } else {
                result[key] = source[key];
            }
        }
        return result;
    }

    // Event Handling

    handleAction(action, componentId, data = {}) {
        const event = {
            userAction: {
                action: {
                    name: action.name,
                    componentId: componentId
                },
                data: data
            }
        };

        console.log('Action triggered:', event);

        // Dispatch custom event for the application to handle
        this.container.dispatchEvent(new CustomEvent('a2ui:action', {
            detail: event,
            bubbles: true
        }));

        // If onAction callback is set, call it
        if (this.onAction) {
            this.onAction(event);
        }
    }

    /**
     * Connect to SSE endpoint for streaming updates
     */
    connectSSE(url) {
        const eventSource = new EventSource(url);

        eventSource.addEventListener('a2ui', (e) => {
            this.processMessage(e.data);
        });

        eventSource.addEventListener('message', (e) => {
            this.processMessage(e.data);
        });

        eventSource.onerror = (e) => {
            console.error('SSE connection error:', e);
        };

        return eventSource;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = A2UIRenderer;
}
