function sendLike(target, id) {
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    const currentRating = document.getElementById(`${id}-rating_value`);

    fetch(`/api/${target}/${id}/toggle_like`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
                   "X-CSRFToken": csrf,
         },
        body: JSON.stringify({ is_like: true }),
        
    })
    .then((res) => {
        if (res.status >= 400) console.error(res);
        return res.json();
    })
    .then((res) => {
        currentRating.textContent = `${res.rating}`;
    });
}

function sendDislike(target, id) {
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    const currentRating = document.getElementById(`${id}-rating_value`);

    fetch(`/api/${target}/${id}/toggle_like`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
            "X-CSRFToken": csrf,
         },
        body: JSON.stringify({ is_like: false }),
    })
    .then((res) => {
        if (res.status >= 400) console.error(res);
        return res.json();
    })
    .then((res) => {
        currentRating.textContent = `${res.rating}`;
    });
}

function toggleCorrect(questionId, answerId, isCorrect) {
  const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

  fetch(`/api/question/${questionId}/correct_answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({ answer_id: answerId, is_correct: isCorrect }),
  })
  .then((res) => res.json().then((data) => ({ ok: res.ok, status: res.status, data })))
  .then(({ ok, data }) => {
    if (!ok) {
      alert(data.error || "Ошибка");
      return;
    }

    if (data.correct === true) {
      document.querySelectorAll('.correct-btn input[type="checkbox"]').forEach(cb => {
        if (cb.id !== `correct-${answerId}`) cb.checked = false;
      });
    }
  })
  .catch(console.error);
}
