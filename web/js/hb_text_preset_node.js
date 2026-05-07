import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "HB.TextPresetFINAL_CLEAR",

    async beforeRegisterNodeDef(nodeType, nodeData) {

        if (nodeData.name !== "HB_TextPresetSwitch") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {

            onNodeCreated?.apply(this, arguments);

            if (this.__hb_done) return;
            this.__hb_done = true;

            // =========================
            // DEFAULT PRESETS
            // =========================
            this._defaultPresets = [
                { name: "HD (~720)", value: "1" },
                { name: "HD+ (~900)", value: "2" },
                { name: "FHD (~1080)", value: "3" },
                { name: "FHD+ (~1200)", value: "4" },
                { name: "2K (~1440)", value: "5" },
                { name: "3K (~1800)", value: "6" },
                { name: "4K (~2160)", value: "7" },
            ];

            // =========================
            // TRUE HIDDEN STORAGE
            // =========================
            this._store = this.addWidget(
                "hidden",
                "presets_json",
                "",
                () => {}
            );

            this._store.serialize = true;

            this._selectedStore = this.addWidget(
                "hidden",
                "selected_preset",
                "",
                () => {}
            );

            this._selectedStore.serialize = true;

            // =========================
            // BUILD UI
            // =========================
            this._buildUI = () => {

                let presets = this._defaultPresets;

                if (this._store.value) {

                    try {

                        const parsed =
                            JSON.parse(this._store.value);

                        presets = parsed;

                    } catch {}
                }
                else {

                    this._store.value =
                        JSON.stringify(
                            this._defaultPresets
                        );
                }

                // =========================
                // PRESERVE LABEL
                // =========================
                let previousLabel = "preset";

                const existing = this.widgets.find(
                    w => w.name === "preset"
                );

                if (existing) {

                    previousLabel =
                        existing.label ||
                        existing.name ||
                        "preset";

                    this.widgets.splice(
                        this.widgets.indexOf(existing),
                        1
                    );
                }

                const presetNames =
                    presets.map(p => p.name);

                let selectedName =
                    this._selectedStore.value;

                if (!presetNames.includes(selectedName)) {

                    selectedName =
                        presetNames[0] || "";
                }

                // =========================
                // CREATE COMBO
                // =========================
                const combo = this.addWidget(
                    "combo",
                    "preset",
                    selectedName,
                    (value) => {

                        this._selectedStore.value =
                            value;

                        this.setDirtyCanvas(
                            true,
                            true
                        );
                    },
                    {
                        values: presetNames
                    }
                );

                combo.label = previousLabel;

                combo.value = selectedName;

                // =========================
                // SERIALIZE OUTPUT VALUE
                // =========================
                combo.serializeValue = () => {

                    let current;

                    try {

                        current =
                            JSON.parse(
                                this._store.value
                            );

                    } catch {

                        current = presets;
                    }

                    const found = current.find(
                        p => p.name === combo.value
                    );

                    return found
                        ? found.value
                        : "";
                };
            };

            // =========================
            // CONFIGURE FIX
            // =========================
            const originalConfigure =
                this.configure;

            this.configure = function () {

                originalConfigure?.apply(
                    this,
                    arguments
                );

                this._buildUI();
            };

            this._buildUI();

            // =========================
            // MANAGE BUTTON
            // =========================
            this.addWidget(
                "button",
                "Manage",
                null,
                () => {

                    const dialog =
                        new app.ui.dialog.constructor();

                    dialog.element.classList.add(
                        "comfy-settings"
                    );

                    const container =
                        document.createElement("div");

                    container.style.display = "flex";
                    container.style.flexDirection =
                        "column";
                    container.style.gap = "10px";

                    // =========================
                    // TOP BUTTONS
                    // =========================
                    const addBtn =
                        document.createElement(
                            "button"
                        );

                    addBtn.textContent =
                        "Add New";

                    const clearBtn =
                        document.createElement(
                            "button"
                        );

                    clearBtn.textContent =
                        "Clear All";

                    clearBtn.style.color = "red";

                    container.appendChild(addBtn);
                    container.appendChild(clearBtn);

                    // =========================
                    // ROWS CONTAINER
                    // =========================
                    const rowsContainer =
                        document.createElement(
                            "div"
                        );

                    rowsContainer.style.display =
                        "grid";

                    rowsContainer.style.gridTemplateColumns =
                        "1fr 1fr auto";

                    rowsContainer.style.gap =
                        "10px";

                    container.appendChild(
                        rowsContainer
                    );

                    let rows = [];

                    // =========================
                    // REFRESH ROWS UI
                    // =========================
                    function refreshRowsUI() {

                        rowsContainer.innerHTML = "";

                        rows.forEach(r => {

                            rowsContainer.appendChild(
                                r.n
                            );

                            rowsContainer.appendChild(
                                r.v
                            );

                            const controls =
                                document.createElement(
                                    "div"
                                );

                            controls.style.display =
                                "flex";

                            controls.style.gap =
                                "4px";

                            controls.appendChild(
                                r.up
                            );

                            controls.appendChild(
                                r.down
                            );

                            controls.appendChild(
                                r.del
                            );

                            rowsContainer.appendChild(
                                controls
                            );
                        });
                    }

                    // =========================
                    // ADD ROW
                    // =========================
                    function addRow(
                        name = "",
                        value = ""
                    ) {

                        const n =
                            document.createElement(
                                "input"
                            );

                        n.value = name;

                        const v =
                            document.createElement(
                                "input"
                            );

                        v.value = value;

                        const up =
                            document.createElement(
                                "button"
                            );

                        up.textContent = "▲";

                        const down =
                            document.createElement(
                                "button"
                            );

                        down.textContent = "▼";

                        const del =
                            document.createElement(
                                "button"
                            );

                        del.textContent = "✕";

                        const obj = {
                            n,
                            v,
                            up,
                            down,
                            del
                        };

                        rows.push(obj);

                        // UP
                        up.onclick = () => {

                            const index =
                                rows.indexOf(obj);

                            if (index <= 0)
                                return;

                            [
                                rows[index - 1],
                                rows[index]
                            ] = [
                                rows[index],
                                rows[index - 1]
                            ];

                            refreshRowsUI();
                        };

                        // DOWN
                        down.onclick = () => {

                            const index =
                                rows.indexOf(obj);

                            if (
                                index >=
                                rows.length - 1
                            )
                                return;

                            [
                                rows[index + 1],
                                rows[index]
                            ] = [
                                rows[index],
                                rows[index + 1]
                            ];

                            refreshRowsUI();
                        };

                        // DELETE
                        del.onclick = () => {

                            rows =
                                rows.filter(
                                    r => r !== obj
                                );

                            refreshRowsUI();
                        };

                        refreshRowsUI();
                    }

                    // =========================
                    // LOAD CURRENT PRESETS
                    // =========================
                    let current;

                    try {

                        current =
                            JSON.parse(
                                this._store.value
                            );

                    } catch {

                        current =
                            this._defaultPresets;
                    }

                    current.forEach(p =>
                        addRow(
                            p.name,
                            p.value
                        )
                    );

                    // ADD NEW
                    addBtn.onclick = () =>
                        addRow();

                    // CLEAR ALL
                    clearBtn.onclick = () => {

                        rowsContainer.innerHTML =
                            "";

                        rows = [];
                    };

                    // =========================
                    // SAVE
                    // =========================
                    const save =
                        document.createElement(
                            "button"
                        );

                    save.textContent = "SAVE";

                    save.onclick = () => {

                        const newData = [];

                        rows.forEach(r => {

                            if (
                                r.n.value &&
                                r.v.value
                            ) {

                                newData.push({
                                    name:
                                        r.n.value,
                                    value:
                                        r.v.value
                                });
                            }
                        });

                        this._store.value =
                            JSON.stringify(
                                newData
                            );

                        // validate selection
                        const currentSelected =
                            this._selectedStore
                                .value;

                        const stillExists =
                            newData.find(
                                p =>
                                    p.name ===
                                    currentSelected
                            );

                        if (!stillExists) {

                            this._selectedStore.value =
                                newData[0]?.name ||
                                "";
                        }

                        dialog.close();

                        this._buildUI();

                        this.setDirtyCanvas(
                            true,
                            true
                        );
                    };

                    container.appendChild(save);

                    // SHOW DIALOG
                    dialog.show("");

                    dialog.textElement.append(
                        container
                    );
                }
            );
        };
    }
});