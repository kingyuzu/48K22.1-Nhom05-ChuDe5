const fetchContactById = (contact_id) => {
  $.ajax({
    url: "/api/contacts/" + contact_id +"/", // Your Django API endpoint
    type: "GET",
    contentType: "application/json",
    headers: {
      "X-CSRFToken": getCSRFToken(), // Add CSRF token here
    },
    success: function (response) {
      $('#updateContactForm input[name="contact_id"]').val(response.contact_id);
      $('#updateContactForm input[name="first_name"]').val(response.user.first_name);
      $('#updateContactForm input[name="last_name"]').val(response.user.last_name);
      $('#updateContactForm input[name="email"]').val(response.user.email);
      $('#updateContactForm input[name="address"]').val(response.user.address);
      $('#updateContactForm input[name="phone_number"]').val(response.user.phone_number);
      $('#updateContactForm select[name="lifecycle_stage"]').val(response.lifecycle_stage);
      $('#updateContactForm input[name="address"]').val(response.user.address);
    },
    error: function (xhr) {
      alert("Error: " + xhr.responseText); // Feedback for error
    },
  });
};

// const showEditCampaignModel = (id) => {
//   const modalElement = new bootstrap.Modal(
//     document.getElementById("editCampaignModal")
//   );
//   modalElement.show(); // Programmatically show the modal

//   $.ajax({
//     url: "/api/campaigns/" + id + "/", // Your Django API endpoint
//     type: "GET",
//     contentType: "application/json",
//     headers: {
//       "X-CSRFToken": getCSRFToken(), // Add CSRF token here
//     },
//     success: function (response) {
//       $('#editCampaignForm input[name="campaign_id"]').val(
//         response.campaign_id
//       );
//       $('#editCampaignForm input[name="name"]').val(response.name);
//       $('#editCampaignForm input[name="start_date"]').val(response.start_date);
//       $('#editCampaignForm input[name="end_date"]').val(response.end_date);
//       $('#editCampaignForm select[name="status"]').val(response.status);
//     },
//     error: function (xhr) {
//       alert("Error: " + xhr.responseText); // Feedback for error
//     },
//   });
// };

// const deleteCampaign = (id) => {
//   $.ajax({
//     url: "/api/campaigns/" + id + "/", // Your Django API endpoint
//     type: "DELETE",
//     contentType: "application/json",
//     headers: {
//       "X-CSRFToken": getCSRFToken(), // Add CSRF token here
//     },
//     success: function (response) {
//       $.notify(
//         {
//           message: "Campaign deleted successfully!",
//           title: "Success",
//           icon: "fa fa-bell",
//         },
//         {
//           type: "success",
//           placement: {
//             from: "top",
//             align: "right",
//           },
//           time: 4000,
//           delay: 0,
//         }
//       );

//       setTimeout(() => {
//         location.reload();
//       }, 2000);
//     },
//     error: function (xhr) {
//       alert("Error: " + xhr.responseText); // Feedback for error
//     },
//   });
// };

// const deleteMailTrack = (id) => {
//   $.ajax({
//     url: "/api/mail-tracks/" + id + "/", // Your Django API endpoint
//     type: "DELETE",
//     contentType: "application/json",
//     headers: {
//       "X-CSRFToken": getCSRFToken(), // Add CSRF token here
//     },
//     success: function (response) {
//       $.notify(
//         {
//           message: "Email deleted successfully!",
//           title: "Success",
//           icon: "fa fa-bell",
//         },
//         {
//           type: "success",
//           placement: {
//             from: "top",
//             align: "right",
//           },
//           time: 4000,
//           delay: 0,
//         }
//       );

//       setTimeout(() => {
//         location.reload();
//       }, 2000);
//     },
//     error: function (xhr) {
//       console.log("xhr", xhr);

//       alert("Error: " + xhr.responseText); // Feedback for error
//     },
//   });
// };

// const sendCampaignEmails = (id, email, track_id) => {
//   // Disable tất cả các button có class 'send-email-btn'
//   // Dùng thư viện Jquery js

//   if (track_id) {
//     $("#send-email-to-" + track_id + "-btn").prop("disabled", true);
//     $("#send-email-to-" + track_id + "-btn").html(
//       '<i class="fas fa-paper-plane"></i>Sending mail...'
//     );
//   } else {
//     $(".send-email-btn").prop("disabled", true);
//     $(".send-email-btn").html(
//       '<i class="fas fa-paper-plane"></i>Sending mail...'
//     );
//   }

