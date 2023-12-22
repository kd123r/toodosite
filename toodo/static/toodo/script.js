function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}

function addTodo(url, payload) {
    $.ajax({
      url: url,
      type: "POST",
      dataType: "html",
      data: payload,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      success: (data) => {
        $('.list-group').append(data);
      },
      error: (error) => {
        console.error(error);
      }
    });
}

function deleteTodo(url) {
    $.ajax({
      url: url,
      type: "DELETE",
      dataType: "json",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      success: (data) => {
        console.log(data);
        $("#todo" + data.deleted).remove()
      },
      error: (error) => {
        console.error(error);
      }
    });
}
