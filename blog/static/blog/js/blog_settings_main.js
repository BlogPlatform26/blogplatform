document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll('input[name="design"]');

    radios.forEach(radio => {
        radio.addEventListener("change", function () {
            document.querySelectorAll(".design-box").forEach(box => {
                box.classList.remove("active-design");
            });

            this.closest(".design-card")
                .querySelector(".design-box")
                .classList.add("active-design");
        });
    });

    const addQuizBtn = document.getElementById("addQuizOption");
    const quizOptions = document.getElementById("quizOptions");

    if (addQuizBtn && quizOptions) {
        addQuizBtn.addEventListener("click", function () {
            const index = quizOptions.querySelectorAll("input[type='text']").length;

            const row = document.createElement("div");
            row.className = "d-flex gap-2 mb-2 align-items-center";
            row.innerHTML = `
                <input type="radio" name="correct_option" value="${index}">
                <input type="text" name="quiz_option" class="form-control" placeholder="Odgovor ${index + 1}">
            `;
            quizOptions.appendChild(row);
        });
    }

    const addPollBtn = document.getElementById("addPollOption");
    const pollOptions = document.getElementById("pollOptions");

    if (addPollBtn && pollOptions) {
        addPollBtn.addEventListener("click", function () {
            const index = pollOptions.querySelectorAll("input[type='text']").length;

            const row = document.createElement("div");
            row.className = "d-flex gap-2 mb-2 align-items-center";
            row.innerHTML = `
                <input type="text" name="poll_option" class="form-control" placeholder="Opcija ${index + 1}">
            `;
            pollOptions.appendChild(row);
        });
    }

const boxLayoutForm = document.getElementById("boxLayoutForm");
const boxLayoutJson = document.getElementById("boxLayoutJson");
const boxLists = document.querySelectorAll(".box-sort-list");
const boxAutoSaveStatus = document.getElementById("boxAutoSaveStatus");

const topLeftCount = document.getElementById("topLeftCount");
const topRightCount = document.getElementById("topRightCount");
const leftColumnCount = document.getElementById("leftColumnCount");
const rightColumnCount = document.getElementById("rightColumnCount");

let draggedItem = null;
let dragOriginContainer = null;
let dragOriginNextSibling = null;
let saveInFlight = false;
let pendingLayout = null;
let savedLayout = JSON.stringify(collectBoxLayout().layout);
let dragSnapshot = null;
let dragCommitted = false;
const boxLayoutRetry = document.getElementById("boxLayoutRetry");

function setAutoSaveStatus(message, type = "muted") {
    if (!boxAutoSaveStatus) return;

    boxAutoSaveStatus.textContent = message;
    boxAutoSaveStatus.classList.remove("text-muted", "text-success", "text-danger");

    if (type === "success") {
        boxAutoSaveStatus.classList.add("text-success");
    } else if (type === "danger") {
        boxAutoSaveStatus.classList.add("text-danger");
    } else {
        boxAutoSaveStatus.classList.add("text-muted");
    }
}

function clearSwapTargets() {
    document.querySelectorAll(".sortable-box-item.swap-target").forEach(item => {
        item.classList.remove("swap-target");
    });
}

function refreshEmptyState(container) {
    const items = container.querySelectorAll(".sortable-box-item");
    let emptyBox = container.querySelector(".box-side-empty");

    if (items.length === 0) {
        if (!emptyBox) {
            emptyBox = document.createElement("div");
            emptyBox.className = "box-side-empty";
            emptyBox.textContent = container.dataset.position === "left"
                ? "Trenutno nema lijevih boxeva."
                : "Trenutno nema desnih boxeva.";
            container.appendChild(emptyBox);
        }
    } else if (emptyBox) {
        emptyBox.remove();
    }

    container.querySelectorAll(".sortable-box-item").forEach(item => {
        const badge = item.querySelector(".box-side-badge");
        if (badge) {
            badge.textContent = container.dataset.position === "left" ? "Lijevo" : "Desno";
        }
    });
}

function updateSideCounts() {
    const leftList = document.getElementById("leftBoxList");
    const rightList = document.getElementById("rightBoxList");

    const leftCount = leftList ? leftList.querySelectorAll(".sortable-box-item").length : 0;
    const rightCount = rightList ? rightList.querySelectorAll(".sortable-box-item").length : 0;

    if (topLeftCount) topLeftCount.textContent = leftCount;
    if (topRightCount) topRightCount.textContent = rightCount;
    if (leftColumnCount) leftColumnCount.textContent = leftCount;
    if (rightColumnCount) rightColumnCount.textContent = rightCount;
}

