const getCSRFToken = () => {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
  return cookieValue || "";
};

const fetchTicketById = (ticketId) => {
  $.ajax({
    url: "/api/tickets/" + ticketId, // Your Django API endpoint
    type: "GET",
    contentType: "application/json",
    headers: {
      "X-CSRFToken": getCSRFToken(), // Add CSRF token here
    },
    success: function (response) {
      setTimeout(() => {
        $('#updateTicketForm input[name="ticket_id"]').val(ticketId);
        $('#updateTicketForm input[name="title"]').val(response.title);
        $('#updateTicketForm textarea[name="description"]').val(
          response.description
        );
        $(
          `#updateTicketForm input[name="subject"][value="${response.subject}"]`
        ).attr("checked", "checked");

        $('#updateTicketForm select[name="status"]').val(response.status);
        $('#updateTicketForm select[name="priority"]').val(response.priority);
        $('#updateTicketForm select[name="order_id"]').val(response.order);
      }, 100);
    },
    error: function (xhr) {
      alert("Error: " + xhr.responseText); // Feedback for error
    },
  });
};

$(document).ready(function () {
  $("#createNewTicketForm").on("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Kiểm tra form có hợp lệ không
    if (!this.checkValidity()) {
      // Nếu không hợp lệ, hiển thị thông báo lỗi từ HTML5
      this.reportValidity();
      return;
    }

    const formData = new FormData(event.target);

    // Convert FormData to a JSON object
    const formValues = {};
    formData.forEach((value, key) => {
      formValues[key] = value;
    });

    console.log("JSON.stringify(formValues)", formValues);

    $.ajax({
      url: "/api/tickets/", // Your Django API endpoint
      type: "POST",
      data: JSON.stringify(formValues),
      contentType: "application/json",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Add CSRF token here
      },
      success: function (response) {
        const myModalEl = document.getElementById("createNewTicketModal");
        const modal = bootstrap.Modal.getInstance(myModalEl); // Get the modal instance
        modal.hide(); // Programmatically hide the modal

        $.notify(
          {
            message: "New ticket added successfully!",
            title: "Success",
            icon: "fa fa-bell",
          },
          {
            type: "success",
            placement: {
              from: "top",
              align: "right",
            },
            time: 4000,
            delay: 0,
          }
        );

        setTimeout(() => {
          location.reload();
        }, 1000);
      },
      error: function (xhr) {
        alert("Error: " + xhr.responseText); // Feedback for error
      },
    });
  });

  $("#updateTicketForm").on("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Kiểm tra form có hợp lệ không
    if (!this.checkValidity()) {
      // Nếu không hợp lệ, hiển thị thông báo lỗi từ HTML5
      this.reportValidity();
      return;
    }

    const formData = new FormData(event.target);

    // Convert FormData to a JSON object
    const formValues = {};
    formData.forEach((value, key) => {
      formValues[key] = value;
    });

    console.log("JSON.stringify(formValues)", formValues);

    $.ajax({
      url: "/api/tickets/" + formValues.ticket_id + "/", // Your Django API endpoint
      type: "PUT",
      data: JSON.stringify(formValues),
      contentType: "application/json",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Add CSRF token here
      },
      success: function (response) {
        const myModalEl = document.getElementById("updateTicketModal");
        const modal = bootstrap.Modal.getInstance(myModalEl); // Get the modal instance
        modal.hide(); // Programmatically hide the modal

        $.notify(
          {
            message: "Ticket update successfully!",
            title: "Success",
            icon: "fa fa-bell",
          },
          {
            type: "success",
            placement: {
              from: "top",
              align: "right",
            },
            time: 4000,
            delay: 0,
          }
        );

        setTimeout(() => {
          location.reload();
        }, 1000);
      },
      error: function (xhr) {
        alert("Error: " + xhr.responseText); // Feedback for error
      },
    });
  });
});
