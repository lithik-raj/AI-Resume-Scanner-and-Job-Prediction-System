function toggleMilo() {
  const chat = document.getElementById("milo-chat-window");

  if (!chat) {
    return;
  }

  chat.classList.toggle("milo-open");

  if (chat.classList.contains("milo-open")) {
    const input = document.getElementById("miloChatInput");

    if (input) {
      setTimeout(function () {
        input.focus();
      }, 200);
    }
  }
}

/* =========================================================
   ADD MESSAGE
   ========================================================= */

function addMiloMessage(message, type) {
  const container = document.getElementById("miloChatMessages");

  if (!container) {
    return;
  }

  const messageElement = document.createElement("div");

  messageElement.className =
    "milo-chat-message " +
    (type === "user" ? "milo-chat-user" : "milo-chat-bot");

  messageElement.textContent = message;

  container.appendChild(messageElement);

  container.scrollTop = container.scrollHeight;
}

/* =========================================================
   SEND MESSAGE
   ========================================================= */

async function sendFloatingMiloMessage() {
  const input = document.getElementById("miloChatInput");

  const typing = document.getElementById("miloTyping");

  if (!input) {
    return;
  }

  const message = input.value.trim();

  if (!message) {
    return;
  }

  addMiloMessage(message, "user");

  input.value = "";

  if (typing) {
    typing.style.display = "block";
  }

  const formData = new FormData();

  formData.append("message", message);

  /*
       RESULT PAGE DATA

       These variables are created
       only on result.html.

       On other pages they simply
       won't exist.
    */

  if (typeof miloRecommendations !== "undefined") {
    formData.append(
      "recommendations_data",
      JSON.stringify(miloRecommendations),
    );
  }

  if (typeof miloPrediction !== "undefined") {
    formData.append("prediction_data", JSON.stringify(miloPrediction));
  }

  if (typeof miloSkills !== "undefined") {
    formData.append("skills_data", JSON.stringify(miloSkills));
  }

  if (typeof miloATSScore !== "undefined") {
    formData.append("ats_score", String(miloATSScore));
  }

  try {
    const response = await fetch("/milo", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      addMiloMessage(data.response, "bot");
    } else {
      addMiloMessage(
        data.response || "Milo could not process your question.",
        "bot",
      );
    }
  } catch (error) {
    console.error("Milo error:", error);

    addMiloMessage(
      "Milo could not connect to the server. Please try again.",
      "bot",
    );
  }

  if (typing) {
    typing.style.display = "none";
  }
}

/* =========================================================
   ENTER KEY
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("miloChatInput");

  if (!input) {
    return;
  }

  input.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();

      sendFloatingMiloMessage();
    }
  });
});