function refreshAllBoxStates() {
    boxLists.forEach(container => refreshEmptyState(container));
    updateSideCounts();
    refreshMoveControls();
    boxLists.forEach(list => {
        const count = list.querySelectorAll(".sortable-box-item").length;
        const badge = document.querySelector(`[data-box-count="${list.dataset.position}"]`);
        if (badge) badge.textContent = `${count}/${list.dataset.max || "3"}`;
    });
    const activeId = boxLayoutForm?.querySelector('[name="active_box_id"]')?.value;
    const active = [...document.querySelectorAll(".sortable-box-item")].find(item => item.dataset.boxId === activeId);
    const positionField = document.querySelector('#editBoxForm select[name="position"]');
    if (active && positionField) {
        const position = active.parentElement.dataset.position;
        if (!positionField.dataset.layoutPosition || positionField.dataset.layoutPosition !== position) {
            positionField.value = position;
        }
        positionField.dataset.layoutPosition = position;
        const activeBadge = document.getElementById("activeBoxPosition");
        if (activeBadge) {
            activeBadge.textContent = position === "left" ? "Lijevo" : "Desno";
            activeBadge.classList.toggle("text-bg-primary", position === "left");
            activeBadge.classList.toggle("text-bg-success", position === "right");
        }
        [...positionField.options].forEach(option => {
            const list = [...boxLists].find(list => list.dataset.position === option.value);
            option.disabled = option.value !== position && list &&
                list.querySelectorAll(".sortable-box-item").length >= Number(list.dataset.max || 3);
        });
    }
}

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll(".sortable-box-item:not(.dragging)")];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;

        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function collectBoxLayout() {
    const layout = [];
    let valid = true;

    boxLists.forEach(container => {
        const maxPerSide = parseInt(container.dataset.max || "3", 10);
        const items = [...container.querySelectorAll(".sortable-box-item")];

        if (items.length > maxPerSide) {
            valid = false;
        }

        items.forEach(item => {
            layout.push({
                id: parseInt(item.dataset.boxId, 10),
                position: container.dataset.position
            });
        });
    });

    return { valid, layout };
}

function autoSaveBoxLayout() {
    if (!boxLayoutForm || !boxLayoutJson) return;
    const result = collectBoxLayout();
    if (!result.valid) {
        setAutoSaveStatus("Jedna strana ima previše boxeva. Raspored nije spremljen.", "danger");
        return;
    }
    pendingLayout = result.layout;
    flushBoxLayout();
}

async function flushBoxLayout() {
    if (saveInFlight || !pendingLayout) return;
    const layout = pendingLayout;
    pendingLayout = null;
    saveInFlight = true;
    boxLayoutJson.value = JSON.stringify(layout);
    const formData = new FormData(boxLayoutForm);
    formData.set("save_box_layout", "1");
    formData.set("box_layout_json", JSON.stringify(layout));
    const retryHadFocus = document.activeElement === boxLayoutRetry;
    if (boxLayoutRetry) boxLayoutRetry.hidden = true;
    setAutoSaveStatus("Spremam raspored...", "muted");
    if (retryHadFocus) boxAutoSaveStatus?.focus();
    let failed = false;
    try {
        const response = await fetch(window.location.href, {
            method: "POST", body: formData, credentials: "same-origin",
            headers: {"X-Requested-With": "XMLHttpRequest"}
        });
        // A redirected login or HTML error page must never look like a successful save.
        const result = await response.json();
        if (!response.ok || result.saved !== true ||
            JSON.stringify(result.layout) !== JSON.stringify(layout)) {
            throw new Error(result.error || "Spremanje rasporeda nije potvrđeno.");
        }
        savedLayout = JSON.stringify(layout);
        if (!pendingLayout) setAutoSaveStatus("Spremljeno.", "success");
    } catch (error) {
        failed = true;
        pendingLayout = collectBoxLayout().layout;
        const message = error instanceof SyntaxError || error instanceof TypeError
            ? "Spremanje nije uspjelo. Provjeri vezu i pokušaj ponovno."
            : error.message;
        setAutoSaveStatus(message + " Raspored na stranici je sačuvan.", "danger");
        if (boxLayoutRetry) boxLayoutRetry.hidden = false;
    } finally {
        saveInFlight = false;
        if (pendingLayout && !failed) flushBoxLayout();
    }
}

