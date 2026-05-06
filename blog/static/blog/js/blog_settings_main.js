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
let saveRequestId = 0;

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
        setAutoSaveStatus("Automatsko spremanje nije uspjelo jer jedna strana ima previše boxeva.", "danger");
        return;
    }

    boxLayoutJson.value = JSON.stringify(result.layout);

    const formData = new FormData(boxLayoutForm);
    formData.set("save_box_layout", "1");

    const currentRequestId = ++saveRequestId;

    setAutoSaveStatus("Spremam raspored...", "muted");

    fetch(window.location.href, {
        method: "POST",
        body: formData,
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Save failed");
        }
        return response.text();
    })
    .then(() => {
        if (currentRequestId !== saveRequestId) return;
        setAutoSaveStatus("Spremljeno.", "success");
    })
    .catch(() => {
        if (currentRequestId !== saveRequestId) return;
        setAutoSaveStatus("Automatsko spremanje nije uspjelo. Možeš kliknuti ručno spremanje.", "danger");
    });
}

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

            clearSwapTargets();
            refreshAllBoxStates();
            autoSaveBoxLayout();
        });
    });

    document.querySelectorAll(".sortable-box-item").forEach(item => {
        item.addEventListener("dragstart", function () {
            draggedItem = item;
            dragOriginContainer = item.parentElement;
            dragOriginNextSibling = item.nextElementSibling;
            item.classList.add("dragging");
            clearSwapTargets();
            setAutoSaveStatus("Povuci box na željeno mjesto.", "muted");
        });

        item.addEventListener("dragend", function () {
            item.classList.remove("dragging");
            boxLists.forEach(list => list.classList.remove("drag-target"));
            clearSwapTargets();
            refreshAllBoxStates();
            draggedItem = null;
            dragOriginContainer = null;
            dragOriginNextSibling = null;
        });
    });

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
