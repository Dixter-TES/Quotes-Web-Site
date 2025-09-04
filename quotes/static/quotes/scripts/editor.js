const csrftoken = Cookies.get("csrftoken");

const openPopup = document.getElementById("openPopup");
const closePopup = document.getElementById("closePopup");
const popup = document.getElementById("popup");
const popupTitle = document.getElementById("popupTitle");

closePopup.addEventListener("click", () => {
    popup.style.display = "none";
    window.location.replace("/editor/");
});

function showPopup(title) {
    popup.style.display = "flex";
    popupTitle.textContent = title
}

function addQuote() {
    showPopup("Добавление цитаты");
}

function deleteQuote(quoteId) {
    if (!confirm("Вы уверены, что хотите удалить эту цитату?")) {
        return;
    }

    $.ajax({
        url: `/api/quotes/${quoteId}/`,
        type: "DELETE",
        headers: { "X-CSRFToken": csrftoken },
        success: function (result) {
            $(`#quote_${quoteId}`).remove();
        },

        error: function (xhr, status, error) {
            alert("Ошибка при удалении цитаты.");
        },
    });
}

function editQuote(quoteId) {
    window.location.replace("/editor/" + quoteId);
}

function updateQuoteForm(quoteData) {}