function refreshMoveControls() {
    document.querySelectorAll(".sortable-box-item").forEach(item => {
        const control = item.querySelector(".box-move-select");
        if (!control) return;
        const list = item.parentElement;
        const siblings = [...list.querySelectorAll(".sortable-box-item")];
        const index = siblings.indexOf(item);
        const other = [...boxLists].find(candidate => candidate !== list);
        control.replaceChildren();
        function option(value, text, disabled = false) {
            const option = document.createElement("option");
            option.value = value; option.textContent = text; option.disabled = disabled;
            control.appendChild(option);
        }
        option("", "Premjesti box…");
        option("up", "Pomakni gore", index === 0);
        option("down", "Pomakni dolje", index === siblings.length - 1);
        if (other) {
            const others = [...other.querySelectorAll(".sortable-box-item")];
            if (others.length < Number(other.dataset.max || 3)) {
                option("across", other.dataset.position === "left" ? "Premjesti lijevo" : "Premjesti desno");
            } else {
                others.forEach(target => option("swap:" + target.dataset.boxId,
                    "Zamijeni s: " + target.querySelector(".fw-semibold").textContent.trim()));
            }
        }
        control.value = "";
    });
}

function moveBox(item, action) {
    const list = item.parentElement;
    const items = [...list.querySelectorAll(".sortable-box-item")];
    const index = items.indexOf(item);
    const other = [...boxLists].find(candidate => candidate !== list);
    if (action === "up" && index > 0) list.insertBefore(item, items[index - 1]);
    else if (action === "down" && index < items.length - 1) list.insertBefore(items[index + 1], item);
    else if (action === "across" && other && other.querySelectorAll(".sortable-box-item").length < Number(other.dataset.max || 3)) {
        other.appendChild(item);
    } else if (action.startsWith("swap:") && other) {
        const target = [...other.querySelectorAll(".sortable-box-item")].find(candidate => candidate.dataset.boxId === action.slice(5));
        if (!target) return;
        const next = item.nextSibling;
        other.insertBefore(item, target);
        list.insertBefore(target, next);
    } else return;
    refreshAllBoxStates();
    item.querySelector(".box-move-select")?.focus();
    autoSaveBoxLayout();
}

if (boxLayoutRetry) boxLayoutRetry.addEventListener("click", autoSaveBoxLayout);
if (boxLayoutForm) window.addEventListener("beforeunload", event => {
    if (saveInFlight || pendingLayout || JSON.stringify(collectBoxLayout().layout) !== savedLayout) {
        event.preventDefault();
        event.returnValue = "";
    }
});