//   $.ajax({
//     url: `/api/campaigns/${id}/send-emails`, // Your Django API endpoint
//     type: "POST",
//     data: JSON.stringify({ email_list: email ? [email] : [] }),
//     contentType: "application/json",
//     headers: {
//       "X-CSRFToken": getCSRFToken(), // Add CSRF token here
//     },
//     success: function (response) {
//       $.notify(
//         {
//           message: "Email send successfully!",
//           title: "Success",
//           icon: "fa fa-bell",
//         },
//         {
//           type: "success",
//           placement: {
//             from: "top",
//             align: "right",
//           },
//           time: 4000,
//           delay: 0,
//         }
//       );

//       // Enable tất cả các button có class 'send-email-btn'
//       if (email) {
//         // tìm thẻ html có id là send-email-to-tran.thi@example.com-btn
//         // const btnidstr = "#"+`send-email-to-${email}-btn`;
//         $("#send-email-to-" + track_id + "-btn").prop("disabled", false);
//         $("#send-email-to-" + track_id + "-btn").html(
//           '<i class="fas fa-envelope"></i>Send mail'
//         );
//       } else {
//         $(`.send-email-btn`).prop("disabled", false);
//         $(`.send-email-btn`).html('<i class="fas fa-envelope"></i>Send mail');
//       }

//       setTimeout(() => {
//         location.reload();
//       }, 2000);
//     },
//     error: function (xhr) {
//       // Enable tất cả các button có class 'send-email-btn'
//       $(".send-email-btn").prop("disabled", false);
//       alert("Error: " + xhr.responseText); // Feedback for error
//     },
//   });
// };

$(document).ready(function () {
  $("#createNewContactForm").on("submit", function (event) {
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

    console.log("formValues", formValues)

    $.ajax({
      url: "/api/contacts/",
      type: "POST",
      data: JSON.stringify(formValues),
      contentType: "application/json",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Add CSRF token here
      },
      success: function (response) {
        const myModalEl = document.getElementById("createNewContactModal");
        const modal = bootstrap.Modal.getInstance(myModalEl); // Get the modal instance
        modal.hide(); // Programmatically hide the modal

        $.notify(
          {
            message: "New contact added successfully!",
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
        }, 2000);
      },
      error: function (xhr) {
        alert("Error: " + xhr.responseText); // Feedback for error
      },
    });
  });

  $("#updateContactForm").on("submit", function (event) {
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

    $.ajax({
      url: "/api/contacts/" + formValues.contact_id + "/",
      type: "PUT",
      data: JSON.stringify(formValues),
      contentType: "application/json",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Add CSRF token here
      },
      success: function (response) {
        const myModalEl = document.getElementById("updateContactModal");
        const modal = bootstrap.Modal.getInstance(myModalEl); // Get the modal instance
        modal.hide(); // Programmatically hide the modal

        $.notify(
          {
            message: "Edit successfully!",
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
        }, 2000);
      },
      error: function (xhr) {
        console.log("xhr", xhr);

        alert("Error: " + xhr.responseText); // Feedback for error
      },
    });
  });

  // $("#addNewEmailsForm").on("submit", function (event) {
  //   event.preventDefault(); // Prevent the default form submission

  //   // Kiểm tra form có hợp lệ không
  //   if (!this.checkValidity()) {
  //     // Nếu không hợp lệ, hiển thị thông báo lỗi từ HTML5
  //     this.reportValidity();
  //     return;
  //   }

  //   const formData = new FormData(event.target);

  //   // Convert FormData to a JSON object
  //   const formValues = {
  //     emails: [],
  //   };
  //   let campaign_id = null;

  //   formData.forEach((value, key) => {
  //     if (key === "emails") {
  //       formValues.emails.push(value);
  //     }
  //     if (key === "campaign_id") {
  //       campaign_id = value;
  //     }
  //   });
  //   console.log("formData", formValues);

  //   $.ajax({
  //     url: `/api/campaigns/${campaign_id}/add-emails`,
  //     type: "POST",
  //     data: JSON.stringify(formValues),
  //     contentType: "application/json",
  //     headers: {
  //       "X-CSRFToken": getCSRFToken(), // Add CSRF token here
  //     },
  //     success: function (response) {
  //       const myModalEl = document.getElementById("addNewEmailsModal");
  //       const modal = bootstrap.Modal.getInstance(myModalEl); // Get the modal instance
  //       modal.hide(); // Programmatically hide the modal

  //       $.notify(
  //         {
  //           message: "Add emails successfully!",
  //           title: "Success",
  //           icon: "fa fa-bell",
  //         },
  //         {
  //           type: "success",
  //           placement: {
  //             from: "top",
  //             align: "right",
  //           },
  //           time: 4000,
  //           delay: 0,
  //         }
  //       );

  //       setTimeout(() => {
  //         location.reload();
  //       }, 2000);
  //     },
  //     error: function (xhr) {
  //       console.log("xhr", xhr);

  //       alert("Error: " + xhr.responseText); // Feedback for error
  //     },
  //   });
  // });
});