if (boxLists.length) {
    boxLists.forEach(container => {
        refreshEmptyState(container);

        container.addEventListener("dragover", function (e) {
            e.preventDefault();
            container.classList.add("drag-target");
            clearSwapTargets();

            if (!draggedItem) return;

            const maxPerSide = parseInt(container.dataset.max || "3", 10);
            const currentItems = container.querySelectorAll(".sortable-box-item").length;
            const sameContainer = draggedItem.parentElement === container;
            const hoveredItem = e.target.closest(".sortable-box-item");

            if (!sameContainer && currentItems >= maxPerSide) {
                if (hoveredItem && hoveredItem !== draggedItem) {
                    hoveredItem.classList.add("swap-target");
                }
                return;
            }

            const afterElement = getDragAfterElement(container, e.clientY);

            if (afterElement == null) {
                container.appendChild(draggedItem);
            } else {
                container.insertBefore(draggedItem, afterElement);
            }

            refreshAllBoxStates();
        });

        container.addEventListener("dragenter", function (e) {
            e.preventDefault();
            container.classList.add("drag-target");
        });

        container.addEventListener("dragleave", function (e) {
            if (!container.contains(e.relatedTarget)) {
                container.classList.remove("drag-target");
                clearSwapTargets();
            }
        });

        container.addEventListener("drop", function (e) {
            e.preventDefault();
            container.classList.remove("drag-target");

            if (!draggedItem) {
                clearSwapTargets();
                return;
            }

            const maxPerSide = parseInt(container.dataset.max || "3", 10);
            const currentItems = container.querySelectorAll(".sortable-box-item").length;
            const sameContainer = draggedItem.parentElement === container;
            const targetItem = e.target.closest(".sortable-box-item");

            if (!sameContainer && currentItems >= maxPerSide) {
                if (targetItem && targetItem !== draggedItem && dragOriginContainer) {
                    const targetNextSibling = targetItem.nextElementSibling;

                    if (dragOriginNextSibling && dragOriginNextSibling.parentElement === dragOriginContainer) {
                        dragOriginContainer.insertBefore(targetItem, dragOriginNextSibling);
                    } else {
                        dragOriginContainer.appendChild(targetItem);
                    }

                    if (targetNextSibling && targetNextSibling.parentElement === container) {
                        container.insertBefore(draggedItem, targetNextSibling);
                    } else {
                        container.appendChild(draggedItem);
                    }
                }
            }

            dragCommitted = true;
            clearSwapTargets();
            refreshAllBoxStates();
            autoSaveBoxLayout();
        });
    });

    document.querySelectorAll(".sortable-box-item").forEach(item => {
        const actions = document.createElement("div");
        actions.className = "box-move-actions";
        const control = document.createElement("select");
        control.className = "box-move-select";
        control.setAttribute("aria-label", "Premjesti box: " + item.querySelector(".fw-semibold").textContent.trim());
        control.addEventListener("change", () => moveBox(item, control.value));
        actions.appendChild(control);
        item.appendChild(actions);
        item.addEventListener("dragstart", function () {
            dragSnapshot = [...boxLists].map(list => ({list, items: [...list.querySelectorAll(".sortable-box-item")]}));
            dragCommitted = false;
            draggedItem = item;
            dragOriginContainer = item.parentElement;
            dragOriginNextSibling = item.nextElementSibling;
            item.classList.add("dragging");
            clearSwapTargets();
            setAutoSaveStatus("Povuci box na željeno mjesto.", "muted");
        });

        item.addEventListener("dragend", function () {
            if (!dragCommitted && dragSnapshot) {
                dragSnapshot.forEach(({list, items}) => items.forEach(item => list.appendChild(item)));
                setAutoSaveStatus("Premještanje je otkazano.", "muted");
            }
            dragSnapshot = null;
            item.classList.remove("dragging");
            boxLists.forEach(list => list.classList.remove("drag-target"));
            clearSwapTargets();
            refreshAllBoxStates();
            draggedItem = null;
            dragOriginContainer = null;
            dragOriginNextSibling = null;
        });
    });

    refreshAllBoxStates();

    if (boxLayoutForm && boxLayoutJson) {
        boxLayoutForm.addEventListener("submit", function (e) {
            const result = collectBoxLayout();

            if (!result.valid) {
                e.preventDefault();
                alert("Na jednoj strani može biti najviše 3 boxa.");
                return;
            }

            boxLayoutJson.value = JSON.stringify(result.layout);
        });
    }
}

    const editBoxForm = document.getElementById("editBoxForm");
    const titleInput = document.getElementById("id_title");
    const titleCounter = document.getElementById("boxTitleCounter");
    const contentCounter = document.getElementById("boxContentCounter");
    const contentError = document.getElementById("boxContentError");
    const contentLimit = parseInt(editBoxForm?.dataset.contentLimit || "1200", 10);

    function updateTitleCounter() {
        if (!titleInput || !titleCounter) return;
        titleCounter.textContent = titleInput.value.length;
    }

    function getPlainTextLengthFromHtml(html) {
        const temp = document.createElement("div");
        temp.innerHTML = html || "";
        return (temp.textContent || temp.innerText || "").replace(/\s+/g, " ").trim().length;
    }

    function updateContentCounter() {
        let length = 0;

        if (window.CKEDITOR && CKEDITOR.instances && CKEDITOR.instances.id_content) {
            length = getPlainTextLengthFromHtml(CKEDITOR.instances.id_content.getData());
        } else {
            const textarea = document.getElementById("id_content");
            if (textarea) {
                length = getPlainTextLengthFromHtml(textarea.value);
            }
        }

        if (contentCounter) {
            contentCounter.textContent = length;
        }

        if (contentError) {
            contentError.classList.toggle("d-none", length <= contentLimit);
        }

        return length;
    }

    if (titleInput) {
        updateTitleCounter();
        titleInput.addEventListener("input", updateTitleCounter);
    }

    if (window.CKEDITOR && CKEDITOR.instances && CKEDITOR.instances.id_content) {
        CKEDITOR.instances.id_content.on("instanceReady", updateContentCounter);
        CKEDITOR.instances.id_content.on("change", updateContentCounter);
        updateContentCounter();
    } else {
        const textarea = document.getElementById("id_content");
        if (textarea) {
            updateContentCounter();
            textarea.addEventListener("input", updateContentCounter);
        }
    }

    if (editBoxForm) {
        editBoxForm.addEventListener("submit", function (e) {
            if (updateContentCounter() > contentLimit) {
                e.preventDefault();
            }
        });
    }
});
